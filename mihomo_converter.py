from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from converter.emitter import dump_yaml
from converter.options import ConvertOptions, ConvertResult
from converter.utils import (
    decode_base64_any,
    dedupe_name,
    normalize_name,
    parse_bool,
    safe_int,
    split_lines,
)


class V2RayToMihomoConverter:
    def convert(self, text: str, options: ConvertOptions | None = None) -> ConvertResult:
        options = options or ConvertOptions()
        warnings: list[str] = []
        errors: list[str] = []

        clash_yaml = self._try_parse_existing_clash(text, options, warnings)
        if clash_yaml is not None:
            return clash_yaml

        decoded = decode_base64_any(text)
        content = decoded if decoded is not None else text
        lines = split_lines(content)

        proxies: list[dict[str, Any]] = []
        seen_names: dict[str, int] = {}
        for line in lines:
            parsed = self._parse_line(line, seen_names, warnings)
            if parsed is None:
                warnings.append(f"unsupported or invalid line skipped: {line[:80]}")
                continue
            proxies.append(parsed)

        if not proxies:
            errors.append("no valid proxies found")
            return self._build_result([], warnings, errors, options)

        return self._build_result(proxies, warnings, errors, options)

    def normalize_proxy(self, proxy: dict[str, Any]) -> dict[str, Any] | None:
        server = str(proxy.get("server") or "")
        name = str(proxy.get("name") or "").strip()
        if not name:
            return None
        if not server:
            return None
        if server in {"127.0.0.1", "localhost", "::1"}:
            return None
        if any(token in name.lower() for token in ("latest-update", "telegram-channel", "developed-by", "donating")):
            return None
        return proxy

    def _try_parse_existing_clash(
        self, text: str, options: ConvertOptions, warnings: list[str]
    ) -> ConvertResult | None:
        data = self._parse_simple_clash_yaml(text)
        if data is None:
            return None
        if not isinstance(data, dict) or "proxies" not in data:
            return None
        proxies = data.get("proxies")
        if not isinstance(proxies, list):
            return None
        normalized: list[dict[str, Any]] = []
        for item in proxies:
            if isinstance(item, dict) and item.get("name") and item.get("type"):
                cleaned = self.normalize_proxy(item)
                if cleaned is not None:
                    normalized.append(cleaned)
        if not normalized:
            return None
        return self._build_result(normalized, warnings, [], options)

    def _parse_simple_clash_yaml(self, text: str) -> dict[str, Any] | None:
        stripped = text.lstrip()
        if not stripped.startswith("proxies:"):
            return None

        lines = text.splitlines()
        proxies: list[dict[str, Any]] = []
        current: dict[str, Any] | None = None

        def commit() -> None:
            nonlocal current
            if current:
                proxies.append(current)
            current = None

        for raw in lines:
            line = raw.rstrip()
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            if line.startswith("proxies:"):
                continue
            if re.match(r"^\s*-\s+", line):
                commit()
                current = {}
                remainder = re.sub(r"^\s*-\s+", "", line)
                if ":" in remainder:
                    key, _, value = remainder.partition(":")
                    current[key.strip()] = value.strip().strip('"\'')
                continue
            if current is None:
                continue
            if ":" in line:
                key, _, value = line.strip().partition(":")
                current[key.strip()] = value.strip().strip('"\'')

        commit()
        return {"proxies": proxies}

    def _build_result(
        self,
        proxies: list[dict[str, Any]],
        warnings: list[str],
        errors: list[str],
        options: ConvertOptions,
    ) -> ConvertResult:
        proxy_names = [proxy["name"] for proxy in proxies if proxy.get("name")]
        document: dict[str, Any] = {
            "mixed-port": 7890,
            "allow-lan": False,
            "mode": "rule",
            "log-level": "info",
            "proxies": proxies,
            "proxy-groups": [
                {
                    "name": "Proxy-Select",
                    "type": "select",
                    "proxies": [
                        "Auto-Lowest-Delay",
                        "Load-Balance",
                        "DIRECT",
                        *proxy_names,
                    ],
                },
                {
                    "name": "Auto-Lowest-Delay",
                    "type": "url-test",
                    "url": options.test_url,
                    "interval": options.auto_interval,
                    "lazy": False,
                    "timeout": 5000,
                    "max-failed-times": 3,
                    "tolerance": options.auto_tolerance,
                    "proxies": proxy_names,
                },
                {
                    "name": "Load-Balance",
                    "type": "load-balance",
                    "url": options.test_url,
                    "interval": options.load_balance_interval,
                    "lazy": False,
                    "timeout": 5000,
                    "max-failed-times": 3,
                    "strategy": options.load_balance_strategy,
                    "proxies": proxy_names,
                },
            ],
            "rules": [],
        }
        if options.prepend_app_rules:
            document["rules"].extend(options.app_rules)
        document["rules"].append("MATCH,DIRECT")

        yaml_text = dump_yaml(document)
        return ConvertResult(yaml=yaml_text, proxies=proxies, warnings=warnings, errors=errors)

    def _parse_line(
        self,
        line: str,
        seen_names: dict[str, int],
        warnings: list[str],
    ) -> dict[str, Any] | None:
        if "://" not in line:
            return None
        scheme = line.split("://", 1)[0].lower()
        try:
            if scheme == "vmess":
                return self._parse_vmess(line, seen_names)
            if scheme == "vless":
                return self._parse_vless(line, seen_names)
            if scheme == "trojan":
                return self._parse_trojan(line, seen_names)
            if scheme == "ss":
                return self._parse_ss(line, seen_names)
            if scheme in {"socks5", "socks"}:
                return self._parse_socks_http(line, seen_names, "socks5")
            if scheme == "http":
                return self._parse_socks_http(line, seen_names, "http")
            if scheme in {"hysteria", "hysteria2", "hy2"}:
                return self._parse_hysteria(line, seen_names, scheme)
            if scheme == "tuic":
                return self._parse_tuic(line, seen_names)
            if scheme == "juicity":
                return self._parse_juicity(line, seen_names)
        except Exception as exc:
            warnings.append(f"{scheme} parse failed: {exc}")
            return None
        return None

    def _parse_vmess(self, line: str, seen_names: dict[str, int]) -> dict[str, Any]:
        payload = line.removeprefix("vmess://")
        decoded = decode_base64_any(payload)
        if decoded is not None:
            data = json.loads(decoded)
            if not isinstance(data, dict):
                raise ValueError("vmess payload must be a json object")

            name = dedupe_name(normalize_name(data.get("ps"), "VMess"), seen_names)
            net = str(data.get("net") or "tcp").lower()
            proxy = {
                "name": name,
                "type": "vmess",
                "server": str(data.get("add") or ""),
                "port": safe_int(data.get("port"), 0) or 0,
                "uuid": str(data.get("id") or ""),
                "alterId": safe_int(data.get("aid"), 0) or 0,
                "cipher": str(data.get("scy") or "auto"),
                "udp": True,
                "network": net,
            }
            if str(data.get("tls") or "").lower() in {"1", "true", "tls"}:
                proxy["tls"] = True
            if sni := data.get("sni"):
                proxy["servername"] = sni
            elif host := data.get("host"):
                proxy["servername"] = host
            if fp := data.get("fp"):
                proxy["client-fingerprint"] = fp

            host = data.get("host")
            path = data.get("path")
            if net == "ws":
                ws_opts: dict[str, Any] = {"path": path or "/"}
                if host:
                    ws_opts["headers"] = {"Host": host}
                proxy["ws-opts"] = ws_opts
            elif net == "grpc":
                proxy["grpc-opts"] = {"grpc-service-name": path or ""}
            elif net == "h2":
                h2_opts: dict[str, Any] = {"path": [path or "/"]}
                if host:
                    h2_opts["host"] = [host]
                proxy["h2-opts"] = h2_opts
            elif net == "http":
                proxy["http-opts"] = {"path": [path or "/"], "headers": {"Host": [host]} if host else {}}

            return proxy

        url = urlparse(line)
        if not url.hostname or not url.port or not url.username:
            raise ValueError("invalid vmess link")
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        name = dedupe_name(normalize_name(unquote(url.fragment), "VMess"), seen_names)
        net = (query.get("net") or query.get("type") or "tcp").lower()
        proxy = {
            "name": name,
            "type": "vmess",
            "server": url.hostname,
            "port": url.port,
            "uuid": url.username,
            "alterId": safe_int(query.get("aid"), 0) or 0,
            "cipher": query.get("scy") or "auto",
            "udp": True,
            "network": net,
        }
        if (query.get("tls") or "").lower() in {"1", "true", "tls"}:
            proxy["tls"] = True
        if sni := query.get("sni") or query.get("host"):
            proxy["servername"] = sni
        if fp := query.get("fp"):
            proxy["client-fingerprint"] = fp
        if net == "ws":
            proxy["ws-opts"] = {
                "path": query.get("path") or "/",
                "headers": {"Host": query.get("host")} if query.get("host") else {},
            }
        elif net == "grpc":
            proxy["grpc-opts"] = {"grpc-service-name": query.get("path") or query.get("serviceName") or ""}
        elif net == "h2":
            proxy["h2-opts"] = {
                "path": [query.get("path") or "/"],
                "host": [query.get("host")] if query.get("host") else None,
            }
        elif net == "http":
            proxy["http-opts"] = {
                "path": [query.get("path") or "/"],
                "headers": {"Host": [query.get("host")]} if query.get("host") else {},
            }
        return {k: v for k, v in proxy.items() if v not in (None, [], "")}

    def _parse_vless(self, line: str, seen_names: dict[str, int]) -> dict[str, Any]:
        url = urlparse(line)
        if not url.hostname or not url.port or not url.username:
            raise ValueError("invalid vless link")
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        name = dedupe_name(normalize_name(unquote(url.fragment), "VLESS"), seen_names)
        network = (query.get("type") or "tcp").lower()
        proxy: dict[str, Any] = {
            "name": name,
            "type": "vless",
            "server": url.hostname,
            "port": url.port,
            "uuid": url.username,
            "udp": True,
            "network": network,
        }
        security = (query.get("security") or "").lower()
        if security in {"tls", "reality"}:
            proxy["tls"] = True
        if sni := query.get("sni"):
            proxy["servername"] = sni
        if fp := query.get("fp"):
            proxy["client-fingerprint"] = fp
        if flow := query.get("flow"):
            proxy["flow"] = flow
        if packet := query.get("packetEncoding"):
            proxy["packet-encoding"] = packet
        if network == "ws":
            ws_opts: dict[str, Any] = {"path": query.get("path") or "/"}
            if host := query.get("host"):
                ws_opts["headers"] = {"Host": host}
            proxy["ws-opts"] = ws_opts
        elif network == "grpc":
            proxy["grpc-opts"] = {"grpc-service-name": query.get("serviceName") or ""}
        elif network == "xhttp":
            proxy["xhttp-opts"] = {
                "path": query.get("path") or "/",
                "host": query.get("host"),
                "mode": query.get("mode"),
            }
        elif network == "h2":
            proxy["h2-opts"] = {
                "path": [query.get("path") or "/"],
                "host": [query.get("host")] if query.get("host") else None,
            }
        if security == "reality":
            proxy["reality-opts"] = {
                "public-key": query.get("pbk"),
                "short-id": query.get("sid"),
            }
        return {k: v for k, v in proxy.items() if v not in (None, [], "")}

    def _parse_trojan(self, line: str, seen_names: dict[str, int]) -> dict[str, Any]:
        url = urlparse(line)
        if not url.hostname or not url.port or not url.username:
            raise ValueError("invalid trojan link")
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        name = dedupe_name(normalize_name(unquote(url.fragment), "Trojan"), seen_names)
        proxy: dict[str, Any] = {
            "name": name,
            "type": "trojan",
            "server": url.hostname,
            "port": url.port,
            "password": url.username,
            "udp": True,
        }
        if sni := query.get("sni") or query.get("peer") or query.get("host"):
            proxy["sni"] = sni
            proxy["servername"] = sni
        if alpn := query.get("alpn"):
            proxy["alpn"] = [item for item in alpn.split(",") if item]
        network = (query.get("type") or "tcp").lower()
        proxy["network"] = network
        if network == "ws":
            proxy["ws-opts"] = {
                "path": query.get("path") or "/",
                "headers": {"Host": query.get("host")} if query.get("host") else {},
            }
        elif network == "grpc":
            proxy["grpc-opts"] = {"grpc-service-name": query.get("serviceName") or ""}
        if fp := query.get("fp"):
            proxy["client-fingerprint"] = fp
        return {k: v for k, v in proxy.items() if v not in (None, [], "")}

    def _parse_ss(self, line: str, seen_names: dict[str, int]) -> dict[str, Any]:
        url = urlparse(line)
        if not url.hostname:
            raise ValueError("invalid shadowsocks link")
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        if url.username and url.password is not None:
            method, password = url.username, url.password
        else:
            encoded = url.netloc.rsplit("@", 1)[0]
            decoded = _decode_base64_any(encoded)
            if decoded is None or ":" not in decoded:
                raise ValueError("invalid shadowsocks credentials")
            method, password = decoded.split(":", 1)
        name = _dedupe_name(_normalize_name(unquote(url.fragment), "SS"), seen_names)
        proxy: dict[str, Any] = {
            "name": name,
            "type": "ss",
            "server": url.hostname,
            "port": url.port or 0,
            "cipher": method,
            "password": password,
            "udp": True,
        }
        if plugin := query.get("plugin"):
            proxy["plugin"] = plugin
        if query.get("udp-over-tcp") == "true" or query.get("uot") == "1":
            proxy["udp-over-tcp"] = True
        return proxy

    def _parse_socks_http(self, line: str, seen_names: dict[str, int], scheme: str) -> dict[str, Any]:
        url = urlparse(line)
        if not url.hostname or not url.port:
            raise ValueError(f"invalid {scheme} link")
        name = dedupe_name(normalize_name(unquote(url.fragment), scheme.upper()), seen_names)
        proxy: dict[str, Any] = {
            "name": name,
            "type": scheme,
            "server": url.hostname,
            "port": url.port,
        }
        if url.username:
            proxy["username"] = url.username
        if url.password:
            proxy["password"] = url.password
        return proxy

    def _parse_hysteria(self, line: str, seen_names: dict[str, int], scheme: str) -> dict[str, Any]:
        url = urlparse(line)
        if not url.hostname or not url.port:
            raise ValueError("invalid hysteria link")
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        name = dedupe_name(normalize_name(unquote(url.fragment), scheme.upper()), seen_names)
        proxy: dict[str, Any] = {
            "name": name,
            "type": "hysteria2" if scheme in {"hysteria2", "hy2"} else "hysteria",
            "server": url.hostname,
            "port": url.port,
            "udp": True,
        }
        if scheme in {"hysteria2", "hy2"}:
            proxy["password"] = url.username or query.get("auth") or ""
            if sni := query.get("sni") or query.get("peer") or query.get("host"):
                proxy["sni"] = sni
            if alpn := query.get("alpn"):
                proxy["alpn"] = [item for item in alpn.split(",") if item]
            if fp := query.get("fp"):
                proxy["client-fingerprint"] = fp
            if obfs := query.get("obfs"):
                proxy["obfs"] = obfs
            if obfs_password := query.get("obfs-password") or query.get("obfs_password"):
                proxy["obfs-password"] = obfs_password
            if query.get("allowInsecure", query.get("allowinsecure", "0")).lower() in {"1", "true", "yes"}:
                proxy["skip-cert-verify"] = True
        else:
            proxy["auth-str"] = query.get("auth") or query.get("auth-str") or query.get("auth_str") or ""
            if sni := query.get("sni") or query.get("peer") or query.get("host"):
                proxy["sni"] = sni
            if alpn := query.get("alpn"):
                proxy["alpn"] = [item for item in alpn.split(",") if item]
            if obfs := query.get("obfs"):
                proxy["obfs"] = obfs
            if obfs_password := query.get("obfs-password") or query.get("obfs_password"):
                proxy["obfs-password"] = obfs_password
            if query.get("allowInsecure", query.get("allowinsecure", "0")).lower() in {"1", "true", "yes"}:
                proxy["skip-cert-verify"] = True
        return {k: v for k, v in proxy.items() if v not in (None, [], "")}

    def _parse_tuic(self, line: str, seen_names: dict[str, int]) -> dict[str, Any]:
        url = urlparse(line)
        if not url.hostname or not url.port:
            raise ValueError("invalid tuic link")
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        name = dedupe_name(normalize_name(unquote(url.fragment), "TUIC"), seen_names)
        proxy: dict[str, Any] = {
            "name": name,
            "type": "tuic",
            "server": url.hostname,
            "port": url.port,
            "uuid": url.username or "",
            "password": url.password or query.get("password") or "",
            "udp": True,
        }
        if sni := query.get("sni") or query.get("peer") or query.get("host"):
            proxy["sni"] = sni
        if alpn := query.get("alpn"):
            proxy["alpn"] = [item for item in alpn.split(",") if item]
        if query.get("allowInsecure", query.get("allowinsecure", "0")).lower() in {"1", "true", "yes"}:
            proxy["skip-cert-verify"] = True
        if query.get("disable-sni", query.get("disable_sni", "0")).lower() in {"1", "true", "yes"}:
            proxy["disable-sni"] = True
        if query.get("reduce-rtt", query.get("reduce_rtt", "0")).lower() in {"1", "true", "yes"}:
            proxy["reduce-rtt"] = True
        if controller := query.get("congestion-controller") or query.get("congestion_controller"):
            proxy["congestion-controller"] = controller
        return {k: v for k, v in proxy.items() if v not in (None, [], "")}

    def _parse_juicity(self, line: str, seen_names: dict[str, int]) -> dict[str, Any]:
        url = urlparse(line)
        if not url.hostname or not url.port:
            raise ValueError("invalid juicity link")
        query = {k: v[0] for k, v in parse_qs(url.query, keep_blank_values=True).items()}
        name = _dedupe_name(_normalize_name(unquote(url.fragment), "Juicity"), seen_names)
        proxy: dict[str, Any] = {
            "name": name,
            "type": "juicity",
            "server": url.hostname,
            "port": url.port,
            "password": url.username or "",
            "udp": True,
        }
        if sni := query.get("sni") or query.get("peer") or query.get("host"):
            proxy["sni"] = sni
        if alpn := query.get("alpn"):
            proxy["alpn"] = [item for item in alpn.split(",") if item]
        if query.get("allowInsecure", query.get("allowinsecure", "0")).lower() in {"1", "true", "yes"}:
            proxy["skip-cert-verify"] = True
        if controller := query.get("congestion-controller") or query.get("congestion_controller"):
            proxy["congestion-controller"] = controller
        return {k: v for k, v in proxy.items() if v not in (None, [], "")}


def convertV2RaySubscriptionToMihomoConfig(
    input_text: str, options: ConvertOptions | None = None
) -> ConvertResult:
    return V2RayToMihomoConverter().convert(input_text, options)


def convert_v2ray_subscription_to_mihomo_config(
    input_text: str, options: ConvertOptions | None = None
) -> ConvertResult:
    return convertV2RaySubscriptionToMihomoConfig(input_text, options)


def main(argv: list[str] | None = None) -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog="convert-v2ray")
    parser.add_argument("--input", required=True, help="input subscription file")
    parser.add_argument("--output", required=True, help="output Clash/Mihomo YAML file")
    parser.add_argument("--prepend-app-rules", action="store_true", help="prepend app process rules")
    args = parser.parse_args(argv)

    text = Path(args.input).read_text(encoding="utf-8")
    result = convertV2RaySubscriptionToMihomoConfig(
        text, ConvertOptions(prepend_app_rules=args.prepend_app_rules)
    )
    Path(args.output).write_text(result.yaml, encoding="utf-8")
    if result.warnings:
        print("\n".join(result.warnings), file=sys.stderr)
    if result.errors:
        print("\n".join(result.errors), file=sys.stderr)
    return 0 if not result.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
