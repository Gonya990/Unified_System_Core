#!/bin/bash
# Master Automation Controller
# Главный контроллер автоматизации

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIFIED_SYSTEM="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║   Unified System - Master Automation                         ║"
echo "║   Унифицированная система - Главная автоматизация           ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🕐 Starting automation cycle at $(date)"
echo "🕐 Запуск цикла автоматизации: $(date)"
echo ""

# Make scripts executable
chmod +x "$SCRIPT_DIR"/*.sh

# Run all automation scripts
echo "═══════════════════════════════════════════════════════════════"
echo "1/3 - ChatGPT Integration | Интеграция с ChatGPT"
echo "═══════════════════════════════════════════════════════════════"
"$SCRIPT_DIR/chatgpt_integration.sh"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "2/3 - CV Synchronization | Синхронизация CV"
echo "═══════════════════════════════════════════════════════════════"
"$SCRIPT_DIR/cv_sync.sh" --auto-update

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "3/3 - GitHub ↔ ChatGPT Monitor | Монитор GitHub ↔ ChatGPT"
echo "═══════════════════════════════════════════════════════════════"
"$SCRIPT_DIR/github_chatgpt_monitor.sh"

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║   ✅ Automation cycle completed successfully                 ║"
echo "║   ✅ Цикл автоматизации завершен успешно                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary | Сводка:"
echo "   - ChatGPT Integration: ✅ Complete"
echo "   - CV Sync: ✅ Complete"  
echo "   - GitHub Monitor: ✅ Complete"
echo ""
echo "🕐 Finished at $(date)"
echo ""
echo "Next run: Check cron schedule"
echo "Следующий запуск: Проверьте расписание cron"
