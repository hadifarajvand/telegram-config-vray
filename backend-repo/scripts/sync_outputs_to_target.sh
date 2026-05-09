#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="${1:?source root required}"
TARGET_ROOT="${2:?target root required}"
PATHS_FILE="${3:?paths file required}"

cd "$TARGET_ROOT"

# Remove all tracked/untracked files from target checkout working tree,
# then restore only generated output artifacts from source.
find . -mindepth 1 -maxdepth 1 ! -name ".git" -exec rm -rf {} +

while IFS= read -r rel; do
  [[ -z "$rel" ]] && continue
  src="$SOURCE_ROOT/$rel"
  dst="$TARGET_ROOT/$rel"
  if [[ -d "$src" ]]; then
    mkdir -p "$dst"
    cp -R "$src"/. "$dst"/
  elif [[ -f "$src" ]]; then
    mkdir -p "$(dirname "$dst")"
    cp "$src" "$dst"
  fi
done < "$PATHS_FILE"

# Publish output-only README in target repo.
cat > "$TARGET_ROOT/README.md" <<'MD'
# telegram-config-vray outputs

This repository contains generated output artifacts only.

Primary feeds:

- `layers/ipv4`
- `layers/ipv6`
- `layers/clash.yaml`
- `layers/ipv4-clash-verge.yaml`
- `layers/ipv6-clash-verge.yaml`

Country feeds:

- `countries/<code>/mixed`

Clash Verge import (IPv4):

`https://raw.githubusercontent.com/hadifarajvand/telegram-config-vray/main/layers/ipv4-clash-verge.yaml`
MD
