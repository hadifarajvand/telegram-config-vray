# telegram-config-vray outputs

This repository is the public artifact bucket for generated subscription files.
The private backend repository produces these files on GitHub Actions and syncs
them here.

## Exact file links

Primary feeds:

- `layers/ipv4`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv4
- `layers/ipv6`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv6
- `layers/clash.yaml`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/clash.yaml
- `layers/ipv4-clash-verge.yaml`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv4-clash-verge.yaml
- `layers/ipv6-clash-verge.yaml`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv6-clash-verge.yaml

Grouped feeds:

- `channels/layers/ipv4`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv4
- `channels/layers/ipv4-clash-verge.yaml`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv4-clash-verge.yaml
- `channels/layers/ipv6`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv6
- `channels/layers/ipv6-clash-verge.yaml`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/layers/ipv6-clash-verge.yaml
- `channels/security/tls`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/security/tls
- `channels/security/non-tls`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/channels/security/non-tls

Subscription feeds:

- `subscribe/layers/ipv4`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv4
- `subscribe/layers/ipv4-clash-verge.yaml`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv4-clash-verge.yaml
- `subscribe/layers/ipv6`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv6
- `subscribe/layers/ipv6-clash-verge.yaml`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/layers/ipv6-clash-verge.yaml
- `subscribe/security/tls`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/security/tls
- `subscribe/security/non-tls`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/subscribe/security/non-tls

Public Pages assets:

- `security/dist/index.html`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/security/dist/index.html
- Pages site: https://hadifarajvand.github.io/telegram-config-vray/

Country examples:

- `countries/us/mixed`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/us/mixed
- `countries/nl/mixed`: https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/countries/nl/mixed

## Automation

- Backend generator: `hadifarajvand/telegram-config-vray-backend` private repo
- Public output repo: this repo
- Backend GitHub Actions syncs explicit generated paths only, plus the public Pages files listed in `config/public_keep_paths.txt`
