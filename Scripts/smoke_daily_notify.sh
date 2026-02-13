#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/igorgoncharenko/Documents/Unified_System_Core"
ENV_FILE="$ROOT/Projects/AI_Core/.env"
SMOKE_SCRIPT="$ROOT/Scripts/smoke_hybrid_stack_v2.sh"
LOG_FILE="$ROOT/logs/smoke_daily.log"

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

FACTORY_REMOTE_HOST="$(get_env FACTORY_REMOTE_HOST)"
FACTORY_REMOTE_USER="$(get_env FACTORY_REMOTE_USER)"
AUTO_HEAL_CRYPTO_ON_FAIL="$(get_env AUTO_HEAL_CRYPTO_ON_FAIL)"
if [[ -z "$AUTO_HEAL_CRYPTO_ON_FAIL" ]]; then
  AUTO_HEAL_CRYPTO_ON_FAIL="true"
fi
AUTO_HEAL_COOLDOWN_MINUTES="$(get_env AUTO_HEAL_COOLDOWN_MINUTES)"
if [[ -z "$AUTO_HEAL_COOLDOWN_MINUTES" ]]; then
  AUTO_HEAL_COOLDOWN_MINUTES="60"
fi
AUTOHEAL_STAMP_FILE="$ROOT/logs/.autoheal_crypto_last_ts"

TMP_OUT="$(mktemp)"
trap 'rm -f "$TMP_OUT"' EXIT

{
  echo ""
  echo "===== DAILY SMOKE RUN $(date '+%Y-%m-%d %H:%M:%S') ====="
  "$SMOKE_SCRIPT"
} 2>&1 | tee -a "$LOG_FILE" | tee "$TMP_OUT" >/dev/null

FAIL_LINES="$(grep '^\[FAIL\]' "$TMP_OUT" | head -n 12 || true)"

if [[ -n "$FAIL_LINES" ]]; then
  echo "[WARN] Smoke detected FAIL status"

  AUTOHEAL_NOTE=""
  if [[ "$AUTO_HEAL_CRYPTO_ON_FAIL" == "true" ]] && echo "$FAIL_LINES" | grep -Eq 'Crypto process not running|Crypto logs missing'; then
    if [[ -n "$FACTORY_REMOTE_HOST" && -n "$FACTORY_REMOTE_USER" ]]; then
      REMOTE="${FACTORY_REMOTE_USER}@${FACTORY_REMOTE_HOST}"
      NOW_TS="$(date +%s)"
      LAST_TS="0"
      if [[ -f "$AUTOHEAL_STAMP_FILE" ]]; then
        LAST_TS="$(cat "$AUTOHEAL_STAMP_FILE" 2>/dev/null || echo 0)"
      fi
      COOLDOWN_SEC=$((AUTO_HEAL_COOLDOWN_MINUTES * 60))
      ELAPSED=$((NOW_TS - LAST_TS))
      if [[ "$ELAPSED" -ge "$COOLDOWN_SEC" ]]; then
        if ssh "$REMOTE" "pm2 restart crypto-bot >/tmp/crypto_autofix.log 2>&1 && echo OK || echo FAIL" | grep -q '^OK$'; then
          echo "$NOW_TS" > "$AUTOHEAL_STAMP_FILE"
          AUTOHEAL_NOTE="\\n\\n🛠 Auto-heal: crypto-bot restart sent (pm2)."
        else
          AUTOHEAL_NOTE="\\n\\n⚠️ Auto-heal failed: pm2 restart crypto-bot"
        fi
      else
        LEFT_SEC=$((COOLDOWN_SEC - ELAPSED))
        LEFT_MIN=$(( (LEFT_SEC + 59) / 60 ))
        AUTOHEAL_NOTE="\\n\\n⏳ Auto-heal cooldown active: ${LEFT_MIN} min left"
      fi
    else
      AUTOHEAL_NOTE="\\n\\n⚠️ Auto-heal skipped: FACTORY_REMOTE_* not configured"
    fi
  fi

  if [[ -n "$BOT_TOKEN" && -n "$CHAT_ID" ]]; then
    MSG="🚨 DAILY SMOKE: FAIL\nHost: $(hostname)\nTime: $(date '+%Y-%m-%d %H:%M:%S')\n\n$FAIL_LINES\n\nLog: $LOG_FILE$AUTOHEAL_NOTE"

    curl -sS -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
      --data-urlencode "chat_id=${CHAT_ID}" \
      --data-urlencode "text=${MSG}" \
      >/dev/null || echo "[WARN] Failed to send Telegram alert"
  else
    echo "[WARN] Telegram token/chat not configured, alert skipped"
  fi
else
  echo "[OK] Smoke run passed. No Telegram alert sent."
fi
