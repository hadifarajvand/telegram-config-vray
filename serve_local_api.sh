#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_ACTIVATE="$ROOT_DIR/.venvmac/bin/activate"
API_BIND="${API_BIND:-0.0.0.0}"
API_PORT="${API_PORT:-8888}"

if [[ ! -f "$VENV_ACTIVATE" ]]; then
  echo "Missing virtualenv activation script: $VENV_ACTIVATE" >&2
  exit 1
fi

cd "$ROOT_DIR"
source "$VENV_ACTIVATE"
exec python -u -m api.server
