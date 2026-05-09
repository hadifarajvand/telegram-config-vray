# Telegram Config Vray

Automated V2Ray/Xray subscription collector and feed generator. The project collects public proxy configuration links, normalizes and deduplicates them, validates reachable endpoints where possible, and publishes both raw V2Ray-style subscriptions and Clash/Mihomo YAML profiles.

The current stack supports VLESS, VMess, Trojan, Shadowsocks, Reality, Hysteria, TUIC, and Juicity inputs. Clash Verge Rev support is first-class through generated Mihomo-compatible YAML files.

## Outputs

Main generated feeds:

| Feed | Format | Path |
| --- | --- | --- |
| IPv4 raw subscription | Base64 V2Ray links | `layers/ipv4` |
| IPv6 raw subscription | Base64 V2Ray links | `layers/ipv6` |
| All-node Clash profile | Clash/Mihomo YAML | `layers/clash.yaml` |
| IPv4 Clash Verge profile | Clash/Mihomo YAML | `layers/ipv4-clash-verge.yaml` |
| IPv6 Clash Verge profile | Clash/Mihomo YAML | `layers/ipv6-clash-verge.yaml` |
| Subscription-only IPv4 raw feed | Base64 V2Ray links | `subscribe/layers/ipv4` |
| Subscription-only IPv4 Clash Verge profile | Clash/Mihomo YAML | `subscribe/layers/ipv4-clash-verge.yaml` |
| Channel-only IPv4 raw feed | Base64 V2Ray links | `channels/layers/ipv4` |
| Channel-only IPv4 Clash Verge profile | Clash/Mihomo YAML | `channels/layers/ipv4-clash-verge.yaml` |

Country feeds are generated under:

```text
countries/<country-code>/mixed
```

Example:

```text
https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/nl/mixed
```

## Clash Verge Rev

Clash Verge Rev expects Clash/Mihomo YAML, not raw V2Ray links. Use the generated `*-clash-verge.yaml` files for Clash Verge Rev imports.

Recommended profile URL after the workflow is merged to `main`:

```text
https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv4-clash-verge.yaml
```

Alternative Clash/Mihomo outputs:

```text
https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/clash.yaml
https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv4-clash-verge.yaml
https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv4-clash-verge.yaml
```

The generated Clash Verge profile uses:

| Group | Type | Purpose |
| --- | --- | --- |
| `Proxy-Select` | `select` | Manual parent group for choosing auto-test, load-balance, direct, or a specific node |
| `Auto-Lowest-Delay` | `url-test` | Picks the lowest-latency available node |
| `Load-Balance` | `load-balance` | Spreads traffic using `round-robin` |

App-specific rules, when enabled by the converter, route selected macOS processes to `Proxy-Select` and keep the final fallback as `MATCH,DIRECT`.

## Local Usage

Create and activate the virtual environment:

```bash
python3 -m venv .venvmac
source .venvmac/bin/activate
pip install -r requirements.txt
```

Generate feeds:

```bash
python3 main.py
```

Run the local API server:

```bash
./serve_local_api.sh
```

Default local API:

```text
http://0.0.0.0:8888
```

Useful local endpoints:

| Endpoint | Description |
| --- | --- |
| `/health` | API health and source-file status |
| `/status` | API status and available feeds |
| `/v2ray/ipv4` | Raw IPv4 V2Ray-style subscription |
| `/clash/ipv4` | General Clash/Mihomo YAML |
| `/clash/ipv4-clash-verge` | Clash Verge IPv4 YAML |
| `/v2ray/countries/nl/mixed` | Raw Netherlands mixed subscription |
| `/clash/countries/nl/mixed` | Netherlands mixed subscription converted to Clash YAML |

For LAN use, import this URL in Clash Verge Rev after starting the local API:

```text
http://<your-lan-ip>:8888/clash/ipv4-clash-verge
```

Example:

```text
http://192.168.1.100:8888/clash/ipv4-clash-verge
```

## Converter

The Mihomo converter lives in `converter/` and exposes the project-level conversion logic used by generated Clash feeds.

Supported input forms:

| Input | Status |
| --- | --- |
| `vless://` | Supported |
| `vmess://` legacy Base64 JSON | Supported |
| `trojan://` | Supported |
| `ss://` | Supported |
| Base64 subscription lists | Supported |
| Existing Clash YAML with `proxies` | Supported |
| Invalid mixed lines | Ignored with warnings |

CLI wrapper:

```bash
./convert-v2ray --input input.txt --output clash.yaml
./convert-v2ray --input input.txt --output clash.yaml --prepend-app-rules
```

## Automation

GitHub Actions workflow:

```text
.github/workflows/update-feeds.yml
```

The workflow:

| Step | Purpose |
| --- | --- |
| Schedule | Runs every 2 hours via cron |
| Manual trigger | Supports `workflow_dispatch` |
| Concurrency | Cancels overlapping runs |
| Compile check | Verifies Python modules before generation |
| Generate feeds | Runs `python main.py` |
| Strict validation | Fails if required feed files are missing or empty |
| Conditional commit | Commits only when generated files changed |
| Push | Pushes refreshed feeds back to the branch |

Required GitHub repository setting:

```text
Settings -> Actions -> General -> Workflow permissions -> Read and write permissions
```

If the default branch is protected, allow `github-actions[bot]` to push or change the workflow to publish updates to a separate branch.

## Project Structure

```text
api/                  Local REST API server
converter/            V2Ray/Xray to Clash/Mihomo converter
feeds/                Output generation and Clash Verge feed writing
scraper/              Telegram/subscription collection pipeline
layers/               Combined generated feeds
subscribe/            Subscription-source generated feeds
channels/             Telegram-channel generated feeds
countries/            Country-specific raw subscriptions
tests/                Converter tests
```

## Validation

Run compile checks:

```bash
python3 -m py_compile main.py scraper/collector.py feeds/output_generation.py api/server.py
```

Run converter tests:

```bash
python3 -m pytest tests
```

Run a full feed refresh:

```bash
python3 main.py
```

The full refresh performs network collection and endpoint checks, so it can take time.

## Notes

Raw V2Ray links are node definitions. Clash Verge Rev works best with complete Clash/Mihomo YAML profiles that include proxies, proxy groups, and rules. Use the `*-clash-verge.yaml` outputs for Clash Verge Rev instead of importing raw V2Ray links directly.

Public proxy feeds are volatile. A successful parse does not guarantee a node is fast, stable, or trustworthy.
