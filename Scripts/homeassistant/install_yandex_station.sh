#!/bin/bash
# Автоматическая установка Yandex.Station интеграции в Home Assistant
# Для использования: bash install_yandex_station.sh

set -e

echo "🎵 Установка Yandex.Station интеграции для Home Assistant"
echo "=========================================================="

# Проверка, что мы на правильном хосте
if [ ! -d "/config" ]; then
    echo "❌ Ошибка: Этот скрипт должен запускаться на сервере Home Assistant"
    echo "Текущий каталог: $(pwd)"
    exit 1
fi

# Проверка HACS
if [ ! -d "/config/custom_components/hacs" ]; then
    echo "⚠️  HACS не установлен!"
    echo "Установите HACS сначала: https://hacs.xyz/docs/setup/download"
    exit 1
fi

echo "✅ HACS найден"

# Создание директории для custom components
CUSTOM_DIR="/config/custom_components/yandex_station"
mkdir -p "$CUSTOM_DIR"

echo "📥 Скачивание последней версии Yandex.Station..."

# Скачивание с GitHub
LATEST_URL=$(curl -s https://api.github.com/repos/AlexxIT/YandexStation/releases/latest | grep "browser_download_url.*zip" | cut -d '"' -f 4)

if [ -z "$LATEST_URL" ]; then
    echo "❌ Не удалось получить URL последней версии"
    exit 1
fi

echo "📦 Загрузка: $LATEST_URL"
curl -L "$LATEST_URL" -o /tmp/yandex_station.zip

echo "📂 Распаковка..."
unzip -o /tmp/yandex_station.zip -d /config/custom_components/
rm /tmp/yandex_station.zip

echo "✅ Интеграция установлена!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 СЛЕДУЮЩИЕ ШАГИ:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. Перезагрузите Home Assistant:"
echo "   Настройки → Система → Перезагрузить"
echo ""
echo "2. После перезагрузки добавьте интеграцию:"
echo "   Настройки → Устройства и службы → + Добавить интеграцию"
echo "   Найдите: 'Yandex.Station'"
echo ""
echo "3. Авторизуйтесь через QR-код (рекомендуется)"
echo ""
echo "4. Готово! Станция появится как Media Player"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Полная документация:"
echo "   /home/gonya/Documents/Unified_System/Projects/AI_Core/docs/YANDEX_STATION_SETUP.md"
echo ""
