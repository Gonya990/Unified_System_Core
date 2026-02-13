#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/igorgoncharenko/Documents/Unified_System_Core"
ENV_FILE="$ROOT/Projects/AI_Core/.env"
SMOKE_SCRIPT="$ROOT/Scripts/smoke_hybrid_stack_v2.sh"
LOG_FILE="$ROOT/logs/smoke_weekly.log"
FORCE_OK="${1:-}"

mkdir -p "$ROOT/logs"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[FAIL] .env not found: $ENV_FILE"
  exit 1
fi

if [[ ! -x "$SMOKE_SCRIPT" ]]; then
  echo "[FAIL] smoke script not executable: $SMOKE_SCRIPT"
  exit 1
fi

get_env() {
  local key="$1"
  python3 - <<PY
from pathlib import Path
p=Path(r"$ENV_FILE")
val=""
for line in p.read_text(encoding='utf-8',errors='ignore').splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k,v=line.split('=',1)
        if k.strip()=="$key":
            val=v.strip()
            break
print(val)
PY
}

BOT_TOKEN="$(get_env TELEGRAM_BOT_TOKEN)"
CHAT_ID="$(get_env ADMIN_CHAT_ID)"
if [[ -z "$CHAT_ID" ]]; then
  CHAT_ID="$(get_env TELEGRAM_ADMIN_CHAT_ID)"
fi

TMP_OUT="$(mktemp)"
trap 'rm -f "$TMP_OUT"' EXIT

{
  echo ""
  echo "===== WEEKLY SMOKE RUN $(date '+%Y-%m-%d %H:%M:%S') ====="
  "$SMOKE_SCRIPT"
} 2>&1 | tee -a "$LOG_FILE" | tee "$TMP_OUT" >/dev/null

FAIL_LINES="$(grep '^\[FAIL\]' "$TMP_OUT" | head -n 12 || true)"

if [[ -n "$FAIL_LINES" ]]; then
  STATUS="FAIL"
else
  STATUS="OK"
fi

if [[ -z "$BOT_TOKEN" || -z "$CHAT_ID" ]]; then
  echo "[WARN] Telegram token/chat not configured, notification skipped"
  exit 0
fi

if [[ "$STATUS" == "FAIL" ]]; then
  MSG="🚨 WEEKLY SMOKE: FAIL\nHost: $(hostname)\nTime: $(date '+%Y-%m-%d %H:%M:%S')\n\n$FAIL_LINES\n\nLog: $LOG_FILE"
  curl -sS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${CHAT_ID}" \
    --data-urlencode "text=${MSG}" \
    >/dev/null || echo "[WARN] Failed to send Telegram alert"
  echo "[WARN] Weekly smoke failed, alert sent"
  exit 0
fi

# Weekly all-green summary (once a week) or manual force
if [[ "$FORCE_OK" == "--force-ok" || "$(date +%u)" == "7" ]]; then
  OK_MSG="✅ WEEKLY SMOKE: ALL GREEN\nHost: $(hostname)\nTime: $(date '+%Y-%m-%d %H:%M:%S')\n\nFactory: OK\nCrypto: OK\nHA: OK\n\nLog: $LOG_FILE"
  curl -sS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${CHAT_ID}" \
    --data-urlencode "text=${OK_MSG}" \
    >/dev/null || echo "[WARN] Failed to send Telegram weekly summary"
  echo "[OK] Weekly all-green summary sent"
else
  echo "[OK] Weekly smoke passed, summary not scheduled for today"
fi
