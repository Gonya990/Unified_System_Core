#!/bin/bash
# SmartThings InstalledApps Cleanup Script
# Automatically finds and removes old Home Assistant integrations

set -e

echo "======================================================================="
echo "🏠 SmartThings InstalledApps Cleanup Tool"
echo "======================================================================="
echo ""

# Check if SmartThings CLI is installed
if ! command -v smartthings &> /dev/null; then
    echo "❌ SmartThings CLI не установлен!"
    echo ""
    echo "Установите с помощью:"
    echo "  npm install -g @smartthings/cli"
    echo ""
    exit 1
fi

echo "✅ SmartThings CLI найден"
echo ""

# Check if logged in
if ! smartthings locations:list &> /dev/null; then
    echo "❌ Вы не авторизованы в SmartThings CLI"
    echo ""
    echo "Выполните:"
    echo "  smartthings login"
    echo ""
    exit 1
fi

echo "✅ Авторизация подтверждена"
echo ""

# Get list of all InstalledApps
echo "🔍 Поиск InstalledApps..."
echo ""

# List all installed apps and filter for Home Assistant
APPS_JSON=$(smartthings apps:installed:list --json 2>/dev/null || echo "[]")

if [ "$APPS_JSON" == "[]" ]; then
    echo "❌ Не удалось получить список приложений"
    echo "Попробуйте вручную: smartthings apps:installed:list"
    exit 1
fi

# Count Home Assistant apps
HA_COUNT=$(echo "$APPS_JSON" | jq '[.[] | select(.displayName | contains("Home Assistant"))] | length')

echo "Найдено приложений Home Assistant: $HA_COUNT"
echo ""

if [ "$HA_COUNT" -eq 0 ]; then
    echo "✅ Приложения Home Assistant не найдены"
    echo "Возможно, проблема в другом. Проверьте:"
    echo "  smartthings apps:installed:list"
    exit 0
fi

if [ "$HA_COUNT" -eq 1 ]; then
    echo "✅ Найдено только одно приложение Home Assistant"
    echo "Это нормально. Проблема может быть в другом."
    echo ""
    echo "Попробуйте перезагрузить интеграцию в Home Assistant:"
    echo "  Настройки → Устройства и Сервисы → SmartThings → Reload"
    exit 0
fi

# Multiple Home Assistant apps found
echo "⚠️  ВНИМАНИЕ: Найдено несколько ($HA_COUNT) приложений Home Assistant!"
echo "Это может вызывать ошибку 'Reached limit of subscriptions'"
echo ""

# Display all Home Assistant apps
echo "Список приложений:"
echo "======================================================================="
echo "$APPS_JSON" | jq -r '.[] | select(.displayName | contains("Home Assistant")) | "ID: \(.installedAppId)\nName: \(.displayName)\nStatus: \(.installedAppStatus)\nCreated: \(.createdDate // "N/A")\n---"'
echo "======================================================================="
echo ""

# Ask user which apps to keep
echo "Рекомендация: Оставьте только ОДНО самое новое приложение"
echo ""

read -p "Показать детали каждого приложения? (y/n): " SHOW_DETAILS

if [ "$SHOW_DETAILS" == "y" ]; then
    echo ""
    echo "$APPS_JSON" | jq -r '.[] | select(.displayName | contains("Home Assistant")) | "═══════════════════════════════════════════════════════════════════════\nID: \(.installedAppId)\nName: \(.displayName)\nApp ID: \(.appId)\nStatus: \(.installedAppStatus)\nLocation: \(.locationId)\nCreated: \(.createdDate // \"N/A\")\n═══════════════════════════════════════════════════════════════════════\n"'
fi

echo ""
read -p "Автоматически удалить старые приложения? (y/n): " AUTO_DELETE

if [ "$AUTO_DELETE" != "y" ]; then
    echo ""
    echo "Ручное удаление:"
    echo "  1. Выберите ID приложения для удаления из списка выше"
    echo "  2. Выполните: smartthings apps:installed:delete <ID>"
    echo ""
    echo "Или запустите этот скрипт снова и выберите 'y'"
    exit 0
fi

# Auto-delete mode
echo ""
echo "🗑️  Режим автоматического удаления"
echo ""

# Get all HA app IDs sorted by creation date (keep newest)
APP_IDS=$(echo "$APPS_JSON" | jq -r '[.[] | select(.displayName | contains("Home Assistant"))] | sort_by(.createdDate) | reverse | .[1:] | .[].installedAppId')

if [ -z "$APP_IDS" ]; then
    echo "❌ Не удалось определить, какие приложения удалить"
    exit 1
fi

echo "Будут удалены следующие приложения (оставлено самое новое):"
echo "$APP_IDS"
echo ""

read -p "Подтвердите удаление (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Отменено пользователем"
    exit 0
fi

# Delete old apps
echo ""
DELETED=0
FAILED=0

for APP_ID in $APP_IDS; do
    echo "🗑️  Удаляю $APP_ID..."
    
    if smartthings apps:installed:delete "$APP_ID" --force 2>/dev/null; then
        echo "   ✅ Успешно удалено"
        ((DELETED++))
    else
        echo "   ❌ Ошибка удаления"
        ((FAILED++))
    fi
    
    sleep 1
done

echo ""
echo "======================================================================="
echo "📊 РЕЗУЛЬТАТЫ"
echo "======================================================================="
echo "Удалено успешно: $DELETED"
echo "Ошибок: $FAILED"
echo ""

if [ "$FAILED" -eq 0 ]; then
    echo "✅ Очистка завершена успешно!"
    echo ""
    echo "Следующие шаги:"
    echo "  1. Откройте Home Assistant"
    echo "  2. Настройки → Устройства и Сервисы → SmartThings"
    echo "  3. Нажмите 'Reload' (перезагрузить интеграцию)"
    echo "  4. Проверьте, что все устройства доступны"
else
    echo "⚠️  Некоторые приложения не удалось удалить"
    echo "Попробуйте удалить их вручную:"
    echo "  smartthings apps:installed:list"
    echo "  smartthings apps:installed:delete <ID>"
fi

echo ""
echo "======================================================================="
