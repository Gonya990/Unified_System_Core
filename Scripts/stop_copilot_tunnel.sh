#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="$ROOT_DIR/logs/cloudflared-copilot.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "No PID file found: $PID_FILE"
  exit 0
fi

PID="$(cat "$PID_FILE")"
if [[ -n "$PID" ]] && kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "Stopped cloudflared (PID $PID)"
else
  echo "Process not running (PID $PID)"
fi

rm -f "$PID_FILE"
