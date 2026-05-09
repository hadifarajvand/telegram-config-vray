from __future__ import annotations

"""
Scraper helpers extracted from the legacy monolith.

This module is intentionally a work-in-progress seam: the scraping pipeline
still lives in main.py for now, but the reusable helpers belong here.
"""

import base64
import concurrent.futures
import json
import math
import os
import re
import string
import time
from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any

import jdatetime
import requests
import urllib3
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from title import check_modify_config_parallel, create_country, create_internet_protocol

warnings = __import__("warnings")
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL.*")
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)


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
            env[key.strip()] = value.strip().strip("'").strip('"')
    return env


def get_env_value(key, env_map):
    return os.environ.get(key) or env_map.get(key)


def create_retry_session():
    session = requests.Session()
    retries = Retry(total=3, connect=3, read=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=frozenset(["GET", "HEAD"]))
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


ENV_VARS = load_env_file(".env")
FETCH_SESSION = create_retry_session()
FETCH_SESSION.headers.update(
    {"User-Agent": "telegram-config-vray/1.0 (+https://t.me/s/)", "Accept-Language": "en-US,en;q=0.9"}
)
FETCH_SESSION.trust_env = False
REQUEST_TIMEOUT = (10, 30)


@contextmanager
def no_proxy_env():
    keys = ["HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy", "ALL_PROXY", "all_proxy", "NO_PROXY", "no_proxy"]
    saved = {k: os.environ.get(k) for k in keys}
    try:
        for k in keys:
            os.environ.pop(k, None)
        yield
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def json_load(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def tg_channel_messages(channel_user):
    response = FETCH_SESSION.get(f"https://t.me/s/{channel_user}", timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("div", class_="tgme_widget_message")


def tg_message_time(div_message):
    div_message_info = div_message.find("div", class_="tgme_widget_message_info")
    message_datetime_tag = div_message_info.find("time")
    message_datetime = message_datetime_tag.get("datetime")
    datetime_object = datetime.fromisoformat(message_datetime)
    datetime_object = datetime.astimezone(datetime_object, tz=timezone(timedelta(hours=3, minutes=30)))
    datetime_now = datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
    return datetime_object, datetime_now, datetime_now - datetime_object


def tg_message_text(div_message, content_extracter):
    div_message_text = div_message.find("div", class_="tgme_widget_message_text")
    text_content = div_message_text.prettify()
    if content_extracter == "url":
        text_content = re.sub(r"<code>([^<>]+)</code>", r"\1", re.sub(r"\s*", "", text_content))
    elif content_extracter == "config":
        text_content = re.sub(
            r"<code>([^<>]+)</code>",
            r"\1",
            re.sub(r"<a[^<>]+>([^<>]+)</a>", r"\1", re.sub(r"\s*", "", text_content)),
        )
    return text_content


def fetch_channel_messages_with_retries(channel_user, max_attempts=3):
    attempt = 0
    while True:
        attempt += 1
        try:
            div_messages = tg_channel_messages(channel_user)
            return channel_user, div_messages, None
        except Exception as exc:
            if attempt >= max_attempts:
                return channel_user, [], exc
            time.sleep(min(10, 2**attempt))


def fetch_channels_batch(channels, invalid_channels=None, max_workers=5):
    messages = []
    removed = []
    invalid_channels = invalid_channels or set()
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fetch_channel_messages_with_retries, channel_user): channel_user
            for channel_user in channels
            if channel_user not in invalid_channels
        }
        for future in concurrent.futures.as_completed(futures):
            channel_user, div_messages, error = future.result()
            print(f"{channel_user}")
            if error is not None:
                removed.append(channel_user)
                continue
            if len(div_messages) == 0:
                removed.append(channel_user)
            messages.append((channel_user, div_messages))
    return messages, removed


def tg_username_extract(url):
    telegram_pattern = r"((http|Http|HTTP)://|(https|Https|HTTPS)://|(www|Www|WWW)\.|https://www\.|)(?P<telegram_domain>(t|T)\.(me|Me|ME)|(telegram|Telegram|TELEGRAM)\.(me|Me|ME)|(telegram|Telegram|TELEGRAM).(org|Org|ORG)|telesco.pe|(tg|Tg|TG).(dev|Dev|DEV)|(telegram|Telegram|TELEGRAM).(dog|Dog|DOG))/(?P<username>[a-zA-Z0-9_+-]+)"
    matches_url = re.match(telegram_pattern, url)
    return matches_url.group("username")


def html_content(html_address):
    response = FETCH_SESSION.get(html_address, timeout=REQUEST_TIMEOUT)
    soup = BeautifulSoup(response.text, "html.parser").text
    return soup


def is_valid_base64(string_value):
    try:
        byte_decoded = base64.b64decode(string_value)
        return base64.b64encode(byte_decoded).decode("utf-8") == string_value
    except Exception:
        return False


def decode_string(content):
    if is_valid_base64(content):
        content = base64.b64decode(content).decode("utf-8")
    return content


def decode_vmess(vmess_config):
    try:
        encoded_config = re.sub(r"vmess://", "", vmess_config)
        decoded_config = base64.b64decode(encoded_config).decode("utf-8")
        decoded_config_dict = json.loads(decoded_config)
        decoded_config_dict["ps"] = "VMESS"
        decoded_config = json.dumps(decoded_config_dict)
        encoded_config = decoded_config.encode("utf-8")
        encoded_config = base64.b64encode(encoded_config).decode("utf-8")
        return f"vmess://{encoded_config}"
    except Exception:
        return None


def remove_duplicate_modified(array_configuration):
    country_config_dict = dict()
    for config in array_configuration:
        try:
            if config.startswith("ss"):
                pattern = r"ss://(?P<id>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?#?(?P<title>(?<=#).*)?"
                shadowsocks_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = shadowsocks_match.group("ip")
                port = shadowsocks_match.group("port")
                non_title_config = f"SS-{ip}:{port}"
                country_config_dict[non_title_config] = config
            if config.startswith("trojan"):
                pattern = r"trojan://(?P<id>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\??(?P<params>[^#]+)?#?(?P<title>(?<=#).*)?"
                trojan_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = trojan_match.group("ip")
                port = trojan_match.group("port")
                non_title_config = f"TR-{ip}:{port}"
                country_config_dict[non_title_config] = config
            if config.startswith("vless"):
                pattern = r"vless://(?P<id>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                vless_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = vless_match.group("ip")
                port = vless_match.group("port")
                non_title_config = f"VL-{ip}:{port}"
                country_config_dict[non_title_config] = config
            if config.startswith("vmess"):
                vmess_pattern = r"vmess://(?P<json>[^#].*)"
                vmess_match = re.match(vmess_pattern, config, flags=re.IGNORECASE)
                json_string = vmess_match.group("json")
                json_string = base64.b64decode(json_string).decode("utf-8", errors="ignore")
                dict_params = json.loads(json_string)
                ip = dict_params.get("ip")
                port = dict_params.get("port")
                non_title_config = f"VM-{ip}:{port}"
                country_config_dict[non_title_config] = config
            if config.startswith("tuic"):
                pattern = r"tuic://(?P<id>[^:]+):(?P<pass>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                tuic_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = tuic_match.group("ip")
                port = tuic_match.group("port")
                non_title_config = f"TUIC-{ip}:{port}"
                country_config_dict[non_title_config] = config
            if config.startswith("hysteria"):
                pattern = r"hysteria://\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                hysteria_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = hysteria_match.group("ip")
                port = hysteria_match.group("port")
                non_title_config = f"HYSTERIA1-{ip}:{port}"
                country_config_dict[non_title_config] = config
            if config.startswith("hy2"):
                pattern = r"hy2://(?P<pass>[^@]+)@\[?(?P<ip>[a-zA-Z0-9\.:-]+?)\]?:(?P<port>[0-9]+)/?\?(?P<params>[^#]+)#?(?P<title>(?<=#).*)?"
                hysteria_match = re.match(pattern, config, flags=re.IGNORECASE)
                ip = hysteria_match.group("ip")
                port = hysteria_match.group("port")
                non_title_config = f"HYSTERIA2-{ip}:{port}"
                country_config_dict[non_title_config] = config
        except Exception:
            continue
    return list(country_config_dict.values())


def remove_duplicate(shadow_array, trojan_array, vmess_array, vless_array, reality_array, tuic_array, hysteria_array, juicity_array, vmess_decode_dedup=True):
    shadow_array = list(set(shadow_array))
    trojan_array = list(set(trojan_array))
    vmess_array = list(set(vmess_array))
    vless_array = list(set(vless_array))
    reality_array = list(set(reality_array))
    tuic_array = list(set(tuic_array))
    hysteria_array = list(set(hysteria_array))
    juicity_array = list(set(juicity_array))
    if vmess_decode_dedup:
        for index, element in enumerate(vmess_array):
            vmess_array[index] = decode_vmess(element)
        vmess_array = [config for config in vmess_array if config is not None]
        vmess_array = list(set(vmess_array))
    return shadow_array, trojan_array, vmess_array, vless_array, reality_array, tuic_array, hysteria_array, juicity_array


def modify_config(shadow_array, trojan_array, vmess_array, vless_array, reality_array, tuic_array, hysteria_array, check_port_connection=True):
    with no_proxy_env():
        shadow_array, shadow_tls_array, shadow_non_tls_array, shadow_tcp_array, shadow_ws_array, shadow_http_array, shadow_grpc_array = check_modify_config_parallel(
            array_configuration=shadow_array,
            protocol_type="SHADOWSOCKS",
            check_connection=check_port_connection,
            max_workers=5,
        )
        trojan_array, trojan_tls_array, trojan_non_tls_array, trojan_tcp_array, trojan_ws_array, trojan_http_array, trojan_grpc_array = check_modify_config_parallel(
            array_configuration=trojan_array,
            protocol_type="TROJAN",
            check_connection=check_port_connection,
            max_workers=5,
        )
        vmess_array, vmess_tls_array, vmess_non_tls_array, vmess_tcp_array, vmess_ws_array, vmess_http_array, vmess_grpc_array = check_modify_config_parallel(
            array_configuration=vmess_array,
            protocol_type="VMESS",
            check_connection=check_port_connection,
            max_workers=5,
        )
        vless_array, vless_tls_array, vless_non_tls_array, vless_tcp_array, vless_ws_array, vless_http_array, vless_grpc_array = check_modify_config_parallel(
            array_configuration=vless_array,
            protocol_type="VLESS",
            check_connection=check_port_connection,
            max_workers=5,
        )
        reality_array, reality_tls_array, reality_non_tls_array, reality_tcp_array, reality_ws_array, reality_http_array, reality_grpc_array = check_modify_config_parallel(
            array_configuration=reality_array,
            protocol_type="REALITY",
            check_connection=check_port_connection,
            max_workers=5,
        )
        tuic_array, _, _, _, _, _, _ = check_modify_config_parallel(
            array_configuration=tuic_array,
            protocol_type="TUIC",
            check_connection=False,
            max_workers=5,
        )
        hysteria_array, _, _, _, _, _, _ = check_modify_config_parallel(
            array_configuration=hysteria_array,
            protocol_type="HYSTERIA",
            check_connection=False,
            max_workers=5,
        )

    tls_array = []
    non_tls_array = []
    tcp_array = []
    ws_array = []
    http_array = []
    grpc_array = []

    for array in [shadow_tls_array, trojan_tls_array, vmess_tls_array, vless_tls_array, reality_tls_array]:
        tls_array.extend(array)
    for array in [shadow_non_tls_array, trojan_non_tls_array, vmess_non_tls_array, vless_non_tls_array, reality_non_tls_array]:
        non_tls_array.extend(array)
    for array in [shadow_tcp_array, trojan_tcp_array, vmess_tcp_array, vless_tcp_array, reality_tcp_array]:
        tcp_array.extend(array)
    for array in [shadow_ws_array, trojan_ws_array, vmess_ws_array, vless_ws_array, reality_ws_array]:
        ws_array.extend(array)
    for array in [shadow_http_array, trojan_http_array, vmess_http_array, vless_http_array, reality_http_array]:
        http_array.extend(array)
    for array in [shadow_grpc_array, trojan_grpc_array, vmess_grpc_array, vless_grpc_array, reality_grpc_array]:
        grpc_array.extend(array)

    return shadow_array, trojan_array, vmess_array, vless_array, reality_array, tuic_array, hysteria_array, tls_array, non_tls_array, tcp_array, ws_array, http_array, grpc_array


def find_matches(text_content):
    pattern_telegram_user = r"(?:@)(\w{4,})"
    pattern_url = r"(?i)\bhttps?://[^\s<>()]+"
    pattern_shadowsocks = r"(?<![\w-])(ss://[^\s<>#]+)"
    pattern_trojan = r"(?<![\w-])(trojan://[^\s<>#]+)"
    pattern_vmess = r"(?<![\w-])(vmess://[^\s<>#]+)"
    pattern_vless = r"(?<![\w-])(vless://(?:(?!=reality)[^\s<>#])+(?=[\s<>#]))"
    pattern_reality = r"(?<![\w-])(vless://[^\s<>#]+?security=reality[^\s<>#]*)"
    pattern_tuic = r"(?<![\w-])(tuic://[^\s<>#]+)"
    pattern_hysteria = r"(?<![\w-])(hysteria://[^\s<>#]+)"
    pattern_hysteria_ver2 = r"(?<![\w-])(hy2://[^\s<>#]+)"
    pattern_juicity = r"(?<![\w-])(juicity://[^\s<>#]+)"

    matches_usersname = re.findall(pattern_telegram_user, text_content, re.IGNORECASE)
    matches_url = re.findall(pattern_url, text_content, re.IGNORECASE)
    matches_shadowsocks = re.findall(pattern_shadowsocks, text_content, re.IGNORECASE)
    matches_trojan = re.findall(pattern_trojan, text_content, re.IGNORECASE)
    matches_vmess = re.findall(pattern_vmess, text_content, re.IGNORECASE)
    matches_vless = re.findall(pattern_vless, text_content, re.IGNORECASE)
    matches_reality = re.findall(pattern_reality, text_content, re.IGNORECASE)
    matches_tuic = re.findall(pattern_tuic, text_content)
    matches_hysteria = re.findall(pattern_hysteria, text_content)
    matches_hysteria_ver2 = re.findall(pattern_hysteria_ver2, text_content)
    matches_juicity = re.findall(pattern_juicity, text_content)
    matches_hysteria.extend(matches_hysteria_ver2)
    return matches_usersname, matches_url, matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria, matches_juicity


def run(telegram_channels_path="telegram channels.json", invalid_channels_path="invalid telegram channels.json"):
    telegram_channels = json_load(telegram_channels_path)
    channel_messages_array = list()
    removed_channel_array = list()
    channel_check_messages_array = list()

    channel_check_messages_array, removed_channel_array = fetch_channels_batch(
        telegram_channels,
        invalid_channels=set(),
        max_workers=5,
    )

    current_datetime_update = datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
    last_update_datetime = current_datetime_update - timedelta(days=1)
    for channel_user, div_messages in channel_check_messages_array:
        for div_message in div_messages:
            datetime_object, _, _ = tg_message_time(div_message)
            if datetime_object > last_update_datetime:
                channel_messages_array.append((channel_user, div_message))

    array_usernames = list()
    array_url = list()
    array_shadowsocks = list()
    array_trojan = list()
    array_vmess = list()
    array_vless = list()
    array_reality = list()
    array_tuic = list()
    array_hysteria = list()
    array_juicity = list()

    for _, message in channel_messages_array:
        try:
            url_text_content = tg_message_text(message, "url")
            config_text_content = tg_message_text(message, "config")
            matches_username, matches_url, _, _, _, _, _, _, _, _ = find_matches(url_text_content)
            _, _, matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria, matches_juicity = find_matches(config_text_content)
            array_usernames.extend([element.lower() for element in matches_username if len(element) >= 5])
            array_url.extend(matches_url)
            array_shadowsocks.extend(matches_shadowsocks)
            array_trojan.extend(matches_trojan)
            array_vmess.extend(matches_vmess)
            array_vless.extend(matches_vless)
            array_reality.extend(matches_reality)
            array_tuic.extend(matches_tuic)
            array_hysteria.extend(matches_hysteria)
            array_juicity.extend(matches_juicity)
        except Exception:
            continue

    invalid_array_channels = set(json_load(invalid_channels_path)) if Path(invalid_channels_path).exists() else set()
    new_telegram_channels = set(array_usernames).difference(telegram_channels)
    new_channel_messages, removed_new_channels = fetch_channels_batch(
        new_telegram_channels,
        invalid_channels=invalid_array_channels,
        max_workers=5,
    )
    removed_channel_array.extend(removed_new_channels)

    return {
        "telegram_channels": telegram_channels,
        "channel_check_messages_array": channel_check_messages_array,
        "channel_messages_array": channel_messages_array,
        "removed_channel_array": removed_channel_array,
        "new_channel_messages": new_channel_messages,
        "array_usernames": array_usernames,
        "array_url": array_url,
        "array_shadowsocks": array_shadowsocks,
        "array_trojan": array_trojan,
        "array_vmess": array_vmess,
        "array_vless": array_vless,
        "array_reality": array_reality,
        "array_tuic": array_tuic,
        "array_hysteria": array_hysteria,
        "array_juicity": array_juicity,
        "current_datetime_update": current_datetime_update,
        "last_update_datetime": last_update_datetime,
    }


def build_subscription_state(
    scrape_state,
    invalid_array_channels=None,
    subscription_links_path="subscription links.json",
    check_port_connection=True,
):
    invalid_array_channels = set(invalid_array_channels or [])
    channel_check_messages_array = scrape_state["channel_check_messages_array"]
    telegram_channels_list = scrape_state["telegram_channels"]
    removed_channel_array = list(scrape_state.get("removed_channel_array", []))

    channel_without_config = set()
    for channel_user, messages in channel_check_messages_array:
        total_config = 0
        for message in messages:
            try:
                url_text_content = tg_message_text(message, "url")
                config_text_content = tg_message_text(message, "config")
                matches_username, matches_url, _, _, _, _, _, _, _, _ = find_matches(url_text_content)
                _, _, matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria, matches_juicity = find_matches(config_text_content)
                total_config += len(matches_shadowsocks) + len(matches_trojan) + len(matches_vmess) + len(matches_vless) + len(matches_reality) + len(matches_tuic) + len(matches_hysteria) + len(matches_juicity)
            except Exception:
                continue
        if total_config == 0:
            channel_without_config.add(channel_user)

    tg_username_list = set()
    url_subscription_links = set()
    for channel_user, messages in channel_check_messages_array:
        for message in messages:
            try:
                url_text_content = tg_message_text(message, "url")
                config_text_content = tg_message_text(message, "config")
                matches_username, matches_url, _, _, _, _, _, _, _, _ = find_matches(url_text_content)
                _, _, matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria, matches_juicity = find_matches(config_text_content)
                for url in matches_url:
                    try:
                        tg_user = tg_username_extract(url)
                        if tg_user not in ["proxy", "img", "emoji", "joinchat"] and "+" not in tg_user and "-" not in tg_user and len(tg_user) >= 5:
                            tg_user = "".join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + "_"])
                            tg_username_list.add(tg_user.lower())
                    except Exception:
                        url_subscription_links.add(url.split("\"")[0])
                        continue
                for element in [element.lower() for element in matches_username if len(element) >= 5]:
                    tg_username_list.add(element)
                for element in matches_shadowsocks + matches_trojan + matches_vmess + matches_vless + matches_reality + matches_tuic + matches_hysteria + matches_juicity:
                    pass
            except Exception:
                continue

    telegram_channels_path = Path("telegram channels.json")
    if telegram_channels_path.exists():
        telegram_channels_list = json_load(telegram_channels_path)
    else:
        telegram_channels_list = []

    new_telegram_channels = tg_username_list.difference(telegram_channels_list)
    new_channel_messages, removed_new_channels = fetch_channels_batch(
        new_telegram_channels,
        invalid_channels=invalid_array_channels,
        max_workers=5,
    )

    current_datetime_update = datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
    last_update_datetime = current_datetime_update - timedelta(days=1)

    new_array_shadowsocks = []
    new_array_trojan = []
    new_array_vmess = []
    new_array_vless = []
    new_array_reality = []
    new_array_tuic = []
    new_array_hysteria = []
    new_array_juicity = []
    new_array_channels = set()

    for channel, messages in new_channel_messages:
        total_config = 0
        new_array_url = set()
        new_array_usernames = set()
        for message in messages:
            try:
                url_text_content = tg_message_text(message, "url")
                config_text_content = tg_message_text(message, "config")
                matches_username, matches_url, _, _, _, _, _, _, _, _ = find_matches(url_text_content)
                _, _, matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria, matches_juicity = find_matches(config_text_content)
                total_config += len(matches_shadowsocks) + len(matches_trojan) + len(matches_vmess) + len(matches_vless) + len(matches_reality) + len(matches_tuic) + len(matches_hysteria) + len(matches_juicity)
                new_array_usernames.update([element.lower() for element in matches_username if len(element) >= 5])
                new_array_url.update(matches_url)
                new_array_shadowsocks.extend(matches_shadowsocks)
                new_array_trojan.extend(matches_trojan)
                new_array_vmess.extend(matches_vmess)
                new_array_vless.extend(matches_vless)
                new_array_reality.extend(matches_reality)
                new_array_tuic.extend(matches_tuic)
                new_array_hysteria.extend(matches_hysteria)
                new_array_juicity.extend(matches_juicity)
            except Exception:
                continue
        if total_config != 0:
            new_array_channels.add(channel)

        tg_username_list_new = set()
        for url in new_array_url:
            try:
                tg_user = tg_username_extract(url)
                if tg_user not in ["proxy", "img", "emoji", "joinchat"] and "+" not in tg_user and "-" not in tg_user and len(tg_user) >= 5:
                    tg_user = "".join([element for element in list(tg_user) if element in string.ascii_letters + string.digits + "_"])
                    tg_username_list_new.add(tg_user.lower())
            except Exception:
                url_subscription_links.add(url.split("\"")[0])
                continue

        tg_username_list_new.update([element.lower() for element in new_array_usernames])
        tg_username_list_new = tg_username_list_new.difference(telegram_channels_list)
        tg_username_list_new = tg_username_list_new.difference(new_telegram_channels)
        tg_username_list_new = tg_username_list_new.difference(set(map(lambda element: element[0], new_channel_messages)))
        _discard_messages, removed_probe = fetch_channels_batch(
            tg_username_list_new,
            invalid_channels=invalid_array_channels,
            max_workers=5,
        )
        removed_channel_array.extend(removed_probe)

    subscription_links = json_load(subscription_links_path)
    subscription_links.extend(list(new_subscription_links := set()))
    subscription_links = sorted(list(set(subscription_links)))

    array_links_content = []
    raw_array_links_content = []
    channel_array_links_content = []
    for url_link in subscription_links:
        try:
            links_content = html_content(url_link)
            array_links_content.append((url_link, links_content))
            if "soroushmirzaei" not in url_link:
                raw_array_links_content.append((url_link, links_content))
            elif "soroushmirzaei" in url_link and "channels" in url_link:
                channel_array_links_content.append((url_link, links_content))
        except Exception:
            continue

    decoded_contents = list(map(lambda element: (element[0], decode_string(element[1])), array_links_content))
    raw_decoded_contents = list(map(lambda element: (element[0], decode_string(element[1])), raw_array_links_content))
    channel_decoded_contents = list(map(lambda element: (element[0], decode_string(element[1])), channel_array_links_content))

    def _split_clean(decoded_pairs):
        result = []
        for url_link, content in decoded_pairs:
            try:
                link_contents = content.splitlines()
                link_contents = [element for element in link_contents if element not in ["\n", "\t", ""]]
                for index, element in enumerate(link_contents):
                    link_contents[index] = re.sub(r"#[^#]+$", "", element)
                result.append((url_link, link_contents))
            except Exception:
                continue
        return result

    array_links_content_decoded = _split_clean(decoded_contents)
    raw_array_links_content_decoded = _split_clean(raw_decoded_contents)
    channel_array_links_content_decoded = _split_clean(channel_decoded_contents)

    matches_usernames = []
    matches_url = []
    matches_shadowsocks = []
    matches_trojan = []
    matches_vmess = []
    matches_vless = []
    matches_reality = []
    matches_tuic = []
    matches_hysteria = []
    matches_juicity = []

    raw_matches_usernames = []
    raw_matches_url = []
    raw_matches_shadowsocks = []
    raw_matches_trojan = []
    raw_matches_vmess = []
    raw_matches_vless = []
    raw_matches_reality = []
    raw_matches_tuic = []
    raw_matches_hysteria = []
    raw_matches_juicity = []

    channel_matches_usernames = []
    channel_matches_url = []
    channel_matches_shadowsocks = []
    channel_matches_trojan = []
    channel_matches_vmess = []
    channel_matches_vless = []
    channel_matches_reality = []
    channel_matches_tuic = []
    channel_matches_hysteria = []
    channel_matches_juicity = []

    new_subscription_urls = set()
    for _, content in array_links_content_decoded:
        content_merged = "\n".join(content)
        match_user, match_url, match_socks, match_trojan, match_vmess, match_vless, match_reality, match_tuic, match_hysteria, match_juicity = find_matches(content_merged)
        if len(match_socks) + len(match_trojan) + len(match_vmess) + len(match_vless) + len(match_reality) + len(match_tuic) + len(match_hysteria) + len(match_juicity) != 0:
            new_subscription_urls.add(_)
        matches_usernames.extend(match_user)
        matches_url.extend(match_url)
        matches_shadowsocks.extend(match_socks)
        matches_trojan.extend(match_trojan)
        matches_vmess.extend(match_vmess)
        matches_vless.extend(match_vless)
        matches_reality.extend(match_reality)
        matches_tuic.extend(match_tuic)
        matches_hysteria.extend(match_hysteria)
        matches_juicity.extend(match_juicity)

    for _, content in raw_array_links_content_decoded:
        raw_content_merged = "\n".join(content)
        match_user, match_url, match_socks, match_trojan, match_vmess, match_vless, match_reality, match_tuic, match_hysteria, match_juicity = find_matches(raw_content_merged)
        raw_matches_usernames.extend(match_user)
        raw_matches_url.extend(match_url)
        raw_matches_shadowsocks.extend(match_socks)
        raw_matches_trojan.extend(match_trojan)
        raw_matches_vmess.extend(match_vmess)
        raw_matches_vless.extend(match_vless)
        raw_matches_reality.extend(match_reality)
        raw_matches_tuic.extend(match_tuic)
        raw_matches_hysteria.extend(match_hysteria)
        raw_matches_juicity.extend(match_juicity)

    for _, content in channel_array_links_content_decoded:
        raw_content_merged = "\n".join(content)
        match_user, match_url, match_socks, match_trojan, match_vmess, match_vless, match_reality, match_tuic, match_hysteria, match_juicity = find_matches(raw_content_merged)
        channel_matches_usernames.extend(match_user)
        channel_matches_url.extend(match_url)
        channel_matches_shadowsocks.extend(match_socks)
        channel_matches_trojan.extend(match_trojan)
        channel_matches_vmess.extend(match_vmess)
        channel_matches_vless.extend(match_vless)
        channel_matches_reality.extend(match_reality)
        channel_matches_tuic.extend(match_tuic)
        channel_matches_hysteria.extend(match_hysteria)
        channel_matches_juicity.extend(match_juicity)

    array_shadowsocks, array_trojan, array_vmess, array_vless, array_reality, array_tuic, array_hysteria, array_juicity = remove_duplicate(
        [item for item in matches_shadowsocks],
        [item for item in matches_trojan],
        [item for item in matches_vmess],
        [item for item in matches_vless],
        [item for item in matches_reality],
        [item for item in matches_tuic],
        [item for item in matches_hysteria],
        [item for item in matches_juicity],
    )
    raw_matches_shadowsocks, raw_matches_trojan, raw_matches_vmess, raw_matches_vless, raw_matches_reality, raw_matches_tuic, raw_matches_hysteria, raw_matches_juicity = remove_duplicate(
        [item for item in raw_matches_shadowsocks],
        [item for item in raw_matches_trojan],
        [item for item in raw_matches_vmess],
        [item for item in raw_matches_vless],
        [item for item in raw_matches_reality],
        [item for item in raw_matches_tuic],
        [item for item in raw_matches_hysteria],
        [item for item in raw_matches_juicity],
    )
    channel_matches_shadowsocks, channel_matches_trojan, channel_matches_vmess, channel_matches_vless, channel_matches_reality, channel_matches_tuic, channel_matches_hysteria, channel_matches_juicity = remove_duplicate(
        [item for item in channel_matches_shadowsocks],
        [item for item in channel_matches_trojan],
        [item for item in channel_matches_vmess],
        [item for item in channel_matches_vless],
        [item for item in channel_matches_reality],
        [item for item in channel_matches_tuic],
        [item for item in channel_matches_hysteria],
        [item for item in channel_matches_juicity],
    )

    array_shadowsocks, array_trojan, array_vmess, array_vless, array_reality, array_tuic, array_hysteria, array_tls, array_non_tls, array_tcp, array_ws, array_http, array_grpc = modify_config(
        array_shadowsocks, array_trojan, array_vmess, array_vless, array_reality, array_tuic, array_hysteria
    )
    matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria, matches_tls, matches_non_tls, matches_tcp, matches_ws, matches_http, matches_grpc = modify_config(
        matches_shadowsocks, matches_trojan, matches_vmess, matches_vless, matches_reality, matches_tuic, matches_hysteria
    )
    raw_matches_shadowsocks, raw_matches_trojan, raw_matches_vmess, raw_matches_vless, raw_matches_reality, raw_matches_tuic, raw_matches_hysteria, raw_matches_tls, raw_matches_non_tls, raw_matches_tcp, raw_matches_ws, raw_matches_http, raw_matches_grpc = modify_config(
        raw_matches_shadowsocks, raw_matches_trojan, raw_matches_vmess, raw_matches_vless, raw_matches_reality, raw_matches_tuic, raw_matches_hysteria, check_port_connection=False
    )
    channel_matches_shadowsocks, channel_matches_trojan, channel_matches_vmess, channel_matches_vless, channel_matches_reality, channel_matches_tuic, channel_matches_hysteria, channel_matches_tls, channel_matches_non_tls, channel_matches_tcp, channel_matches_ws, channel_matches_http, channel_matches_grpc = modify_config(
        channel_matches_shadowsocks, channel_matches_trojan, channel_matches_vmess, channel_matches_vless, channel_matches_reality, channel_matches_tuic, channel_matches_hysteria, check_port_connection=True
    )

    array_shadowsocks_channels = array_shadowsocks + channel_matches_shadowsocks
    array_trojan_channels = array_trojan + channel_matches_trojan
    array_vmess_channels = array_vmess + channel_matches_vmess
    array_vless_channels = array_vless + channel_matches_vless
    array_reality_channels = array_reality + channel_matches_reality
    array_tuic_channels = array_tuic + channel_matches_tuic
    array_hysteria_channels = array_hysteria + channel_matches_hysteria
    array_juicity_channels = array_juicity + channel_matches_juicity

    array_shadowsocks_channels, array_trojan_channels, array_vmess_channels, array_vless_channels, array_reality_channels, array_tuic_channels, array_hysteria_channels, array_juicity_channels = remove_duplicate(
        array_shadowsocks_channels, array_trojan_channels, array_vmess_channels, array_vless_channels, array_reality_channels, array_tuic_channels, array_hysteria_channels, array_juicity_channels, vmess_decode_dedup=False
    )

    array_tls_channels = list(set(array_tls + channel_matches_tls))
    array_non_tls_channels = list(set(array_non_tls + channel_matches_non_tls))
    array_tcp_channels = list(set(array_tcp + channel_matches_tcp))
    array_ws_channels = list(set(array_ws + channel_matches_ws))
    array_http_channels = list(set(array_http + channel_matches_http))
    array_grpc_channels = list(set(array_grpc + channel_matches_grpc))

    array_shadowsocks = list(set(array_shadowsocks + matches_shadowsocks))
    array_trojan = list(set(array_trojan + matches_trojan))
    array_vmess = list(set(array_vmess + matches_vmess))
    array_vless = list(set(array_vless + matches_vless))
    array_reality = list(set(array_reality + matches_reality))
    array_tuic = list(set(array_tuic + matches_tuic))
    array_hysteria = list(set(array_hysteria + matches_hysteria))
    array_juicity = list(set(array_juicity + matches_juicity))

    array_shadowsocks, array_trojan, array_vmess, array_vless, array_reality, array_tuic, array_hysteria, array_juicity = remove_duplicate(
        array_shadowsocks, array_trojan, array_vmess, array_vless, array_reality, array_tuic, array_hysteria, array_juicity, vmess_decode_dedup=False
    )

    array_mixed = array_shadowsocks + array_trojan + array_vmess + array_vless + array_reality
    chunk_size = max(1, math.ceil(len(array_mixed) / 10))
    chunks = [array_mixed[i : i + chunk_size] for i in range(0, len(array_mixed), chunk_size)]

    all_subscription_matches = list(set(matches_shadowsocks + matches_trojan + matches_vmess + matches_vless + matches_reality))
    array_subscription_ipv4, array_subscription_ipv6 = create_internet_protocol(all_subscription_matches)

    all_channel_matches = list(set(array_shadowsocks_channels + array_trojan_channels + array_vmess_channels + array_vless_channels + array_reality_channels))
    array_channel_ipv4, array_channel_ipv6 = create_internet_protocol(all_channel_matches)

    return {
        "channel_without_config": channel_without_config,
        "telegram_channels": telegram_channels_list,
        "new_telegram_channels": new_telegram_channels,
        "new_channel_messages": new_channel_messages,
        "removed_channel_array": removed_channel_array,
        "new_array_channels": new_array_channels,
        "array_shadowsocks": array_shadowsocks,
        "array_trojan": array_trojan,
        "array_vmess": array_vmess,
        "array_vless": array_vless,
        "array_reality": array_reality,
        "array_tuic": array_tuic,
        "array_hysteria": array_hysteria,
        "array_juicity": array_juicity,
        "matches_shadowsocks": matches_shadowsocks,
        "matches_trojan": matches_trojan,
        "matches_vmess": matches_vmess,
        "matches_vless": matches_vless,
        "matches_reality": matches_reality,
        "matches_tuic": matches_tuic,
        "matches_hysteria": matches_hysteria,
        "matches_juicity": matches_juicity,
        "raw_matches_shadowsocks": raw_matches_shadowsocks,
        "raw_matches_trojan": raw_matches_trojan,
        "raw_matches_vmess": raw_matches_vmess,
        "raw_matches_vless": raw_matches_vless,
        "raw_matches_reality": raw_matches_reality,
        "raw_matches_tuic": raw_matches_tuic,
        "raw_matches_hysteria": raw_matches_hysteria,
        "raw_matches_juicity": raw_matches_juicity,
        "raw_matches_tls": raw_matches_tls,
        "raw_matches_non_tls": raw_matches_non_tls,
        "raw_matches_tcp": raw_matches_tcp,
        "raw_matches_ws": raw_matches_ws,
        "raw_matches_http": raw_matches_http,
        "raw_matches_grpc": raw_matches_grpc,
        "channel_matches_shadowsocks": channel_matches_shadowsocks,
        "channel_matches_trojan": channel_matches_trojan,
        "channel_matches_vmess": channel_matches_vmess,
        "channel_matches_vless": channel_matches_vless,
        "channel_matches_reality": channel_matches_reality,
        "channel_matches_tuic": channel_matches_tuic,
        "channel_matches_hysteria": channel_matches_hysteria,
        "channel_matches_juicity": channel_matches_juicity,
        "array_tls": array_tls,
        "array_non_tls": array_non_tls,
        "array_tcp": array_tcp,
        "array_ws": array_ws,
        "array_http": array_http,
        "array_grpc": array_grpc,
        "array_tls_channels": array_tls_channels,
        "array_non_tls_channels": array_non_tls_channels,
        "array_tcp_channels": array_tcp_channels,
        "array_ws_channels": array_ws_channels,
        "array_http_channels": array_http_channels,
        "array_grpc_channels": array_grpc_channels,
        "array_shadowsocks_channels": array_shadowsocks_channels,
        "array_trojan_channels": array_trojan_channels,
        "array_vmess_channels": array_vmess_channels,
        "array_vless_channels": array_vless_channels,
        "array_reality_channels": array_reality_channels,
        "array_tuic_channels": array_tuic_channels,
        "array_hysteria_channels": array_hysteria_channels,
        "array_juicity_channels": array_juicity_channels,
        "array_mixed": array_mixed,
        "chunks": chunks,
        "all_subscription_matches": all_subscription_matches,
        "array_subscription_ipv4": array_subscription_ipv4,
        "array_subscription_ipv6": array_subscription_ipv6,
        "all_channel_matches": all_channel_matches,
        "array_channel_ipv4": array_channel_ipv4,
        "array_channel_ipv6": array_channel_ipv6,
        "current_datetime_update": current_datetime_update,
        "last_update_datetime": last_update_datetime,
    }
