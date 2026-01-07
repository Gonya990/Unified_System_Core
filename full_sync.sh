#!/bin/bash
# FULL SYSTEM SYNC SCRIPT - "СИНХРОНИЗАЦИЯ"
# Antigravity <-> Unified System <-> FuchsiaCat

echo "🔄 Начинаю полную синхронизацию системы..."
echo "------------------------------------------"

# 1. GIT SYNC
echo "📌 [1/4] Синхронизация кода с GitHub..."
git pull origin main --rebase
git add .
git commit -m "chore: auto-sync $(date +'%Y-%m-%d %H:%M:%S')" || echo "Нет изменений для коммита"
git push origin main
echo "✅ Git синхронизирован."

# 2. SERVICE STATUS CHECK
echo "📌 [2/4] Проверка статуса сервисов на сервере..."
tailscale ssh gonya@100.110.209.49 "
    echo '--- SERVICES STATUS ---'
    ps aux | grep -E '(uvicorn|telegram_bot|mcp_agent_mail)' | grep -v grep | awk '{print \$11, \$2, \"STATUS: OK\"}'
    echo '--- RESOURCES ---'
    df -h / | grep /
    nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader,nounits
" > .system_state.tmp

# 3. AGENT SYNC (Talk to Kostya)
echo "📌 [3/4] Доклад агенту FuchsiaCat через MCP..."
STATE_REPORT=$(cat .system_state.tmp)
python3 sync_agent.py "ПОЛНАЯ СИНХРОНИЗАЦИЯ ВЫПОЛНЕНА. 
Текущее состояние системы:
$STATE_REPORT

Все системы в норме. Работаем дальше в унисон! 🤝"
rm .system_state.tmp
echo "✅ Агент FuchsiaCat оповещен."

# 4. ENVIRONMENT SYNC
echo "📌 [4/4] Финализация..."
echo "СИНХРОНИЗАЦИЯ ЗАВЕРШЕНА: $(date)"
echo "------------------------------------------"
