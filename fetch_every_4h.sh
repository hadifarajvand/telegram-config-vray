#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_ACTIVATE="$ROOT_DIR/.venvmac/bin/activate"
PYTHON_ENTRY="${PYTHON_ENTRY:-main.py}"
INTERVAL_SECONDS="${INTERVAL_SECONDS:-14400}"

if [[ ! -f "$VENV_ACTIVATE" ]]; then
  echo "Missing virtualenv activation script: $VENV_ACTIVATE" >&2
  exit 1
fi

cd "$ROOT_DIR"
source "$VENV_ACTIVATE"

if [[ ! -f "$PYTHON_ENTRY" ]]; then
  echo "Missing Python entrypoint: $ROOT_DIR/$PYTHON_ENTRY" >&2
  exit 1
fi

while true; do
  python "$PYTHON_ENTRY"
  printf 'refreshed feeds at %s\n' "$(date '+%Y-%m-%d %H:%M:%S %Z')"
  sleep "$INTERVAL_SECONDS"
done
