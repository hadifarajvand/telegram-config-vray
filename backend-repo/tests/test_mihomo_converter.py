from __future__ import annotations

import base64
import json
import subprocess

from mihomo_converter import ConvertOptions, convertV2RaySubscriptionToMihomoConfig

try:
    import yaml
except Exception:  # pragma: no cover
    yaml = None


def _load_config(text: str) -> dict:
    # Backward-compatible parser for either JSON-shaped YAML or real YAML.
    try:
        data = json.loads(text)
    except Exception:
        if yaml is not None:
            data = yaml.safe_load(text)
        else:
            ruby = subprocess.run(
                [
                    "ruby",
                    "-ryaml",
                    "-rjson",
                    "-e",
                    "doc=YAML.safe_load(ARGF.read); puts JSON.generate(doc)",
                ],
                input=text.encode("utf-8"),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            data = json.loads(ruby.stdout.decode("utf-8"))
    assert isinstance(data, dict)
    return data


def _group_map(doc: dict) -> dict[str, dict]:
    groups = doc.get("proxy-groups", [])
    assert isinstance(groups, list)
    return {g["name"]: g for g in groups if isinstance(g, dict) and "name" in g}


def test_legacy_vmess_base64_json_preserves_ws_opts():
    payload = base64.b64encode(
        json.dumps(
            {
                "v": "2",
                "ps": "VMess WS",
                "add": "example.com",
                "port": "443",
                "id": "11111111-1111-1111-1111-111111111111",
                "aid": "0",
                "scy": "auto",
                "net": "ws",
                "tls": "tls",
                "host": "cdn.example.com",
                "path": "/ray",
                "sni": "example.com",
                "fp": "chrome",
            }
        ).encode()
    ).decode()

    doc = _load_config(convertV2RaySubscriptionToMihomoConfig(f"vmess://{payload}").yaml)
    proxy = doc["proxies"][0]
    assert proxy["type"] == "vmess"
    assert proxy["name"] == "VMess WS"
    assert proxy["ws-opts"]["path"] == "/ray"
    assert proxy["ws-opts"]["headers"]["Host"] == "cdn.example.com"


def test_vless_reality_preserves_key_fields():
    result = convertV2RaySubscriptionToMihomoConfig(
        "vless://11111111-1111-1111-1111-111111111111@example.com:443"
        "?type=tcp&security=reality&flow=xtls-rprx-vision&sni=example.com&fp=chrome"
        "&pbk=PUBLICKEY123&sid=ABCD#Example-VLESS"
    )
    doc = _load_config(result.yaml)
    proxy = doc["proxies"][0]
    assert proxy["type"] == "vless"
    assert proxy["flow"] == "xtls-rprx-vision"
    assert proxy["servername"] == "example.com"
    assert proxy["client-fingerprint"] == "chrome"
    assert proxy["reality-opts"]["public-key"] == "PUBLICKEY123"
    assert proxy["reality-opts"]["short-id"] == "ABCD"


def test_vless_tls_websocket_preserves_host_and_path():
    result = convertV2RaySubscriptionToMihomoConfig(
        "vless://11111111-1111-1111-1111-111111111111@example.com:443"
        "?type=ws&security=tls&path=/ws&host=cdn.example.com&sni=example.com#WS"
    )
    proxy = _load_config(result.yaml)["proxies"][0]
    assert proxy["network"] == "ws"
    assert proxy["tls"] is True
    assert proxy["ws-opts"]["path"] == "/ws"
    assert proxy["ws-opts"]["headers"]["Host"] == "cdn.example.com"


def test_trojan_tls_grpc():
    result = convertV2RaySubscriptionToMihomoConfig(
        "trojan://password@example.com:443?sni=example.com&alpn=h2,http/1.1&type=grpc"
        "&serviceName=svc#Trojan"
    )
    proxy = _load_config(result.yaml)["proxies"][0]
    assert proxy["type"] == "trojan"
    assert proxy["sni"] == "example.com"
    assert proxy["grpc-opts"]["grpc-service-name"] == "svc"


def test_base64_subscription_multiple_links():
    plaintext = "\n".join(
        [
            "vless://11111111-1111-1111-1111-111111111111@example.com:443?type=tcp#One",
            "vmess://"
            + base64.b64encode(
                json.dumps(
                    {
                        "ps": "Two",
                        "add": "two.example.com",
                        "port": "443",
                        "id": "22222222-2222-2222-2222-222222222222",
                        "aid": "0",
                    }
                ).encode()
            ).decode(),
        ]
    )
    encoded = base64.b64encode(plaintext.encode()).decode()
    doc = _load_config(convertV2RaySubscriptionToMihomoConfig(encoded).yaml)
    assert len(doc["proxies"]) == 2


def test_existing_clash_yaml_keeps_proxies_and_has_groups():
    clash = """
proxies:
  - name: Existing
    type: ss
    server: 1.1.1.1
    port: 8388
    cipher: aes-128-gcm
    password: pass
"""
    doc = _load_config(convertV2RaySubscriptionToMihomoConfig(clash).yaml)
    assert doc["proxies"][0]["name"] == "Existing"
    groups = _group_map(doc)
    assert "Proxy-Select" in groups
    assert "Auto-Lowest-Delay" in groups
    assert "Load-Balance" in groups


def test_invalid_lines_are_skipped_not_fatal():
    text = """
invalid-line
vless://11111111-1111-1111-1111-111111111111@example.com:443?type=tcp#Ok
bad://nope
"""
    result = convertV2RaySubscriptionToMihomoConfig(text)
    doc = _load_config(result.yaml)
    assert len(doc["proxies"]) == 1
    assert result.warnings


def test_duplicate_names_deduped_and_present_in_groups():
    text = "\n".join(
        [
            "vless://11111111-1111-1111-1111-111111111111@example.com:443?type=tcp#Same",
            "vless://22222222-2222-2222-2222-222222222222@example.com:443?type=tcp#Same",
        ]
    )
    doc = _load_config(convertV2RaySubscriptionToMihomoConfig(text).yaml)
    names = [p["name"] for p in doc["proxies"]]
    assert names == ["Same", "Same-2"]
    groups = _group_map(doc)
    for group_name in ("Auto-Lowest-Delay", "Load-Balance"):
        for name in names:
            assert name in groups[group_name]["proxies"]


def test_group_structure_and_fallback_rule():
    text = "\n".join(
        [
            "vless://11111111-1111-1111-1111-111111111111@example.com:443?type=tcp#N1",
            "vless://22222222-2222-2222-2222-222222222222@example.com:443?type=tcp#N2",
        ]
    )
    doc = _load_config(convertV2RaySubscriptionToMihomoConfig(text).yaml)
    groups = _group_map(doc)

    assert "Proxy-Select" in groups
    assert groups["Proxy-Select"]["type"] == "select"
    assert "Auto-Lowest-Delay" in groups["Proxy-Select"]["proxies"]
    assert "Load-Balance" in groups["Proxy-Select"]["proxies"]
    assert "DIRECT" in groups["Proxy-Select"]["proxies"]

    assert groups["Auto-Lowest-Delay"]["type"] == "url-test"
    assert groups["Auto-Lowest-Delay"]["interval"] == 600
    assert groups["Auto-Lowest-Delay"]["timeout"] == 5000
    assert groups["Auto-Lowest-Delay"]["tolerance"] == 80
    assert groups["Auto-Lowest-Delay"]["lazy"] is False
    assert groups["Auto-Lowest-Delay"]["max-failed-times"] == 3

    assert groups["Load-Balance"]["type"] == "load-balance"
    assert groups["Load-Balance"]["strategy"] == "round-robin"
    assert groups["Load-Balance"]["interval"] == 600
    assert groups["Load-Balance"]["timeout"] == 5000
    assert groups["Load-Balance"]["lazy"] is False
    assert groups["Load-Balance"]["max-failed-times"] == 3

    assert doc["rules"][-1] == "MATCH,DIRECT"


def test_app_rules_prepended_and_before_fallback():
    result = convertV2RaySubscriptionToMihomoConfig(
        "vless://11111111-1111-1111-1111-111111111111@example.com:443?type=tcp#One",
        ConvertOptions(prepend_app_rules=True),
    )
    rules = _load_config(result.yaml)["rules"]
    assert rules[:5] == [
        "PROCESS-NAME,Cursor,Proxy-Select",
        "PROCESS-NAME,Google Chrome,Proxy-Select",
        "PROCESS-NAME,Google Chrome Helper,Proxy-Select",
        "PROCESS-NAME,Visual Studio Code,Proxy-Select",
        "PROCESS-NAME,Claude,Proxy-Select",
    ]
    assert rules[-1] == "MATCH,DIRECT"
