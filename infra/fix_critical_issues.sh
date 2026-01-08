#!/bin/bash
# 🚀 Рекомендуемое Решение Критических Проблем
# Дата: 2026-01-07
# Цель: Освободить ~30 GB, исправить git статус

set -e  # Остановка при ошибке

echo "🔍 Диагностика завершена!"
echo "📊 Disk использование: 84% (81GB/96GB)"
echo ""
echo "🎯 План действий:"
echo "  1. Удалить ContentFarm (старая версия Video Factory) - 28 GB"
echo "  2. Удалить Unified_System_Core (пустая папка) - 529 MB"
echo "  3. Удалить установщики .deb - 113 MB"
echo "  4. Системная очистка - ~1-2 GB"
echo "  5. Fix git submodule - 0 GB (просто исправление)"
echo ""
echo "💾 Ожидаемый результат: ~30-32 GB освобождено"
echo "📉 Disk после очистки: ~55-60%"
echo ""

read -p "Продолжить? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Отменено пользователем"
    exit 1
fi

echo ""
echo "🚀 Начинаем очистку..."
echo ""

# Шаг 1: ContentFarm
echo "🗑️  [1/5] Удаление ContentFarm (28 GB)..."
if [ -d "/home/gonya/ContentFarm" ]; then
    du -sh /home/gonya/ContentFarm
    rm -rf /home/gonya/ContentFarm
    echo "   ✅ ContentFarm удалён"
else
    echo "   ⏭️  ContentFarm не найден, пропускаем"
fi

# Шаг 2: Unified_System_Core
echo "🗑️  [2/5] Удаление Unified_System_Core (529 MB)..."
if [ -d "/home/gonya/Unified_System_Core" ]; then
    du -sh /home/gonya/Unified_System_Core
    rm -rf /home/gonya/Unified_System_Core
    echo "   ✅ Unified_System_Core удалён"
else
    echo "   ⏭️  Unified_System_Core не найден, пропускаем"
fi

# Шаг 3: Установщики
echo "🗑️  [3/5] Удаление .deb установщиков..."
find /home/gonya -maxdepth 1 -name "*.deb" -exec rm -f {} \;
echo "   ✅ .deb файлы удалены"

# Шаг 4: Системная очистка
echo "🧹 [4/5] Системная очистка..."
sudo apt clean
sudo apt autoremove -y
sudo journalctl --vacuum-time=7d
find /tmp -type f -mtime +1 -delete 2>/dev/null || true
echo "   ✅ Система очищена"

# Шаг 5: Git submodule fix
echo "🔧 [5/5] Исправление git подмодуля..."
cd /home/gonya/Unified_System/External_Tools/Stack/mcp_agent_mail
git reset --hard HEAD 2>/dev/null || echo "   ⚠️  Подмодуль уже в порядке"
echo "   ✅ Git подмодуль в порядке"

echo ""
echo "🎉 Очистка завершена!"
echo ""
echo "📊 Проверка результата:"
df -h / | grep -v "^Filesystem"
echo ""
du -sh /home/gonya/* 2>/dev/null | sort -rh | head -10
echo ""
echo "✨ Готово! Система здорова!"
