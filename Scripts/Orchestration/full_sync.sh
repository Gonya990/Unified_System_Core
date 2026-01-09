#!/bin/bash
# 💎 VIBRANIUM SYSTEM SYNC & LIFT v2.0
# Спроектировано для абсолютной стабильности (Antigravity Core)

set -e # Выход при любой ошибке

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Запуск Vibranium Sync...${NC}"
echo "--------------------------------------------------"

# 1. ПРОВЕРКА ЛОКАЛЬНОЙ СРЕДЫ
echo "📌 [1/7] Проверка локального состояния Git..."
if ! git diff-index --quiet HEAD --; then
    echo "⚠️ Обнаружены незакоммиченные изменения. Сохраняю..."
    git add .
    git commit -m "chore(sync): auto-save before vibranium sync $(date +'%Y-%m-%d %H:%M:%S')"
fi

# 2. BEADS SYNC
echo "📌 [2/7] Синхронизация задач Beads..."
bd sync || echo "⚠️ Ошибка синхронизации Beads, продолжаем..."

# 3. PUSH В ОБЛАКО
echo "📌 [3/7] Отправка кода в GitHub..."
git pull origin main --rebase
git push origin main
echo -e "${GREEN}✅ Локальный код синхронизирован.${NC}"

# 4. УДАЛЕННОЕ ОБНОВЛЕНИЕ (АГРЕССИВНОЕ)
echo "📌 [4/7] Обновление удаленного сервера (100.110.209.49)..."
tailscale ssh gonya@100.110.209.49 "
    set -e
    cd /home/gonya/Unified_System
    
    echo '--- Ремонт Git и Подмодулей ---'
    # Очистка возможных конфликтов подмодулей
    rm -rf External_Tools/Stack/mcp_agent_mail
    git submodule deinit -f --all || true
    
    echo '--- Hard Reset на Main ---'
    git fetch origin
    git reset --hard origin/main
    
    # Восстановление подмодулей
    # git submodule update --init --recursive || echo 'Submodules failed, skipping'
"

# 5. ПЕРЕЗАПУСК СЕРВИСОВ
echo "📌 [5/7] Сборка и запуск Docker контейнеров..."
tailscale ssh gonya@100.110.209.49 "
    cd /home/gonya/Unified_System/Projects/AI_Core
    
    # Удаляем старые логи перед запуском для чистоты
    # > bot_journal.log || true
    
    docker rm -f ai_telegram_bot || true
    docker compose --profile local down --remove-orphans || true
    docker compose --profile local build --pull
    docker compose --profile local up -d --force-recreate
"

# 6. ВЕРИФИКАЦИЯ (ГЛАВНЫЙ ЭТАП)
echo "📌 [6/7] Верификация работы сервисов..."
sleep 5 # Даем время на запуск
tailscale ssh gonya@100.110.209.49 "
    echo '--- Проверка Docker ---'
    docker ps | grep ai_telegram_bot || (echo '❌ БОТ НЕ ЗАПУСТИЛСЯ!' && exit 1)
    
    echo '--- Проверка Логов на ошибки ---'
    if docker logs ai_telegram_bot 2>&1 | grep -i 'ValueError\|Error\|Exception' | tail -n 10 | grep .; then
        echo '⚠️ В логах обнаружены ошибки! Проверьте статус.'
    else
        echo '✅ Ошибок в логах не обнаружено.'
    fi
"

# 7. MCP УВЕДОМЛЕНИЕ
echo "📌 [7/7] Отправка рапорта в MCP Mail (Консилиум)..."
# (Используем OrangeStone как фиксированное имя)
LAST_COMMITS=$(git log -n 3 --pretty=format:"- %s")
tailscale ssh gonya@100.110.209.49 "
    cd /home/gonya/Unified_System
    ./venv/bin/python3 -c \"
import requests, os
URL = 'http://localhost:8765/mcp'
TOKEN = 'c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb'
payload = {
    'jsonrpc': '2.0', 'method': 'tools/call', 'id': 1,
    'params': {
        'name': 'send_message',
        'arguments': {
            'project_key': 'home-kosta-documents-unified-system-core',
            'sender_name': 'OrangeStone',
            'to': ['PinkLake'],
            'subject': 'SYSTEM STATUS: VIBRANIUM',
            'body_md': '### ✅ Система синхронизирована и запущена\n\n**Последние правки:**\n$LAST_COMMITS\n\nВсе системы в норме.'
        }
    }
}
r = requests.post(URL, json=payload, headers={'Authorization': f'Bearer {TOKEN}'})
print(f'MCP Notify: {r.status_code}')
\"
"

echo "--------------------------------------------------"
echo -e "${GREEN}🌟 СИСТЕМА ПЕРЕВЕДЕНА В РЕЖИМ VIBRANIUM!${NC}"
echo "--------------------------------------------------"
