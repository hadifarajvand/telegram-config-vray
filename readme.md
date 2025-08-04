## Introduction
The script systematically collects Vmess, Vless, ShadowSocks, Trojan, Reality, Hysteria, Tuic, and Juicity configurations from publicly accessible Telegram channels. It categorizes these configurations based on open and closed ports, eliminates duplicate entries, resolves configuration addresses using IP addresses, and revises configuration titles to reflect server and protocol-type properties. These properties include network and security type, IP address and port, and the respective country associated with the configuration.

![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/hadifarajvand/telegram-config-vray?label=Last%20Commit&color=%2338914b)
![GitHub](https://img.shields.io/github/license/hadifarajvand/telegram-config-vray?label=License&color=yellow)
![GitHub Repo stars](https://img.shields.io/github/stars/hadifarajvand/telegram-config-vray?label=Stars&color=red&style=flat)
![GitHub forks](https://img.shields.io/github/forks/hadifarajvand/telegram-config-vray?label=Forks&color=blue&style=flat)
[![Execute On Schedule](https://github.com/hadifarajvand/telegram-config-vray/actions/workflows/schedule.yml/badge.svg)](https://github.com/hadifarajvand/telegram-config-vray/actions/workflows/schedule.yml)
[![Execute On Push](https://github.com/hadifarajvand/telegram-config-vray/actions/workflows/push.yml/badge.svg)](https://github.com/hadifarajvand/telegram-config-vray/actions/workflows/push.yml)

## Tutorial
This is a guide for configuring domains by routing type in the `nekoray` and `nekobox` applications when using the `sing-box` core. To implement these domain settings, create new routes in either application and add the appropriate domains to the relevant `domains` section. Configure the outbound setting as `bypass`, `proxy`, or `block` according to the specifications provided for each domain category.

- Bypass
```
geosite:category-ir
geosite:category-bank-ir
geosite:category-bourse-ir
geosite:category-education-ir
geosite:category-forums-ir
geosite:category-gov-ir
geosite:category-insurance-ir
geosite:category-media-ir
geosite:category-news-ir
geosite:category-payment-ir
geosite:category-scholar-ir
geosite:category-shopping-ir
geosite:category-social-media-ir
geosite:category-tech-ir
geosite:category-travel-ir
```

- Proxy
```
geosite:apple
geosite:adobe
geosite:anthropic
geosite:openai
geosite:clubhouse
geosite:netflix
geosite:nvidia
geosite:intel
geosite:amd
geosite:signal
geosite:soundcloud
geosite:youtube
geosite:telegram
geosite:twitter
geosite:instagram
geosite:facebook
geosite:pinterest
geosite:tiktok
geosite:spotify
geosite:twitch
geosite:discord
```

- Block
```
geosite:category-ads-all
geosite:category-ads-ir
geosite:google-ads
geosite:spotify-ads
geosite:adobe-ads
geosite:apple-ads
```

## Protocol Type Subscription Links
Subscription links for configurations are organized according to protocol type and categorized into separate Telegram channels and subscription links. These links provide access to configurations based on specific protocol requirements.
| **Protocol Type** | **Mixed Configurations** | **Telegram Channels** | **Subscription Links** |
|:---:|:---:|:---:|:---:|
| **Juicity Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/juicity) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/juicity) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/juicity) |
| **Hysteria Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/hysteria) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/hysteria) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/hysteria) |
| **Tuic Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/tuic) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/tuic) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/tuic) |
| **Reality Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/reality) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/reality) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/reality) |
| **Vless Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/vless) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/vless) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/vless) |
| **Vmess Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/vmess) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/vmess) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/vmess) |
| **Trojan Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/trojan) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/trojan) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/trojan) |
| **Shadowsocks Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/protocols/shadowsocks) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/protocols/shadowsocks) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/protocols/shadowsocks) |
| **Mixed Type Configurations** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/splitted/mixed) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/splitted/channels) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/splitted/subscribe) |

## Network Type Subscription Links
Subscription links for configurations are organized according to network type and categorized into separate Telegram channels and subscription links. These links facilitate access to configurations optimized for specific network architectures.
| **Network Type** | **Mixed Configurations** | **Telegram Channels** | **Subscription Links** |
|:---:|:---:|:---:|:---:|
| **Google Remote Procedure Call (GRPC)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/networks/grpc) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/networks/grpc) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/networks/grpc) |
| **Hypertext Transfer Protocol (HTTP)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/networks/http) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/networks/http) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/networks/http) |
| **WebSocket Protocol (WS)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/networks/ws) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/networks/ws) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/networks/ws) |
 | **Transmission Control Protocol (TCP)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/networks/tcp) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/networks/tcp) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/networks/tcp) |

## Security Type Subscription Links
Subscription links for configurations are organized according to security type and categorized into separate Telegram channels and subscription links. These links provide access to configurations with specific security implementations.
| **Security Type** | **Mixed Configurations** | **Telegram Channels** | **Subscription Links** |
|:---:|:---:|:---:|:---:|
| **Transport Layer Security (TLS)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/security/tls) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/security/tls) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/security/tls) |
| **Non Transport Layer Security (Non-TLS)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/security/non-tls) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/security/non-tls) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/security/non-tls) |

## Internet Protocol Type Subscription Links
Subscription links for configurations are organized according to internet protocol type and categorized into separate Telegram channels and subscription links. These links enable access to configurations designed for specific internet protocol versions.
| **Internet Protocol Type** | **Mixed Configurations** | **Telegram Channels** | **Subscription Links** |
|:---:|:---:|:---:|:---:|
| **Internet Protocol Version 4 (IPV4)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv4) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv4) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv4) |
| **Internet Protocol Version 6 (IPV6)** | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv6) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv6) | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv6) |

## Country Subscription Links
Subscription links for configurations are organized according to country and provide access to specialized configurations for services that implement location-based restrictions. These configurations are particularly relevant for social media and artificial intelligence services that may restrict access or ban accounts when location changes are detected.
| **Code** | **Country Name** | **Subscription Link** | **Code** | **Country Name** | **Subscription Link** |
|:---:|:---:|:---:|:---:|:---:|:---:|
| AL | Albania | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/al/mixed) | AR | Argentina | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ar/mixed) |
| AM | Armenia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/am/mixed) | AU | Australia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/au/mixed) |
| AT | Austria | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/at/mixed) | BH | Bahrain | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bh/mixed) |
| BY | Belarus | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/by/mixed) | BE | Belgium | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/be/mixed) |
| BZ | Belize | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bz/mixed) | BO | Bolivia, Plurinational State of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bo/mixed) |
| BA | Bosnia and Herzegovina | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ba/mixed) | BR | Brazil | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/br/mixed) |
| BG | Bulgaria | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/bg/mixed) | KH | Cambodia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kh/mixed) |
| CA | Canada | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ca/mixed) | CL | Chile | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cl/mixed) |
| CN | China | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cn/mixed) | CO | Colombia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/co/mixed) |
| CR | Costa Rica | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cr/mixed) | HR | Croatia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/hr/mixed) |
| CY | Cyprus | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cy/mixed) | CZ | Czechia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/cz/mixed) |
| DK | Denmark | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/dk/mixed) | EC | Ecuador | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ec/mixed) |
| EE | Estonia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ee/mixed) | FI | Finland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/fi/mixed) |
| FR | France | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/fr/mixed) | DE | Germany | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/de/mixed) |
| GI | Gibraltar | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gi/mixed) | GR | Greece | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gr/mixed) |
| GT | Guatemala | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gt/mixed) | HK | Hong Kong | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/hk/mixed) |
| HU | Hungary | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/hu/mixed) | IS | Iceland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/is/mixed) |
| IN | India | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/in/mixed) | ID | Indonesia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/id/mixed) |
| IR | Iran, Islamic Republic of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ir/mixed) | IQ | Iraq | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/iq/mixed) |
| IE | Ireland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ie/mixed) | IM | Isle of Man | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/im/mixed) |
| IL | Israel | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/il/mixed) | IT | Italy | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/it/mixed) |
| JP | Japan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/jp/mixed) | JO | Jordan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/jo/mixed) |
| KZ | Kazakhstan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kz/mixed) | KR | Korea, Republic of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kr/mixed) |
| KW | Kuwait | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kw/mixed) | KG | Kyrgyzstan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/kg/mixed) |
| LV | Latvia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/lv/mixed) | LT | Lithuania | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/lt/mixed) |
| LU | Luxembourg | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/lu/mixed) | MY | Malaysia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/my/mixed) |
| MV | Maldives | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mv/mixed) | MT | Malta | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mt/mixed) |
| MU | Mauritius | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mu/mixed) | MX | Mexico | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mx/mixed) |
| MD | Moldova, Republic of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/md/mixed) | MA | Morocco | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ma/mixed) |
| NL | Netherlands | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/nl/mixed) | NZ | New Zealand | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/nz/mixed) |
| NG | Nigeria | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ng/mixed) | MK | North Macedonia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/mk/mixed) |
| NO | Norway | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/no/mixed) | NA | Not Available | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/na/mixed) |
| OM | Oman | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/om/mixed) | PK | Pakistan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pk/mixed) |
| PS | Palestine, State of | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ps/mixed) | PY | Paraguay | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/py/mixed) |
| PE | Peru | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pe/mixed) | PH | Philippines | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ph/mixed) |
| PL | Poland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pl/mixed) | PT | Portugal | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pt/mixed) |
| PR | Puerto Rico | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/pr/mixed) | QA | Qatar | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/qa/mixed) |
| RO | Romania | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ro/mixed) | RU | Russian Federation | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ru/mixed) |
| SA | Saudi Arabia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sa/mixed) | RS | Serbia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/rs/mixed) |
| SC | Seychelles | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sc/mixed) | SG | Singapore | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sg/mixed) |
| SK | Slovakia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/sk/mixed) | SI | Slovenia | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/si/mixed) |
| ZA | South Africa | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/za/mixed) | ES | Spain | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/es/mixed) |
| SE | Sweden | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/se/mixed) | CH | Switzerland | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ch/mixed) |
| TW | Taiwan, Province of China | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/tw/mixed) | TH | Thailand | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/th/mixed) |
| TG | Togo | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/tg/mixed) | TR | T�rkiye | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/tr/mixed) |
| UA | Ukraine | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ua/mixed) | AE | United Arab Emirates | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/ae/mixed) |
| GB | United Kingdom | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/gb/mixed) | US | United States | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/us/mixed) |
| UZ | Uzbekistan | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/uz/mixed) | VN | Viet Nam | [Subscription Link](https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/vn/mixed) |
## Stats
[![Stars](https://starchart.cc/hadifarajvand/telegram-config-vray.svg?variant=adaptive)](https://starchart.cc/hadifarajvand/telegram-config-vray)
## Activity
![Alt](https://repobeats.axiom.co/api/embed/6e88aa7d66986824532760b5b14120a22c8ca813.svg "Repobeats analytics image")