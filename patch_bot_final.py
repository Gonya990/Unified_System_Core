import sys, os, re
from datetime import datetime

def patch_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # 1. Update show_advanced_help with TRIPLE quotes to avoid newline issues
    new_help_func = """async def show_advanced_help(update_or_query, context, edit=False):
    advanced_text = \"\"\"🏗 **UNIFIED SYSTEM CORE v2.5**
━━━━━━━━━━━━━━━━━━━━
👋 Рад видеть вас в системе управления. Вот список доступных команд:

🧠 **УПРАВЛЕНИЕ И ПАМЯТЬ**
• /start - Запуск и обновление профиля
• /help - Это меню
• /settings - Настройка AI модели и провайдера
• /memory - Ваши долгосрочные факты
• /clear - Очистить контекст текущего диалога

📽 **CONTENT FACTORY & VIDEO**
• /factory - Статус и запуск контент-фабрики
• /videostatus - Контроль генерации видео
• /generate_video <prompt> - Создать AI видео

📅 **ПЛАНИРОВАНИЕ И МОНИТОРИНГ**
• /calendar - Подключить Google Календарь
• /brief - Сводка дел на сегодня
• /mail - Почтовый клиент AgentMail
• /status - Статус всех узлов системы
• /infra - Подробная инфа об инфраструктуре

⚙️ **ИНСТРУМЕНТЫ**
• /search <query> - Поиск в интернете (AI)
• /imagine <prompt> - Сгенерировать изображение
• /beads - Управление тасками (Git-native)
• /todo - Список дел

**БЫСТРЫЙ ДОСТУП:**\"\"\"
    keyboard = [
        [InlineKeyboardButton("📅 Сводка дня", callback_data="daily_brief_cb")],
        [InlineKeyboardButton("🧠 Мои воспоминания", callback_data="show_memories_cb")],
        [InlineKeyboardButton("⚙️ Настройки AI", callback_data="settings_cb")],
        [InlineKeyboardButton("🏭 Контент-Фабрика", callback_data="factory_status")],
        [InlineKeyboardButton("📧 Почта (AgentMail)", callback_data="mail_list")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if edit:
        await update_or_query.edit_message_text(advanced_text, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update_or_query.message.reply_text(advanced_text, parse_mode='Markdown', reply_markup=reply_markup)"""
    
    # Use re.escape is too complex here, let's just find the broken function
    # The broken function starts with async def show_advanced_help
    content = re.sub(r'async def show_advanced_help.*?reply_markup=reply_markup\s+\)', new_help_func, content, flags=re.DOTALL)

    # Also fix the factory_command if it got messed up (it probably did)
    new_factory_func = """async def factory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_approved(user_id): return
    if not context.args:
        try:
            ps_proc = await asyncio.create_subprocess_exec('ps', 'aux', stdout=asyncio.subprocess.PIPE)
            stdout, _ = await ps_proc.communicate()
            is_running = 'factory_scheduler.py' in stdout.decode()
            out_dir = '/home/gonya/Unified_System_Core/outputs'
            last_videos = []
            from pathlib import Path
            if os.path.exists(out_dir):
                files = sorted(Path(out_dir).glob('*.mp4'), key=os.path.getmtime, reverse=True)
                for f in files[:3]:
                    mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime('%d.%m %H:%M')
                    last_videos.append(f'• {f.name} ({mtime})')
            status_color = '🟢 RUNNING' if is_running else '🔴 STOPPED'
            msg = f\"\"\"🏭 **Content Factory 2.0 STATUS**
━━━━━━━━━━━━━━━━━━━━
Статус: {status_color}

Последние видео:
\"\"\" + ('\\n'.join(last_videos) if last_videos else '• _Нет данных_') + \"\"\"

**Команды:**
`/factory run` - Запуск
`/factory longform` - 15-мин видео
`/factory restart` - Перезапуск\"\"\"
            await update.message.reply_text(msg, parse_mode='Markdown')
            return
        except Exception as e:
            await update.message.reply_text(f'❌ Error: {e}')
            return
    subcmd = context.args[0].lower()
    script_path = '/home/gonya/Unified_System_Core/Projects/Content_Factory/src/pipeline/factory_scheduler.py'
    if subcmd == 'run': cmd = ['python3', script_path]
    elif subcmd == 'longform': cmd = ['python3', script_path, '--longform']
    elif subcmd == 'restart':
        await asyncio.create_subprocess_exec('pm2', 'delete', 'factory', stderr=asyncio.subprocess.DEVNULL)
        await asyncio.create_subprocess_exec('pm2', 'start', script_path, '--name', 'factory', '--', '--scheduler')
        await update.message.reply_text('✅ Factory Started in PM2.')
        return
    else: return
    try:
        p = await asyncio.create_subprocess_exec(*cmd, cwd=os.path.dirname(script_path))
        await update.message.reply_text(f'🚀 Started! PID: `{p.pid}`')
    except Exception as e: await update.message.reply_text(f'❌ Failed: {e}')"""

    content = re.sub(r'async def factory_command.*?await update\.message\.reply_text\(f\'❌ Failed: \{e\}\'\)', new_factory_func, content, flags=re.DOTALL)

    with open(file_path, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    patch_file(sys.argv[1])
