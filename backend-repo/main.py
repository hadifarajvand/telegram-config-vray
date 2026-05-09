#import requirement libraries
import os
import json
import sys
from pathlib import Path
import time
import warnings
import threading
import concurrent.futures
from contextlib import contextmanager

import jdatetime
from datetime import datetime, timezone, timedelta

#import web-based libraries
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL.*")

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from feeds.output_generation import generate_outputs
from scraper.collector import (
    build_subscription_state,
    run as scrape_run,
)


warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)

GEOIP_DIR = Path("./geoip-lite")
MMDB_FILENAME = "geoip-lite-country.mmdb"
MMDB_PATH = GEOIP_DIR / MMDB_FILENAME
MMDB_META_PATH = GEOIP_DIR / f"{MMDB_FILENAME}.meta.json"
MMDB_MIN_SIZE_BYTES = 1024 * 1024
MMDB_CHUNK_SIZE = 1024 * 1024
MMDB_MAX_WORKERS = 4
MMDB_URLS = [
    "https://raw.githubusercontent.com/P3TERX/GeoLite.mmdb/download/GeoLite2-Country.mmdb",
    "https://github.com/P3TERX/GeoLite.mmdb/raw/download/GeoLite2-Country.mmdb",
]


def mmdb_is_valid(mmdb_path):
    return mmdb_path.exists() and mmdb_path.stat().st_size >= MMDB_MIN_SIZE_BYTES


def load_mmdb_meta():
    if not MMDB_META_PATH.exists():
        return {}
    try:
        with open(MMDB_META_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception:
        return {}


def save_mmdb_meta(metadata):
    with open(MMDB_META_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=True, indent=2)


def load_env_file(path=".env"):
    env = {}
    if not os.path.exists(path):
        return env
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            env[key] = value
    return env


def get_env_value(key, env_map):
    return os.environ.get(key) or env_map.get(key)


def create_retry_session():
    session = requests.Session()
    retries = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=frozenset(["GET", "HEAD"]),
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


ENV_VARS = load_env_file(".env")

FETCH_SESSION = create_retry_session()
FETCH_SESSION.headers.update(
    {
        "User-Agent": "telegram-config-vray/1.0 (+https://t.me/s/)",
        "Accept-Language": "en-US,en;q=0.9",
    }
)
FETCH_SESSION.trust_env = False

REQUEST_TIMEOUT = (10, 30)
CONFIG_CHECK_WORKERS = int(get_env_value("CONFIG_CHECK_WORKERS", ENV_VARS) or 30)

SOCKS5_HOST = get_env_value("SOCKS5_HOST", ENV_VARS)
SOCKS5_PORT = get_env_value("SOCKS5_PORT", ENV_VARS)
SOCKS5_USER = get_env_value("SOCKS5_USER", ENV_VARS)
SOCKS5_PASS = get_env_value("SOCKS5_PASS", ENV_VARS)

if SOCKS5_HOST and SOCKS5_PORT:
    auth = ""
    if SOCKS5_USER and SOCKS5_PASS:
        auth = f"{SOCKS5_USER}:{SOCKS5_PASS}@"
    proxy_url = f"socks5h://{auth}{SOCKS5_HOST}:{SOCKS5_PORT}"
    try:
        import socks  # noqa: F401
    except ImportError as exc:
        raise RuntimeError(
            "SOCKS5 proxy is configured in .env, but PySocks is not installed in the active environment. "
            "Install it with: .venvmac/bin/pip install PySocks"
        ) from exc
    FETCH_SESSION.proxies.update({"http": proxy_url, "https": proxy_url})
else:
    proxy_url = None


@contextmanager
def no_proxy_env():
    keys = [
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "http_proxy",
        "https_proxy",
        "ALL_PROXY",
        "all_proxy",
        "NO_PROXY",
        "no_proxy",
    ]
    saved = {k: os.environ.get(k) for k in keys}
    try:
        for k in keys:
            if k in os.environ:
                del os.environ[k]
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                if k in os.environ:
                    del os.environ[k]
            else:
                os.environ[k] = v


def get_remote_mmdb_meta(session):
    for url in MMDB_URLS:
        try:
            response = session.head(url, allow_redirects=True, timeout=(10, 30))
            response.raise_for_status()
            return {
                "source_url": url,
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
                "content_length": response.headers.get("Content-Length"),
            }
        except Exception:
            continue
    return {}


def is_mmdb_up_to_date(local_meta, remote_meta):
    if not mmdb_is_valid(MMDB_PATH):
        return False
    if not remote_meta:
        return False

    remote_etag = remote_meta.get("etag")
    remote_last_modified = remote_meta.get("last_modified")
    local_etag = local_meta.get("etag")
    local_last_modified = local_meta.get("last_modified")
    remote_content_length = remote_meta.get("content_length")

    etag_match = bool(remote_etag and local_etag and remote_etag == local_etag)
    lm_match = bool(
        remote_last_modified and local_last_modified and remote_last_modified == local_last_modified
    )
    size_match = bool(
        remote_content_length
        and str(MMDB_PATH.stat().st_size) == str(remote_content_length)
    )

    return etag_match or (lm_match and size_match)


def download_mmdb_in_chunks(session, url, tmp_path, content_length, max_workers=MMDB_MAX_WORKERS):
    if not tmp_path.exists():
        with open(tmp_path, "wb") as file:
            file.truncate(content_length)

    next_start = 0
    bytes_written = 0
    last_report = 0.0
    lock = threading.Lock()

    def worker():
        nonlocal next_start
        while True:
            with lock:
                if next_start >= content_length:
                    return
                start = next_start
                end = min(next_start + MMDB_CHUNK_SIZE - 1, content_length - 1)
                next_start = end + 1

            headers = {"Range": f"bytes={start}-{end}"}
            while True:
                try:
                    response = session.get(url, headers=headers, stream=True, timeout=(10, 60))
                    if response.status_code not in (200, 206):
                        raise RuntimeError(f"unexpected status {response.status_code}")

                    with lock:
                        with open(tmp_path, "r+b") as file:
                            file.seek(start)
                            for chunk in response.iter_content(chunk_size=1024 * 256):
                                if chunk:
                                    file.write(chunk)
                                    nonlocal bytes_written, last_report
                                    bytes_written += len(chunk)
                                    now = time.time()
                                    if now - last_report >= 0.5:
                                        pct = (bytes_written / content_length) * 100
                                        print(
                                            f"\rDownloading MMDB: {bytes_written}/{content_length} bytes ({pct:.1f}%)",
                                            end="",
                                            flush=True,
                                        )
                                        last_report = now
                    break
                except Exception:
                    time.sleep(2)

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(max_workers)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"\rDownloading MMDB: {content_length}/{content_length} bytes (100.0%)")


def update_mmdb(max_attempts=None):
    GEOIP_DIR.mkdir(exist_ok=True)

    session = FETCH_SESSION
    local_meta = load_mmdb_meta()
    remote_meta = get_remote_mmdb_meta(session)

    if is_mmdb_up_to_date(local_meta, remote_meta):
        print("MMDB is up to date; skipping download.")
        return

    errors = []
    tmp_path = GEOIP_DIR / f".{MMDB_FILENAME}.tmp"

    attempt = 0
    while True:
        attempt += 1
        for url in MMDB_URLS:
            try:
                head = session.head(url, allow_redirects=True, timeout=(10, 30))
                head.raise_for_status()
                content_length = head.headers.get("Content-Length")
                if not content_length or not content_length.isdigit():
                    raise RuntimeError("missing content length")
                content_length = int(content_length)

                if tmp_path.exists() and tmp_path.stat().st_size > content_length:
                    tmp_path.unlink()

                download_mmdb_in_chunks(session, url, tmp_path, content_length)

                if tmp_path.stat().st_size != content_length:
                    raise RuntimeError("downloaded size mismatch")

                if not mmdb_is_valid(tmp_path):
                    raise RuntimeError(f"Downloaded MMDB is too small: {tmp_path.stat().st_size} bytes")

                os.replace(tmp_path, MMDB_PATH)
                save_mmdb_meta(
                    {
                        "etag": head.headers.get("ETag") or remote_meta.get("etag"),
                        "last_modified": head.headers.get("Last-Modified") or remote_meta.get("last_modified"),
                        "content_length": str(MMDB_PATH.stat().st_size),
                        "downloaded_from": url,
                    }
                )
                print(f"MMDB downloaded successfully from {url}.")
                return
            except Exception as exc:
                errors.append(f"attempt={attempt}, url={url}, error={exc}")
            finally:
                if tmp_path.exists() and tmp_path.stat().st_size == 0:
                    tmp_path.unlink()

        print(f"MMDB download failed on attempt {attempt}. Retrying in 2s...")
        time.sleep(2)

    if mmdb_is_valid(MMDB_PATH):
        print("MMDB update failed; keeping the existing local MMDB file.")
        return

    raise RuntimeError("MMDB download failed after retries: " + " | ".join(errors[-5:]))


update_mmdb()


# Clean up unmatched file
with open("./splitted/no-match", "w", encoding="utf-8") as no_match_file:
    no_match_file.write("#Non-Adaptive Configurations\n")


# Load and read last date and time update
with open('./last update', 'r') as file:
    last_update_datetime = file.readline()
    last_update_datetime = datetime.strptime(last_update_datetime, '%Y-%m-%d %H:%M:%S.%f%z')

# Write the current date and time update
with open('./last update', 'w') as file:
    current_datetime_update = datetime.now(tz = timezone(timedelta(hours = 3, minutes = 30)))
    jalali_current_datetime_update = jdatetime.datetime.now(tz = timezone(timedelta(hours = 3, minutes = 30)))
    file.write(f'{current_datetime_update}')

print(f"Latest Update: {last_update_datetime.strftime('%a, %d %b %Y %X %Z')}\nCurrent Update: {current_datetime_update.strftime('%a, %d %b %Y %X %Z')}")


def get_absolute_paths(start_path):
    abs_paths = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            abs_path = Path(root).joinpath(file).resolve()
            abs_paths.append(str(abs_path))
    return abs_paths

dirs_list = ['./security', './protocols', './networks', './layers',
            './subscribe', './splitted', './channels']

if (int(jalali_current_datetime_update.day) == 1 and int(jalali_current_datetime_update.hour) == 0) or (int(jalali_current_datetime_update.day) == 15 and int(jalali_current_datetime_update.hour) == 0):
    print("The All Collected Configurations Cleared Based On Scheduled Day".title())
    last_update_datetime = last_update_datetime - timedelta(days=3)
    print(f"The Latest Update Time Is Set To {last_update_datetime.strftime('%a, %d %b %Y %X %Z')}".title())
    for root_dir in dirs_list:
        for path in get_absolute_paths(root_dir):
            if not path.endswith('readme.md'):
                with open(path, 'w') as file:
                    file.write('')
                    file.close
            else:
                continue


def json_load(path):
    # Open and read the json file
    with open(path, 'r') as file:
        # Load json file content into list
        list_content = json.load(file)
    # Return list of json content
    return list_content


# Scraping/fetching is fully delegated to scraper.collector.

scrape_state = scrape_run()
subscription_state = build_subscription_state(
    scrape_state,
    invalid_array_channels=set(json_load("invalid telegram channels.json")) if Path("invalid telegram channels.json").exists() else set(),
)

channel_without_config = subscription_state["channel_without_config"]
telegram_channels = subscription_state["telegram_channels"]
new_telegram_channels = subscription_state["new_telegram_channels"]
new_channel_messages = subscription_state["new_channel_messages"]
removed_channel_array = subscription_state["removed_channel_array"]
new_array_channels = subscription_state["new_array_channels"]
array_shadowsocks = subscription_state["array_shadowsocks"]
array_trojan = subscription_state["array_trojan"]
array_vmess = subscription_state["array_vmess"]
array_vless = subscription_state["array_vless"]
array_reality = subscription_state["array_reality"]
array_tuic = subscription_state["array_tuic"]
array_hysteria = subscription_state["array_hysteria"]
array_juicity = subscription_state["array_juicity"]
matches_shadowsocks = subscription_state["matches_shadowsocks"]
matches_trojan = subscription_state["matches_trojan"]
matches_vmess = subscription_state["matches_vmess"]
matches_vless = subscription_state["matches_vless"]
matches_reality = subscription_state["matches_reality"]
matches_tuic = subscription_state["matches_tuic"]
matches_hysteria = subscription_state["matches_hysteria"]
matches_juicity = subscription_state["matches_juicity"]
raw_matches_shadowsocks = subscription_state["raw_matches_shadowsocks"]
raw_matches_trojan = subscription_state["raw_matches_trojan"]
raw_matches_vmess = subscription_state["raw_matches_vmess"]
raw_matches_vless = subscription_state["raw_matches_vless"]
raw_matches_reality = subscription_state["raw_matches_reality"]
raw_matches_tuic = subscription_state["raw_matches_tuic"]
raw_matches_hysteria = subscription_state["raw_matches_hysteria"]
raw_matches_juicity = subscription_state["raw_matches_juicity"]
channel_matches_shadowsocks = subscription_state["channel_matches_shadowsocks"]
channel_matches_trojan = subscription_state["channel_matches_trojan"]
channel_matches_vmess = subscription_state["channel_matches_vmess"]
channel_matches_vless = subscription_state["channel_matches_vless"]
channel_matches_reality = subscription_state["channel_matches_reality"]
channel_matches_tuic = subscription_state["channel_matches_tuic"]
channel_matches_hysteria = subscription_state["channel_matches_hysteria"]
channel_matches_juicity = subscription_state["channel_matches_juicity"]
array_tls = subscription_state["array_tls"]
array_non_tls = subscription_state["array_non_tls"]
array_tcp = subscription_state["array_tcp"]
array_ws = subscription_state["array_ws"]
array_http = subscription_state["array_http"]
array_grpc = subscription_state["array_grpc"]
array_tls_channels = subscription_state["array_tls_channels"]
array_non_tls_channels = subscription_state["array_non_tls_channels"]
array_tcp_channels = subscription_state["array_tcp_channels"]
array_ws_channels = subscription_state["array_ws_channels"]
array_http_channels = subscription_state["array_http_channels"]
array_grpc_channels = subscription_state["array_grpc_channels"]
array_shadowsocks_channels = subscription_state["array_shadowsocks_channels"]
array_trojan_channels = subscription_state["array_trojan_channels"]
array_vmess_channels = subscription_state["array_vmess_channels"]
array_vless_channels = subscription_state["array_vless_channels"]
array_reality_channels = subscription_state["array_reality_channels"]
array_tuic_channels = subscription_state["array_tuic_channels"]
array_hysteria_channels = subscription_state["array_hysteria_channels"]
array_juicity_channels = subscription_state["array_juicity_channels"]
array_mixed = subscription_state["array_mixed"]
chunks = subscription_state["chunks"]
all_subscription_matches = subscription_state["all_subscription_matches"]
array_subscription_ipv4 = subscription_state["array_subscription_ipv4"]
array_subscription_ipv6 = subscription_state["array_subscription_ipv6"]
all_channel_matches = subscription_state["all_channel_matches"]
array_channel_ipv4 = subscription_state["array_channel_ipv4"]
array_channel_ipv6 = subscription_state["array_channel_ipv6"]
current_datetime_update = subscription_state["current_datetime_update"]
last_update_datetime = subscription_state["last_update_datetime"]

generate_outputs(subscription_state, Path(__file__).resolve().parent)
sys.exit(0)
