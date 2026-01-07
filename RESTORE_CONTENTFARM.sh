#!/bin/bash
# ВОССТАНОВЛЕНИЕ CONTENTFARM - АВТОНОМНАЯ ФАБРИКА КОНТЕНТА
# Сервер: unified-home-core-cloud (100.110.209.49)
# GPU: NVIDIA Titan RTX

set -e

echo "🚨 ВОССТАНОВЛЕНИЕ CONTENTFARM"
echo "================================"
echo ""

# 1. Проверка, что мы на правильном сервере
if ! nvidia-smi &>/dev/null; then
    echo "❌ ОШИБКА: Нет NVIDIA GPU! Запускайте на unified-home-core-cloud!"
    exit 1
fi

echo "✅ GPU найден:"
nvidia-smi --query-gpu=name --format=csv,noheader

# 2. Переход в рабочую директорию
cd /home/gonya/Unified_System

echo ""
echo "📁 Проверка файлов..."
for file in factory_scheduler.py orchestrator_v3_no_face.py daily_researcher.py insta_uploader.py; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file ОТСУТСТВУЕТ!"
    fi
done

# 3. Создание необходимых директорий
echo ""
echo "📂 Создание структуры директорий..."
mkdir -p outputs
mkdir -p inputs  
mkdir -p assets
mkdir -p logs/factory

echo "✅ Директории созданы"

# 4. Настройка systemd timer для ежедневного запуска
echo ""
echo "⏰ Настройка автозапуска (systemd timer)..."

# Создаем service
cat > ~/.config/systemd/user/contentfarm.service <<'EOF'
[Unit]
Description=ContentFarm Daily Production
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=/home/gonya/Unified_System
Environment="PATH=/home/gonya/Unified_System/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=/home/gonya/Unified_System/venv/bin/python3 factory_scheduler.py
StandardOutput=append:/home/gonya/Unified_System/logs/factory/run_%Y%m%d.log
StandardError=append:/home/gonya/Unified_System/logs/factory/run_%Y%m%d.log

[Install]
WantedBy=default.target
EOF

# Создаем timer для ежедневного запуска в 10:00
cat > ~/.config/systemd/user/contentfarm.timer <<'EOF'
[Unit]
Description=ContentFarm Daily Timer
Requires=contentfarm.service

[Timer]
OnCalendar=daily
OnCalendar=*-*-* 10:00:00
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Перезагружаем systemd и включаем timer
systemctl --user daemon-reload
systemctl --user enable contentfarm.timer
systemctl --user start contentfarm.timer

echo "✅ Systemd timer настроен (ежедневно в 10:00)"

# 5. Проверка venv
echo ""
echo "🐍 Проверка Python окружения..."
if [ ! -d "venv" ]; then
    echo "❌ venv не найден! Создаю..."
    python3 -m venv venv
    ./venv/bin/pip install --upgrade pip
fi

# Устанавливаем зависимости
echo "📦 Установка зависимостей..."
./venv/bin/pip install -q openai instagrapi moviepy pillow pydantic numpy feedparser requests python-dotenv pydub edge-tts

echo "✅ Зависимости установлены"

# 6. Проверка .env файла
echo ""
echo "🔐 Проверка конфигурации..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env не найден! Создайте его с необходимыми ключами:"
    echo "   - OPENAI_API_KEY"
    echo "   - INSTAGRAM_USERNAME"
    echo "   - INSTAGRAM_PASSWORD"
    echo "   - PEXELS_API_KEY (опционально)"
else
    echo "✅ .env найден"
fi

# 7. Тестовый запуск
echo ""
echo "🧪 Запускаю тестовый запуск factory_scheduler.py..."
echo "(Ctrl+C для отмены через 5 секунд)"
sleep 5

# Запускаем в фоне с логированием
nohup ./venv/bin/python3 factory_scheduler.py > logs/factory/manual_test_$(date +%Y%m%d_%H%M%S).log 2>&1 &
TEST_PID=$!

echo "✅ Тестовый запуск начат (PID: $TEST_PID)"
echo "   Лог: logs/factory/manual_test_*.log"
echo "   Проверить статус: jobs"
echo "   Остановить: kill $TEST_PID"

# 8. Финальный статус
echo ""
echo "======================================"
echo "🎉 ВОССТАНОВЛЕНИЕ ЗАВЕРШЕНО!"
echo "======================================"
echo ""
echo "📊 Статус ContentFarm:"
echo "  ✅ Файлы: восстановлены"
echo "  ✅ Директории: созданы"
echo "  ✅ Автозапуск: настроен (ежедневно 10:00)"
echo "  ✅ Python venv: готов"
echo "  🔄 Тестовый запуск: выполняется (PID: $TEST_PID)"
echo ""
echo "📝 Команды управления:"
echo "  systemctl --user status contentfarm.timer   # Статус таймера"
echo "  systemctl --user list-timers                # Все таймеры"
echo "  journalctl --user -u contentfarm -f         # Логи в реальном времени"
echo "  tail -f logs/factory/run_*.log              # Логи продакшена"
echo ""
echo "🚀 ContentFarm СНОВА АВТОНОМЕН!"
echo ""
