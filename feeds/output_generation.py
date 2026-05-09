from __future__ import annotations

import base64
from pathlib import Path
from urllib.parse import quote

import jdatetime
from datetime import timezone, timedelta

from converter.mihomo import ConvertOptions, convert_v2ray_subscription_to_mihomo_config
from feeds.clash_verge import build_clash_verge_feed
from title import create_country, create_country_table, create_internet_protocol


def create_title(label: str, port: int = 1080):
    # Build deterministic marker nodes for each protocol family.
    encoded_label = quote(label, safe="")
    reality = (
        f"vless://11111111-1111-1111-1111-111111111111@127.0.0.1:{port}"
        f"?security=reality&type=tcp&sni=localhost&fp=chrome&pbk=PUBLICKEY123&sid=ABCD#{encoded_label}"
    )
    vless = (
        f"vless://22222222-2222-2222-2222-222222222222@127.0.0.1:{port}"
        f"?security=tls&type=tcp&sni=localhost#{encoded_label}"
    )
    vmess_payload = base64.b64encode(
        (
            f'{{"v":"2","ps":"{label}","add":"127.0.0.1","port":"{port}",'
            f'"id":"33333333-3333-3333-3333-333333333333","aid":"0","scy":"auto","net":"tcp"}}'
        ).encode("utf-8")
    ).decode("utf-8")
    vmess = f"vmess://{vmess_payload}"
    trojan = f"trojan://password@127.0.0.1:{port}#{encoded_label}"
    ss = f"ss://YWVzLTEyOC1nY206cGFzc3dvcmQ=@127.0.0.1:{port}#{encoded_label}"
    return reality, vless, vmess, trojan, ss


def generate_outputs(state: dict, repo_root: Path) -> None:
    # Define update date and time based on Iran timezone and calendar
    datetime_update = jdatetime.datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
    datetime_update_str = datetime_update.strftime("\U0001F504 LATEST-UPDATE \U0001F4C5 %a-%d-%B-%Y \U0001F551 %H:%M").upper()
    reality_update, vless_update, vmess_update, trojan_update, shadowsocks_update = create_title(datetime_update_str, port=1080)

    dev_sign = "\U0001F468\U0001F3FB\u200D\U0001F4BB DEVELOPED-BY SOROUSH-MIRZAEI \U0001F4CC FOLLOW-CONTACT SYDSRSMRZ"
    reality_dev_sign, vless_dev_sign, vmess_dev_sign, trojan_dev_sign, shadowsocks_dev_sign = create_title(dev_sign, port=8080)

    adv_bool = True
    adv_sign = "\U0001F916 TELEGRAM-CHANNEL \U0001F31F ARTIFICIAL-INTELLIGENCE \U0001F5A5 @NEUROVANCE \U0001F9E0"
    reality_adv_sign, vless_adv_sign, vmess_adv_sign, trojan_adv_sign, shadowsocks_adv_sign = create_title(adv_sign, port=2080)

    dnt_bool = True
    dnt_sign = "\U0001F6E1 TELEGRAM-CHANNEL \U0001F510 MTPROTO-PROXY \U0001F30D @NEXUPROXY \U0001F4E1"
    reality_dnt_sign, vless_dnt_sign, vmess_dnt_sign, trojan_dnt_sign, shadowsocks_dnt_sign = create_title(dnt_sign, port=3080)

    chunks = state["chunks"]
    array_mixed = state["array_mixed"]
    array_shadowsocks = state["array_shadowsocks"]
    array_trojan = state["array_trojan"]
    array_vmess = state["array_vmess"]
    array_vless = state["array_vless"]
    array_reality = state["array_reality"]
    array_tuic = state["array_tuic"]
    array_hysteria = state["array_hysteria"]
    array_juicity = state["array_juicity"]
    raw_matches_shadowsocks = state["raw_matches_shadowsocks"]
    raw_matches_trojan = state["raw_matches_trojan"]
    raw_matches_vmess = state["raw_matches_vmess"]
    raw_matches_vless = state["raw_matches_vless"]
    raw_matches_reality = state["raw_matches_reality"]
    raw_matches_tuic = state["raw_matches_tuic"]
    raw_matches_hysteria = state["raw_matches_hysteria"]
    raw_matches_juicity = state["raw_matches_juicity"]
    array_tls = state["array_tls"]
    array_non_tls = state["array_non_tls"]
    array_tcp = state["array_tcp"]
    array_ws = state["array_ws"]
    array_http = state["array_http"]
    array_grpc = state["array_grpc"]
    raw_matches_tls = state["raw_matches_tls"]
    raw_matches_non_tls = state["raw_matches_non_tls"]
    raw_matches_tcp = state["raw_matches_tcp"]
    raw_matches_ws = state["raw_matches_ws"]
    raw_matches_http = state["raw_matches_http"]
    raw_matches_grpc = state["raw_matches_grpc"]
    array_shadowsocks_channels = state["array_shadowsocks_channels"]
    array_trojan_channels = state["array_trojan_channels"]
    array_vmess_channels = state["array_vmess_channels"]
    array_vless_channels = state["array_vless_channels"]
    array_reality_channels = state["array_reality_channels"]
    array_tuic_channels = state["array_tuic_channels"]
    array_hysteria_channels = state["array_hysteria_channels"]
    array_juicity_channels = state["array_juicity_channels"]
    array_tls_channels = state["array_tls_channels"]
    array_non_tls_channels = state["array_non_tls_channels"]
    array_tcp_channels = state["array_tcp_channels"]
    array_ws_channels = state["array_ws_channels"]
    array_http_channels = state["array_http_channels"]
    array_grpc_channels = state["array_grpc_channels"]
    all_subscription_matches = state["all_subscription_matches"]
    all_channel_matches = state["all_channel_matches"]

    # Save configurations based on splitted and chunks
    for i in range(0, 10):
        path = Path(repo_root) / f"splitted/mixed-{i}"
        if i < len(chunks):
            with path.open("w", encoding="utf-8") as file:
                chunks[i].insert(0, trojan_update)
                if adv_bool:
                    chunks[i].insert(1, trojan_adv_sign)
                if dnt_bool:
                    chunks[i].insert(2, trojan_dnt_sign)
                chunks[i].append(trojan_dev_sign)
                file.write(base64.b64encode("\n".join(chunks[i]).encode("utf-8")).decode("utf-8"))
        else:
            path.write_text("", encoding="utf-8")

    country_based_configs_dict = create_country(array_mixed)
    for country in country_based_configs_dict.keys():
        country_based_configs_dict[country].insert(0, trojan_update)
        if adv_bool:
            country_based_configs_dict[country].insert(1, trojan_adv_sign)
        if dnt_bool:
            country_based_configs_dict[country].insert(2, trojan_dnt_sign)
        country_based_configs_dict[country].append(trojan_dev_sign)
        (repo_root / "countries" / country).mkdir(parents=True, exist_ok=True)
        with (repo_root / f"countries/{country}/mixed").open("w", encoding="utf-8") as file:
            file.write(base64.b64encode("\n".join(country_based_configs_dict[country]).encode("utf-8")).decode("utf-8"))

    array_mixed_ipv4, array_mixed_ipv6 = create_internet_protocol(array_mixed)
    with (repo_root / "layers/ipv4").open("w", encoding="utf-8") as file:
        array_mixed_ipv4.insert(0, trojan_update)
        if adv_bool:
            array_mixed_ipv4.insert(1, trojan_adv_sign)
        if dnt_bool:
            array_mixed_ipv4.insert(2, trojan_dnt_sign)
        array_mixed_ipv4.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(array_mixed_ipv4).encode("utf-8")).decode("utf-8"))
    build_clash_verge_feed(repo_root / "layers/ipv4-clash-verge.yaml", array_mixed_ipv4)

    with (repo_root / "layers/ipv6").open("w", encoding="utf-8") as file:
        array_mixed_ipv6.insert(0, trojan_update)
        if adv_bool:
            array_mixed_ipv6.insert(1, trojan_adv_sign)
        if dnt_bool:
            array_mixed_ipv6.insert(2, trojan_dnt_sign)
        array_mixed_ipv6.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(array_mixed_ipv6).encode("utf-8")).decode("utf-8"))
    build_clash_verge_feed(repo_root / "layers/ipv6-clash-verge.yaml", array_mixed_ipv6)

    clash_yaml = convert_v2ray_subscription_to_mihomo_config("\n".join(array_mixed), ConvertOptions()).yaml
    (repo_root / "layers/clash.yaml").write_text(clash_yaml, encoding="utf-8")

    with (repo_root / "splitted/mixed").open("w", encoding="utf-8") as file:
        array_mixed.insert(0, trojan_update)
        if adv_bool:
            array_mixed.insert(1, trojan_adv_sign)
        if dnt_bool:
            array_mixed.insert(2, trojan_dnt_sign)
        array_mixed.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(array_mixed).encode("utf-8")).decode("utf-8"))

    all_subscription_matches = list(set(state["matches_shadowsocks"] + state["matches_trojan"] + state["matches_vmess"] + state["matches_vless"] + state["matches_reality"]))
    array_subscription_ipv4, array_subscription_ipv6 = create_internet_protocol(all_subscription_matches)
    with (repo_root / "subscribe/layers/ipv4").open("w", encoding="utf-8") as file:
        array_subscription_ipv4.insert(0, trojan_update)
        if adv_bool:
            array_subscription_ipv4.insert(1, trojan_adv_sign)
        if dnt_bool:
            array_subscription_ipv4.insert(2, trojan_dnt_sign)
        array_subscription_ipv4.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(array_subscription_ipv4).encode("utf-8")).decode("utf-8"))
    build_clash_verge_feed(repo_root / "subscribe/layers/ipv4-clash-verge.yaml", array_subscription_ipv4)

    with (repo_root / "subscribe/layers/ipv6").open("w", encoding="utf-8") as file:
        array_subscription_ipv6.insert(0, trojan_update)
        if adv_bool:
            array_subscription_ipv6.insert(1, trojan_adv_sign)
        if dnt_bool:
            array_subscription_ipv6.insert(2, trojan_dnt_sign)
        array_subscription_ipv6.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(array_subscription_ipv6).encode("utf-8")).decode("utf-8"))
    build_clash_verge_feed(repo_root / "subscribe/layers/ipv6-clash-verge.yaml", array_subscription_ipv6)
    with (repo_root / "splitted/subscribe").open("w", encoding="utf-8") as file:
        all_subscription_matches.insert(0, trojan_update)
        if adv_bool:
            all_subscription_matches.insert(1, trojan_adv_sign)
        if dnt_bool:
            all_subscription_matches.insert(2, trojan_dnt_sign)
        all_subscription_matches.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(all_subscription_matches).encode("utf-8")).decode("utf-8"))
    (repo_root / "subscribe/layers/clash.yaml").write_text(clash_yaml, encoding="utf-8")

    all_channel_matches = list(set(state["array_shadowsocks_channels"] + state["array_trojan_channels"] + state["array_vmess_channels"] + state["array_vless_channels"] + state["array_reality_channels"]))
    array_channel_ipv4, array_channel_ipv6 = create_internet_protocol(all_channel_matches)
    with (repo_root / "channels/layers/ipv4").open("w", encoding="utf-8") as file:
        array_channel_ipv4.insert(0, trojan_update)
        if adv_bool:
            array_channel_ipv4.insert(1, trojan_adv_sign)
        if dnt_bool:
            array_channel_ipv4.insert(2, trojan_dnt_sign)
        array_channel_ipv4.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(array_channel_ipv4).encode("utf-8")).decode("utf-8"))
    build_clash_verge_feed(repo_root / "channels/layers/ipv4-clash-verge.yaml", array_channel_ipv4)

    with (repo_root / "channels/layers/ipv6").open("w", encoding="utf-8") as file:
        array_channel_ipv6.insert(0, trojan_update)
        if adv_bool:
            array_channel_ipv6.insert(1, trojan_adv_sign)
        if dnt_bool:
            array_channel_ipv6.insert(2, trojan_dnt_sign)
        array_channel_ipv6.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(array_channel_ipv6).encode("utf-8")).decode("utf-8"))
    build_clash_verge_feed(repo_root / "channels/layers/ipv6-clash-verge.yaml", array_channel_ipv6)
    with (repo_root / "splitted/channels").open("w", encoding="utf-8") as file:
        all_channel_matches.insert(0, trojan_update)
        if adv_bool:
            all_channel_matches.insert(1, trojan_adv_sign)
        if dnt_bool:
            all_channel_matches.insert(2, trojan_dnt_sign)
        all_channel_matches.append(trojan_dev_sign)
        file.write(base64.b64encode("\n".join(all_channel_matches).encode("utf-8")).decode("utf-8"))

    array_shadowsocks.insert(0, shadowsocks_update)
    array_trojan.insert(0, trojan_update)
    array_vmess.insert(0, vmess_update)
    array_vless.insert(0, vless_update)
    array_reality.insert(0, reality_update)
    array_tuic.insert(0, vless_update)
    array_hysteria.insert(0, vless_update)
    array_juicity.insert(0, vless_update)

    if adv_bool:
        array_shadowsocks.insert(1, shadowsocks_adv_sign)
        array_trojan.insert(1, trojan_adv_sign)
        array_vmess.insert(1, vmess_adv_sign)
        array_vless.insert(1, vless_adv_sign)
        array_reality.insert(1, reality_adv_sign)
        array_tuic.insert(1, vless_adv_sign)
        array_hysteria.insert(1, vless_adv_sign)
        array_juicity.insert(1, vless_adv_sign)

    if dnt_bool:
        array_shadowsocks.insert(2, shadowsocks_dnt_sign)
        array_trojan.insert(2, trojan_dnt_sign)
        array_vmess.insert(2, vmess_dnt_sign)
        array_vless.insert(2, vless_dnt_sign)
        array_reality.insert(2, reality_dnt_sign)
        array_tuic.insert(2, vless_dnt_sign)
        array_hysteria.insert(2, vless_dnt_sign)
        array_juicity.insert(2, vless_dnt_sign)

    array_shadowsocks.append(shadowsocks_dev_sign)
    array_trojan.append(trojan_dev_sign)
    array_vmess.append(vmess_dev_sign)
    array_vless.append(vless_dev_sign)
    array_reality.append(reality_dev_sign)
    array_tuic.append(vless_dev_sign)
    array_hysteria.append(vless_dev_sign)
    array_juicity.append(vless_dev_sign)

    (repo_root / "protocols").mkdir(exist_ok=True)
    (repo_root / "subscribe/protocols").mkdir(parents=True, exist_ok=True)
    (repo_root / "channels/protocols").mkdir(parents=True, exist_ok=True)
    (repo_root / "security").mkdir(exist_ok=True)
    (repo_root / "subscribe/security").mkdir(parents=True, exist_ok=True)
    (repo_root / "channels/security").mkdir(parents=True, exist_ok=True)
    (repo_root / "networks").mkdir(exist_ok=True)
    (repo_root / "subscribe/networks").mkdir(parents=True, exist_ok=True)
    (repo_root / "channels/networks").mkdir(parents=True, exist_ok=True)

    # Save configurations into files splitted based on configuration type
    for rel, content in [
        ("protocols/shadowsocks", array_shadowsocks),
        ("protocols/trojan", array_trojan),
        ("protocols/vmess", array_vmess),
        ("protocols/vless", array_vless),
        ("protocols/reality", array_reality),
        ("protocols/tuic", array_tuic),
        ("protocols/hysteria", array_hysteria),
        ("protocols/juicity", array_juicity),
        ("security/tls", array_tls),
        ("security/non-tls", array_non_tls),
        ("networks/tcp", array_tcp),
        ("networks/ws", array_ws),
        ("networks/http", array_http),
        ("networks/grpc", array_grpc),
        ("subscribe/protocols/shadowsocks", raw_matches_shadowsocks),
        ("subscribe/protocols/trojan", raw_matches_trojan),
        ("subscribe/protocols/vmess", raw_matches_vmess),
        ("subscribe/protocols/vless", raw_matches_vless),
        ("subscribe/protocols/reality", raw_matches_reality),
        ("subscribe/protocols/tuic", raw_matches_tuic),
        ("subscribe/protocols/hysteria", raw_matches_hysteria),
        ("subscribe/protocols/juicity", raw_matches_juicity),
        ("subscribe/security/tls", raw_matches_tls),
        ("subscribe/security/non-tls", raw_matches_non_tls),
        ("subscribe/networks/tcp", raw_matches_tcp),
        ("subscribe/networks/ws", raw_matches_ws),
        ("subscribe/networks/http", raw_matches_http),
        ("subscribe/networks/grpc", raw_matches_grpc),
        ("channels/protocols/shadowsocks", array_shadowsocks_channels),
        ("channels/protocols/trojan", array_trojan_channels),
        ("channels/protocols/vmess", array_vmess_channels),
        ("channels/protocols/vless", array_vless_channels),
        ("channels/protocols/reality", array_reality_channels),
        ("channels/protocols/tuic", array_tuic_channels),
        ("channels/protocols/hysteria", array_hysteria_channels),
        ("channels/protocols/juicity", array_juicity_channels),
        ("channels/security/tls", array_tls_channels),
        ("channels/security/non-tls", array_non_tls_channels),
        ("channels/networks/tcp", array_tcp_channels),
        ("channels/networks/ws", array_ws_channels),
        ("channels/networks/http", array_http_channels),
        ("channels/networks/grpc", array_grpc_channels),
    ]:
        target = repo_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(base64.b64encode("\n".join(content).encode("utf-8")).decode("utf-8"), encoding="utf-8")

    readme = '''## Introduction
The script systematically collects Vmess, Vless, ShadowSocks, Trojan, Reality, Hysteria, Tuic, and Juicity configurations from publicly accessible Telegram channels. It categorizes these configurations based on open and closed ports, eliminates duplicate entries, resolves configuration addresses using IP addresses, and revises configuration titles to reflect server and protocol-type properties. These properties include network and security type, IP address and port, and the respective country associated with the configuration.
'''
    stats = """## Stats
[![Stars](https://starchart.cc/hadifarajvand/telegram-config-vray.svg?variant=adaptive)](https://starchart.cc/hadifarajvand/telegram-config-vray)
## Activity
![Alt](https://repobeats.axiom.co/api/embed/6e88aa7d66986824532760b5b14120a22c8ca813.svg "Repobeats analytics image")"""
    (repo_root / "readme.md").write_text(readme + "\n" + create_country_table(str(repo_root / "countries")) + "\n" + stats, encoding="utf-8")
