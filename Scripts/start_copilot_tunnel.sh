#!/usr/bin/env bash
set -euo pipefail

IP="$(ipconfig getifaddr en0 || ipconfig getifaddr en1 || true)"
if [[ -z "$IP" ]]; then
  echo "No LAN IP found (en0/en1)."
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/cloudflared-copilot.log"
PID_FILE="$LOG_DIR/cloudflared-copilot.pid"

nohup /opt/homebrew/bin/cloudflared tunnel --url "http://$IP:3030" --no-autoupdate --logfile "$LOG_FILE" --loglevel info >/dev/null 2>&1 &

echo $! > "$PID_FILE"

echo "cloudflared started (PID $(cat "$PID_FILE"))"
echo "Public URL will appear in: $LOG_FILE"
echo "Look for https://*.trycloudflare.com"
