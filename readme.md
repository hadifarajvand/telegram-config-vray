# Telegram Config Vray

Automated V2Ray/Xray subscription collector and feed generator. The project collects public proxy configuration links, normalizes and deduplicates them, validates reachable endpoints where possible, and publishes both raw V2Ray-style subscriptions and Clash/Mihomo YAML profiles.

The current stack supports VLESS, VMess, Trojan, Shadowsocks, Reality, Hysteria, TUIC, and Juicity inputs. Clash Verge Rev support is first-class through generated Mihomo-compatible YAML files.

## Subscription Links

Primary feeds:

| Feed | Format | Subscription Link |
| --- | --- | --- |
| IPv4 raw subscription | Base64 V2Ray links | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv4) |
| IPv6 raw subscription | Base64 V2Ray links | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv6) |
| Clash/Mihomo profile | YAML | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/clash.yaml) |
| Clash Verge IPv4 profile | YAML | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv4-clash-verge.yaml) |
| Clash Verge IPv6 profile | YAML | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv6-clash-verge.yaml) |
| Subscription-only IPv4 raw feed | Base64 V2Ray links | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv4) |
| Subscription-only Clash Verge IPv4 profile | YAML | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv4-clash-verge.yaml) |
| Channel-only IPv4 raw feed | Base64 V2Ray links | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv4) |
| Channel-only Clash Verge IPv4 profile | YAML | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv4-clash-verge.yaml) |

Country feeds:

| Code | Country Name | Subscription Link | Code | Country Name | Subscription Link |
|:---:|:---|:---|:---:|:---|:---|
| AE | United Arab Emirates | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ae/mixed) | AL | Albania | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/al/mixed) |
| AM | Armenia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/am/mixed) | AR | Argentina | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ar/mixed) |
| AT | Austria | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/at/mixed) | AU | Australia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/au/mixed) |
| AZ | Azerbaijan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/az/mixed) | BA | Bosnia and Herzegovina | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ba/mixed) |
| BD | Bangladesh | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bd/mixed) | BE | Belgium | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/be/mixed) |
| BG | Bulgaria | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bg/mixed) | BH | Bahrain | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bh/mixed) |
| BO | Bolivia, Plurinational State of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bo/mixed) | BR | Brazil | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/br/mixed) |
| BY | Belarus | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/by/mixed) | BZ | Belize | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bz/mixed) |
| CA | Canada | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ca/mixed) | CH | Switzerland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ch/mixed) |
| CL | Chile | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cl/mixed) | CM | Cameroon | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cm/mixed) |
| CN | China | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cn/mixed) | CO | Colombia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/co/mixed) |
| CR | Costa Rica | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cr/mixed) | CY | Cyprus | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cy/mixed) |
| CZ | Czechia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cz/mixed) | DE | Germany | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/de/mixed) |
| DK | Denmark | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/dk/mixed) | DZ | Algeria | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/dz/mixed) |
| EC | Ecuador | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ec/mixed) | EE | Estonia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ee/mixed) |
| EG | Egypt | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/eg/mixed) | ES | Spain | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/es/mixed) |
| FI | Finland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/fi/mixed) | FR | France | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/fr/mixed) |
| GB | United Kingdom | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gb/mixed) | GE | Georgia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ge/mixed) |
| GI | Gibraltar | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gi/mixed) | GR | Greece | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gr/mixed) |
| GT | Guatemala | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gt/mixed) | HK | Hong Kong | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/hk/mixed) |
| HR | Croatia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/hr/mixed) | HU | Hungary | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/hu/mixed) |
| ID | Indonesia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/id/mixed) | IE | Ireland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ie/mixed) |
| IL | Israel | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/il/mixed) | IM | Isle of Man | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/im/mixed) |
| IN | India | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/in/mixed) | IQ | Iraq | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/iq/mixed) |
| IR | Iran, Islamic Republic of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ir/mixed) | IS | Iceland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/is/mixed) |
| IT | Italy | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/it/mixed) | JO | Jordan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/jo/mixed) |
| JP | Japan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/jp/mixed) | KE | Kenya | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ke/mixed) |
| KG | Kyrgyzstan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kg/mixed) | KH | Cambodia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kh/mixed) |
| KR | Korea, Republic of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kr/mixed) | KW | Kuwait | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kw/mixed) |
| KZ | Kazakhstan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kz/mixed) | LI | Liechtenstein | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/li/mixed) |
| LT | Lithuania | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/lt/mixed) | LU | Luxembourg | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/lu/mixed) |
| LV | Latvia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/lv/mixed) | LY | Libya | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ly/mixed) |
| MA | Morocco | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ma/mixed) | MD | Moldova, Republic of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/md/mixed) |
| ME | Montenegro | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/me/mixed) | MH | Marshall Islands | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mh/mixed) |
| MK | North Macedonia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mk/mixed) | MT | Malta | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mt/mixed) |
| MU | Mauritius | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mu/mixed) | MV | Maldives | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mv/mixed) |
| MX | Mexico | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mx/mixed) | MY | Malaysia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/my/mixed) |
| NA | Not Available | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/na/mixed) | NG | Nigeria | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ng/mixed) |
| NL | Netherlands | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/nl/mixed) | NO | Norway | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/no/mixed) |
| NP | Nepal | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/np/mixed) | NZ | New Zealand | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/nz/mixed) |
| OM | Oman | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/om/mixed) | PA | Panama | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pa/mixed) |
| PE | Peru | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pe/mixed) | PH | Philippines | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ph/mixed) |
| PK | Pakistan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pk/mixed) | PL | Poland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pl/mixed) |
| PR | Puerto Rico | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pr/mixed) | PS | Palestine, State of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ps/mixed) |
| PT | Portugal | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pt/mixed) | PY | Paraguay | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/py/mixed) |
| QA | Qatar | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/qa/mixed) | RO | Romania | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ro/mixed) |
| RS | Serbia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/rs/mixed) | RU | Russian Federation | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ru/mixed) |
| SA | Saudi Arabia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sa/mixed) | SC | Seychelles | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sc/mixed) |
| SE | Sweden | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/se/mixed) | SG | Singapore | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sg/mixed) |
| SI | Slovenia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/si/mixed) | SK | Slovakia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sk/mixed) |
| TG | Togo | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/tg/mixed) | TH | Thailand | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/th/mixed) |
| TR | Türkiye | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/tr/mixed) | TW | Taiwan, Province of China | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/tw/mixed) |
| UA | Ukraine | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ua/mixed) | US | United States | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/us/mixed) |
| UZ | Uzbekistan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/uz/mixed) | VG | Virgin Islands, British | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/vg/mixed) |
| VN | Viet Nam | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/vn/mixed) | XK | Kosovo | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/xk/mixed) |
| ZA | South Africa | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/za/mixed) |  |  |  |

## Generated Outputs

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
