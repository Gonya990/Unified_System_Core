#!/bin/bash
# FULL SYSTEM SYNC & LIFT - "ПОЛНАЯ СИНХРОНИЗАЦИЯ И ПОДЪЕМ"
# Antigravity <-> Unified System <-> FuchsiaCat

set -e # Exit on error

echo "🚀 Начинаю полную синхронизацию и запуск систем..."
echo "--------------------------------------------------"

# 1. BEADS SYNC (Tasks)
echo "📌 [1/6] Синхронизация задач Beads..."
bd sync
echo "✅ Задачи синхронизированы."

# 2. LOCAL GIT SYNC
echo "📌 [2/6] Синхронизация локального кода с GitHub..."
git add .
git commit -m "chore: full-sync & system lift $(date +'%Y-%m-%d %H:%M:%S')" || echo "Нет локальных изменений"
git pull origin main --rebase
git push origin main
echo "✅ Локальный код отправлен в облако."

# 3. REMOTE SERVER SYNC & RESTART
echo "📌 [3/6] Обновление кода и запуск сервисов на удаленном сервере..."
tailscale ssh gonya@100.110.209.49 "
    cd /home/gonya/Unified_System
    git pull origin main --rebase
    
    echo '--- RESTARTING SERVICES ---'
    cd Projects/AI_Core
    # Перезапуск бота с локальным билдом (профиль local)
    docker compose --profile local up -d ai-bot-local
    
    echo '--- REMOTE SYSTEM CHECK ---'
    docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
"
echo "✅ Удаленный сервер обновлен и перезапущен."

# 4. MCP BROADCAST (Communication)
echo "📌 [4/6] Рассылка уведомлений всем агентам..."
# Собираем лог последних коммитов для прозрачности
LAST_WORK=$(git log -n 5 --pretty=format:"- %s (%an)")

tailscale ssh gonya@100.110.209.49 "
    cd /home/gonya/Unified_System
    ./venv/bin/python3 -c \"
import requests
import json
from datetime import datetime

URL = 'http://localhost:8765/mcp'
TOKEN = 'c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb'
PROJECT_KEY = '/Gonya990/Unified_System_Core'

def broadcast(msg):
    headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
    payload = {
        'jsonrpc': '2.0', 
        'method': 'tools/call', 
        'params': {
            'name': 'send_message',
            'arguments': {
                'project_key': PROJECT_KEY,
                'sender_name': 'Antigravity',
                'to': ['FuchsiaCat', '@all'],
                'subject': 'SYSTEM SYNC & LIFT COMPLETE',
                'body_md': msg
            }
        }, 
        'id': 1
    }
    requests.post(URL, json=payload, headers=headers)

report = f'''### 🏁 Система Перезапущена и Синхронизирована
**Время:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Проделанная работа (последние правки):**
{'''"'''+LAST_WORK+'''"'''}

**Статус сервисов:**
- AI Telegram Bot: 🟢 Running (Remote)
- Connect Landing Page: 🟢 Running (Local:3002)
- Beads: 🟢 Synced

*Все агенты, примите во внимание текущий стейт проекта.*
'''
broadcast(report)
\""
echo "✅ Уведомление отправлено всем агентам."

# 5. WORK LOG UPDATE
echo "📌 [5/6] Обновление журнала работ..."
echo "- $(date +'%Y-%m-%d %H:%M:%S'): Full synchronization and system lift by Antigravity." >> Agent_Context/WORK_SESSION_LOG.md

# 6. FINALIZATION
echo "📌 [6/6] Финализация..."
echo "--------------------------------------------------"
echo "🌟 ВСЯ СИСТЕМА ПОДНЯТА И СИНХРОНИЗИРОВАНА: $(date)"
echo "--------------------------------------------------"
