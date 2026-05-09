# V2Ray/Xray to Mihomo Converter

This project now includes a standalone converter that turns raw V2Ray/Xray
subscription content into Clash/Mihomo YAML for Clash Verge Rev.

What it accepts:

- single `vless://` links
- single `vmess://` links
- multiline subscriptions
- Base64-encoded subscriptions
- existing Clash/Mihomo YAML with a top-level `proxies` list

What it emits:

- `proxies`
- a `Proxy` selector group
- `rules` ending in `MATCH,DIRECT`
- optional macOS process rules before the fallback rule

Why this matters:

- V2Ray links are node definitions, not full Clash configs
- Clash Verge Rev expects Clash/Mihomo YAML
- VLESS Reality requires `pbk`, `sid`, `sni`, `fp`, and often `flow`
- Dropping those fields breaks the node

CLI:

```bash
./convert-v2ray --input input.txt --output clash.yaml --prepend-app-rules
```
