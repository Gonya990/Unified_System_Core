#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/igorgoncharenko/Documents/Unified_System_Core"
ENV_FILE="$ROOT/Projects/AI_Core/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[FAIL] .env not found: $ENV_FILE"
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

FACTORY_REMOTE_HOST="$(get_env FACTORY_REMOTE_HOST)"
FACTORY_REMOTE_USER="$(get_env FACTORY_REMOTE_USER)"
FACTORY_REMOTE_ROOT="$(get_env FACTORY_REMOTE_ROOT)"
CRYPTO_BOT_LOG_PATH="$(get_env CRYPTO_BOT_LOG_PATH)"
HA_URL="$(get_env HA_URL)"
CRYPTO_MIN_BALANCE_USDT="$(get_env CRYPTO_MIN_BALANCE_USDT)"
CRYPTO_MIN_TOTAL_EQUITY_USD="$(get_env CRYPTO_MIN_TOTAL_EQUITY_USD)"
if [[ -z "$CRYPTO_MIN_TOTAL_EQUITY_USD" ]]; then
  if [[ -n "$CRYPTO_MIN_BALANCE_USDT" ]]; then
    CRYPTO_MIN_TOTAL_EQUITY_USD="$CRYPTO_MIN_BALANCE_USDT"
  else
    CRYPTO_MIN_TOTAL_EQUITY_USD="10"
  fi
fi

echo "== ENV CHECK =="
for k in FACTORY_REMOTE_HOST FACTORY_REMOTE_USER FACTORY_REMOTE_ROOT CRYPTO_BOT_LOG_PATH HA_URL; do
  v="$(get_env "$k")"
  if [[ -n "$v" ]]; then
    echo "[OK] $k"
  else
    echo "[MISS] $k"
  fi
done

echo
REMOTE="${FACTORY_REMOTE_USER}@${FACTORY_REMOTE_HOST}"
FACTORY_SCRIPT="${FACTORY_REMOTE_ROOT}/Projects/Content_Factory/src/pipeline/factory_scheduler.py"

echo "== CLOUD FACTORY CHECK =="
if ssh "$REMOTE" "test -f '$FACTORY_SCRIPT'"; then
  echo "[OK] Factory script exists: $FACTORY_SCRIPT"
else
  echo "[FAIL] Factory script missing: $FACTORY_SCRIPT"
fi

echo
echo "== CRYPTO CHECK =="
REMOTE_ENV_FILE="${FACTORY_REMOTE_ROOT}/Projects/AI_Core/.env"
ssh "$REMOTE" CRYPTO_LOG_PATH="$CRYPTO_BOT_LOG_PATH" MIN_BAL="$CRYPTO_MIN_TOTAL_EQUITY_USD" REMOTE_ENV_FILE="$REMOTE_ENV_FILE" 'bash -s' <<'EOS'
set -euo pipefail

PROC_COUNT=$(pgrep -af 'bybit_trading_bot.py|crypto' | wc -l | tr -d ' ')
if [ "$PROC_COUNT" -gt 0 ]; then
  echo "[OK] Crypto process running ($PROC_COUNT match(es))"
else
  echo "[FAIL] Crypto process not running"
fi

LOGS=""
if [ -f "$CRYPTO_LOG_PATH" ]; then
  LOGS="$CRYPTO_LOG_PATH"
fi
if [ -f /home/gonya/.pm2/logs/crypto-bot-out.log ]; then
  LOGS="$LOGS /home/gonya/.pm2/logs/crypto-bot-out.log"
fi
if [ -f /home/gonya/.pm2/logs/crypto-bot-error.log ]; then
  LOGS="$LOGS /home/gonya/.pm2/logs/crypto-bot-error.log"
fi

if [ -n "$LOGS" ]; then
  echo "[OK] Logs available:$LOGS"
else
  echo "[FAIL] Crypto logs missing"
fi

BAL=$(grep -hEo 'Balance: [^ ]+ USDT' $LOGS 2>/dev/null | tail -n 1 || true)
EQUITY_CHECK_OUTPUT="$(python3 - <<'PY'
import os

def parse_env(path: str):
    env = {}
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k, v = line.split('=', 1)
                env[k.strip()] = v.strip()
    except Exception:
        pass
    return env

min_bal_raw = os.environ.get('MIN_BAL', '10').strip() or '10'
try:
    min_bal = float(min_bal_raw)
except Exception:
    min_bal = 10.0

env_file = os.environ.get('REMOTE_ENV_FILE', '').strip()
file_env = parse_env(env_file) if env_file else {}
api_key = os.environ.get('BYBIT_API_KEY') or file_env.get('BYBIT_API_KEY', '')
api_secret = os.environ.get('BYBIT_API_SECRET') or file_env.get('BYBIT_API_SECRET', '')
testnet_val = (os.environ.get('BYBIT_TESTNET') or file_env.get('BYBIT_TESTNET', 'true')).lower()
testnet = testnet_val == 'true'

if not api_key or not api_secret:
    print('STATUS=NO_API_CREDENTIALS')
    raise SystemExit(0)

try:
    from pybit.unified_trading import HTTP
except Exception:
    print('STATUS=NO_PYBIT')
    raise SystemExit(0)

try:
    session = HTTP(testnet=testnet, api_key=api_key, api_secret=api_secret)
    res = session.get_wallet_balance(accountType='UNIFIED')
except Exception:
    print('STATUS=API_ERROR')
    raise SystemExit(0)

if not isinstance(res, dict) or res.get('retCode') != 0:
    print('STATUS=API_BAD_RESPONSE')
    raise SystemExit(0)

items = (((res.get('result') or {}).get('list')) or [])
if not items:
    print('STATUS=API_EMPTY')
    raise SystemExit(0)

wallet = items[0] or {}
try:
    equity = float(wallet.get('totalEquity') or 0)
except Exception:
    equity = 0.0

coins = wallet.get('coin') or []
rows = []
for c in coins:
    try:
        wb = float(c.get('walletBalance') or 0)
    except Exception:
        wb = 0.0
    try:
        uv = float(c.get('usdValue') or 0)
    except Exception:
        uv = 0.0
    if wb <= 0 and uv <= 0:
        continue
    rows.append((c.get('coin', '?'), wb, uv))

rows.sort(key=lambda x: x[2], reverse=True)
preview = ', '.join([f"{coin}:{wb:.6f} (~${uv:.2f})" for coin, wb, uv in rows[:8]])
print('STATUS=OK')
print(f'EQUITY={equity:.8f}')
print(f'THRESHOLD={min_bal:.8f}')
print('COINS=' + preview)
PY
)"

if echo "$EQUITY_CHECK_OUTPUT" | grep -q '^STATUS=OK$'; then
  EQUITY_VAL="$(echo "$EQUITY_CHECK_OUTPUT" | awk -F= '/^EQUITY=/{print $2}' | tail -n1)"
  COINS_PREVIEW="$(echo "$EQUITY_CHECK_OUTPUT" | sed -n 's/^COINS=//p' | tail -n1)"
  if [ -n "$EQUITY_VAL" ]; then
    echo "[OK] Total wallet equity: \$$EQUITY_VAL (all coins, USD equivalent)"
    if [ -n "$COINS_PREVIEW" ]; then
      echo "[OK] Coins snapshot: $COINS_PREVIEW"
    fi
    if awk -v b="$EQUITY_VAL" -v t="$MIN_BAL" 'BEGIN {exit !(b < t)}'; then
      echo "[FAIL] Total equity below threshold: \$$EQUITY_VAL < \$$MIN_BAL"
    else
      echo "[OK] Equity threshold met: \$$EQUITY_VAL >= \$$MIN_BAL"
    fi
  else
    echo "[WARN] Could not parse total equity value"
  fi
else
  STATUS_LINE="$(echo "$EQUITY_CHECK_OUTPUT" | awk -F= '/^STATUS=/{print $2}' | tail -n1)"
  if [ -n "$STATUS_LINE" ]; then
    echo "[WARN] API equity check unavailable ($STATUS_LINE), fallback to logs"
  else
    echo "[WARN] API equity check unavailable, fallback to logs"
  fi

  if [ -n "$BAL" ]; then
    echo "[OK] Last $BAL"
    BAL_NUM=$(echo "$BAL" | sed -E 's/.*\$([0-9.]+).*/\1/' || true)
    if [ -n "$BAL_NUM" ]; then
      if awk -v b="$BAL_NUM" -v t="$MIN_BAL" 'BEGIN {exit !(b < t)}'; then
        echo "[FAIL] Balance below threshold (USDT fallback): $BAL_NUM < $MIN_BAL"
      else
        echo "[OK] Balance threshold met (USDT fallback): $BAL_NUM >= $MIN_BAL"
      fi
    else
      echo "[WARN] Could not parse numeric balance"
    fi
  else
    echo "[WARN] Balance metric not found in logs"
  fi
fi

MKT=$(grep -hEo 'Market: RSI=[0-9.]+, SMA_short=[0-9.]+, SMA_long=[0-9.]+' $LOGS 2>/dev/null | tail -n 1 || true)
if [ -n "$MKT" ]; then
  echo "[OK] Last $MKT"
else
  echo "[WARN] Market metric not found in logs"
fi
EOS

echo
echo "== HA NETWORK CHECK (from this node) =="
python3 - <<PY
from pathlib import Path
from urllib.parse import urlparse
import socket
p=Path(r"$ENV_FILE")
env={}
for line in p.read_text(encoding='utf-8',errors='ignore').splitlines():
    if '=' in line and not line.strip().startswith('#'):
        k,v=line.split('=',1)
        env[k.strip()]=v.strip()
url=env.get('HA_URL','').strip()
if not url:
    print('[FAIL] HA_URL missing')
else:
    u=urlparse(url)
    host=u.hostname
    port=u.port or (443 if u.scheme=='https' else 80)
    s=socket.socket()
    s.settimeout(5)
    try:
        s.connect((host,port))
        print(f'[OK] TCP reachable: {host}:{port}')
    except Exception as e:
        print(f'[FAIL] TCP unreachable: {host}:{port} ({e})')
    finally:
        s.close()
PY

echo
echo "== HA API CHECK (from Cloud Server) =="
ssh "$REMOTE" "python3 -c \"import requests; url='${HA_URL}'.rstrip('/'); token='$(get_env HA_TOKEN)'; r=requests.get(url + '/api/', headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'}, timeout=8); print('[OK] Cloud -> HA HTTP 200 ('+url+')' if r.status_code==200 else '[FAIL] Cloud -> HA HTTP '+str(r.status_code)+' ('+url+')')\"" || echo "[FAIL] Cloud -> HA request failed"

echo
echo "Smoke check complete."
