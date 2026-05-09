#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

"$ROOT_DIR/fetch_every_4h.sh" &
FETCH_PID=$!
"$ROOT_DIR/serve_local_api.sh" &
API_PID=$!

cleanup() {
  for pid in "$FETCH_PID" "$API_PID"; do
    if [[ -n "${pid:-}" ]] && kill -0 "$pid" 2>/dev/null; then
      kill "$pid" 2>/dev/null || true
      wait "$pid" 2>/dev/null || true
    fi
  done
}

trap cleanup EXIT INT TERM
wait "$FETCH_PID" "$API_PID"
