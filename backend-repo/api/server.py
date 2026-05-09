from __future__ import annotations

import base64
import json
import os
import re
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
HOST = os.environ.get("API_BIND", "0.0.0.0")
PORT = int(os.environ.get("API_PORT", "8888"))
STARTED_AT = time.time()
SOURCE_FILES = [
    ROOT / "main.py",
    ROOT / "mixin.yml",
    ROOT / "layers" / "ipv4",
    ROOT / "layers" / "ipv4-clash-verge.yaml",
    ROOT / "layers" / "ipv6-clash-verge.yaml",
    ROOT / "layers" / "clash.yaml",
    ROOT / "countries" / "nl" / "mixed",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_state(path: Path):
    if not path.exists():
        return {"path": str(path.relative_to(ROOT)), "exists": False}
    stat = path.stat()
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": True,
        "size": stat.st_size,
        "mtime": stat.st_mtime,
    }


def decode_subscription_file(path: Path):
    raw = read_text(path).strip()
    if not raw:
        return []
    try:
        decoded = base64.b64decode(raw + "=" * (-len(raw) % 4)).decode("utf-8", errors="ignore")
    except Exception:
        return []
    return [line.strip() for line in decoded.splitlines() if line.strip()]


def q(query, key, default=""):
    value = query.get(key, [default])
    return value[0] if value else default


def as_bool(value):
    return str(value).lower() in {"1", "true", "yes", "on"}


def proxy_from_config(config: str):
    try:
        parsed = urlparse(config)
        query = parse_qs(parsed.query, keep_blank_values=True)
        name = unquote(parsed.fragment) if parsed.fragment else (parsed.hostname or "Proxy")
        if config.startswith("ss://"):
            match = re.match(r"ss://(?P<rest>[^#]+)(?:#(?P<name>.*))?", config, flags=re.IGNORECASE)
            if not match:
                return None
            rest = match.group("rest")
            name = unquote(match.group("name") or "SS")
            if "@" in rest:
                userinfo, hostpart = rest.rsplit("@", 1)
            else:
                decoded = base64.b64decode(rest + "=" * (-len(rest) % 4)).decode("utf-8", errors="ignore")
                userinfo, hostpart = decoded.split("@", 1)
            method, password = userinfo.split(":", 1)
            server, port = hostpart.rsplit(":", 1)
            return {"name": name, "type": "ss", "server": server.strip("[]"), "port": int(port), "cipher": method, "password": password, "udp": True}
        if config.startswith("trojan://"):
            return {"name": name, "type": "trojan", "server": parsed.hostname, "port": parsed.port, "password": parsed.username or "", "udp": True, "sni": q(query, "sni") or q(query, "peer") or q(query, "host"), "skip-cert-verify": as_bool(q(query, "allowInsecure", q(query, "allowinsecure", "0"))), "network": q(query, "type", "tcp"), "flow": q(query, "flow")}
        if config.startswith("vless://"):
            proxy = {"name": name, "type": "vless", "server": parsed.hostname, "port": parsed.port, "uuid": parsed.username or "", "udp": True, "sni": q(query, "sni") or q(query, "peer") or q(query, "host"), "skip-cert-verify": as_bool(q(query, "allowInsecure", q(query, "allowinsecure", "0"))), "network": q(query, "type", "tcp"), "flow": q(query, "flow"), "client-fingerprint": q(query, "fp")}
            if q(query, "security").lower() == "reality":
                proxy["tls"] = True
                proxy["reality-opts"] = {"public-key": q(query, "pbk"), "short-id": q(query, "sid"), "spider-x": q(query, "spx", "/")}
            elif q(query, "security").lower() in {"tls", "reality"}:
                proxy["tls"] = True
            return proxy
        if config.startswith("vmess://"):
            payload = config.removeprefix("vmess://")
            data = json.loads(base64.b64decode(payload + "=" * (-len(payload) % 4)).decode("utf-8", errors="ignore"))
            return {"name": data.get("ps") or name, "type": "vmess", "server": data.get("add"), "port": int(data.get("port", 0)), "uuid": data.get("id"), "alterId": int(data.get("aid", 0)), "cipher": data.get("scy") or "auto", "udp": True, "network": data.get("net", "tcp"), "tls": bool(data.get("tls")), "servername": data.get("sni") or data.get("host")}
        if config.startswith("tuic://"):
            proxy = {"name": name, "type": "tuic", "server": parsed.hostname, "port": parsed.port, "uuid": parsed.username or "", "password": parsed.password or "", "udp": True, "sni": q(query, "sni") or q(query, "peer") or q(query, "host"), "alpn": [item for item in q(query, "alpn", "").split(",") if item], "skip-cert-verify": as_bool(q(query, "allowInsecure", q(query, "allowinsecure", "0")))}
            if q(query, "congestion-controller"):
                proxy["congestion-controller"] = q(query, "congestion-controller")
            if q(query, "request-timeout").isdigit():
                proxy["request-timeout"] = int(q(query, "request-timeout"))
            return proxy
        if config.startswith("hysteria://"):
            return {"name": name, "type": "hysteria", "server": parsed.hostname, "port": parsed.port, "auth-str": q(query, "auth") or q(query, "auth-str") or q(query, "auth_str") or "", "up": q(query, "up"), "down": q(query, "down"), "sni": q(query, "sni") or q(query, "peer") or q(query, "host"), "alpn": [item for item in q(query, "alpn", "").split(",") if item], "skip-cert-verify": as_bool(q(query, "allowInsecure", q(query, "allowinsecure", "0"))), "obfs": q(query, "obfs"), "obfs-password": q(query, "obfs-password") or q(query, "obfs_password")}
        if config.startswith("hy2://"):
            return {"name": name, "type": "hysteria2", "server": parsed.hostname, "port": parsed.port, "password": parsed.username or "", "udp": True, "sni": q(query, "sni") or q(query, "peer") or q(query, "host"), "alpn": [item for item in q(query, "alpn", "").split(",") if item], "skip-cert-verify": as_bool(q(query, "allowInsecure", q(query, "allowinsecure", "0"))), "obfs": q(query, "obfs"), "obfs-password": q(query, "obfs-password") or q(query, "obfs_password"), "client-fingerprint": q(query, "fp")}
        if config.startswith("juicity://"):
            return {"name": name, "type": "juicity", "server": parsed.hostname, "port": parsed.port, "password": parsed.username or "", "udp": True, "sni": q(query, "sni") or q(query, "peer") or q(query, "host"), "alpn": [item for item in q(query, "alpn", "").split(",") if item], "skip-cert-verify": as_bool(q(query, "allowInsecure", q(query, "allowinsecure", "0")))}
    except Exception:
        return None
    return None


def yaml_scalar(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "":
        return '""'
    if re.fullmatch(r"[A-Za-z0-9_.:/@%+\-]+", text):
        return text
    return "'" + text.replace("'", "''") + "'"


def yaml_lines(value, indent=0):
    prefix = " " * indent
    if isinstance(value, dict):
        if not value:
            return [f"{prefix}{{}}"]
        lines = []
        for key, item in value.items():
            if isinstance(item, dict):
                if item:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: {{}}")
            elif isinstance(item, list):
                if item:
                    lines.append(f"{prefix}{key}:")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}{key}: []")
            else:
                lines.append(f"{prefix}{key}: {yaml_scalar(item)}")
        return lines
    if isinstance(value, list):
        if not value:
            return [f"{prefix}[]"]
        lines = []
        for item in value:
            if isinstance(item, dict):
                if item:
                    lines.append(f"{prefix}-")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}- {{}}")
            elif isinstance(item, list):
                if item:
                    lines.append(f"{prefix}-")
                    lines.extend(yaml_lines(item, indent + 2))
                else:
                    lines.append(f"{prefix}- []")
            else:
                lines.append(f"{prefix}- {yaml_scalar(item)}")
        return lines
    return [f"{prefix}{yaml_scalar(value)}"]


def clash_yaml_from_file(path: Path):
    configs = decode_subscription_file(path)
    proxies = [proxy_from_config(cfg) for cfg in configs]
    proxies = [p for p in proxies if p and p.get("server") and p.get("port")]
    names = [p["name"] for p in proxies if p.get("name")] or ["DIRECT"]
    document = {"mixed-port": 7890, "mode": "rule", "log-level": "info", "ipv6": True, "allow-lan": True, "external-controller": "0.0.0.0:9090", "proxies": proxies, "proxy-groups": [{"name": "Proxy", "type": "select", "proxies": names + ["DIRECT"]}, {"name": "Auto", "type": "url-test", "proxies": names, "url": "https://www.gstatic.com/generate_204", "interval": 300}], "rules": ["MATCH,Proxy"]}
    return "\n".join(yaml_lines(document)) + "\n"


class Handler(BaseHTTPRequestHandler):
    def send_text(self, body, status=200, content_type="text/plain; charset=utf-8"):
        data = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
        print(f"{self.command} {self.path.split('?', 1)[0]} -> {status}", flush=True)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in {"/favicon.ico", "/apple-touch-icon.png", "/apple-touch-icon-precomposed.png"}:
            self.send_text("", status=204)
            return
        if path in {"/", "/health"}:
            self.send_text(json.dumps({
                "status": "ok",
                "uptime_seconds": round(time.time() - STARTED_AT, 3),
                "feeds": {
                    "v2ray_ipv4": "/v2ray/ipv4",
                    "clash_ipv4": "/clash/ipv4",
                    "clash_ipv4_verge": "/clash/ipv4-clash-verge",
                    "clash_ipv6_verge": "/clash/ipv6-clash-verge",
                    "v2ray_nl": "/v2ray/countries/nl/mixed",
                    "clash_nl": "/clash/countries/nl/mixed",
                },
                "source_files": [file_state(path) for path in SOURCE_FILES],
            }, indent=2), content_type="application/json; charset=utf-8")
            return
        if path == "/status":
            self.send_text(json.dumps({
                "status": "ok",
                "endpoint": f"http://{HOST}:{PORT}",
                "source_files": [file_state(path) for path in SOURCE_FILES],
                "feeds": {
                    "v2ray_ipv4": "/v2ray/ipv4",
                    "clash_ipv4": "/clash/ipv4",
                    "clash_ipv4_verge": "/clash/ipv4-clash-verge",
                    "clash_ipv6_verge": "/clash/ipv6-clash-verge",
                    "v2ray_nl": "/v2ray/countries/nl/mixed",
                    "clash_nl": "/clash/countries/nl/mixed",
                },
            }, indent=2), content_type="application/json; charset=utf-8")
            return
        routes = {
            "/v2ray/ipv4": ROOT / "layers" / "ipv4",
            "/v2ray/countries/nl/mixed": ROOT / "countries" / "nl" / "mixed",
            "/clash/ipv4": ROOT / "layers" / "clash.yaml",
            "/clash/ipv4-clash-verge": ROOT / "layers" / "ipv4-clash-verge.yaml",
            "/clash/ipv6-clash-verge": ROOT / "layers" / "ipv6-clash-verge.yaml",
        }
        if path == "/clash/countries/nl/mixed":
            source = ROOT / "countries" / "nl" / "mixed"
            if not source.exists():
                self.send_text("Country feed missing\n", status=404)
                return
            self.send_text(clash_yaml_from_file(source), content_type="text/yaml; charset=utf-8")
            return
        source = routes.get(path)
        if not source or not source.exists():
            self.send_text("Feed missing\n", status=404)
            return
        content_type = "text/yaml; charset=utf-8" if source.name.endswith(".yaml") else "text/plain; charset=utf-8"
        self.send_text(read_text(source), content_type=content_type)

    def log_message(self, fmt, *args):
        return


def main():
    print(f"Serving local API on http://{HOST}:{PORT}", flush=True)
    print("Feeds:", flush=True)
    print("  /health", flush=True)
    print("  /status", flush=True)
    print("  /v2ray/ipv4", flush=True)
    print("  /clash/ipv4", flush=True)
    print("  /clash/ipv4-clash-verge", flush=True)
    print("  /clash/ipv6-clash-verge", flush=True)
    print("  /v2ray/countries/nl/mixed", flush=True)
    print("  /clash/countries/nl/mixed", flush=True)
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.daemon_threads = True
    server.allow_reuse_address = True
    try:
        server.serve_forever()
    except ConnectionResetError:
        pass


if __name__ == "__main__":
    main()
