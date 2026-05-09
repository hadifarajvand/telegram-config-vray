#!/usr/bin/env bash
set -euo pipefail

# Ensure generation directories exist in a clean runner.
mkdir -p \
  channels/layers channels/networks channels/protocols channels/security \
  countries \
  layers \
  networks \
  protocols \
  security/dist security/scripts \
  splitted \
  subscribe/layers subscribe/networks subscribe/protocols subscribe/security

# Ensure timestamp file exists.
if [[ ! -f "last update" ]]; then
  python3 - <<'PY'
from datetime import datetime, timezone, timedelta
ts = datetime.now(tz=timezone(timedelta(hours=3, minutes=30)))
with open("last update", "w", encoding="utf-8") as f:
    f.write(str(ts))
PY
fi
