"""
AI Telegram Bot - Main Entry Point.
Handles Telegram commands and message routing.
"""
import asyncio
import logging
import signal
import sys

from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from .config_manager import ConfigManager
from .inference_client import InferenceClient
from .conversation_manager import ConversationManager
from .health import start_health_server
from .logging_config import setup_logging
from .image_generator import ImageGenerator
from .ha_controller import HAController
from .usage_tracker import UsageTracker
from .web_search import WebSearch
from .task_manager import TaskManager
from .alice_skill import AliceSkill
from .scheduler_service import SchedulerService
from .infrastructure import InfrastructureManager
from .dashboard import DashboardService
from .notification_manager import NotificationManager
from .linear_client import LinearClient
from .digest_service import DigestService
from .calendar_client import CalendarClient

# Initialize logging first
setup_logging()
logger = logging.getLogger(__name__)

# Global instances
config = ConfigManager()
inference = InferenceClient(config)
conv_manager = ConversationManager(storage_path="conversations")
image_gen = ImageGenerator(config)
ha_controller = HAController()
usage_tracker = UsageTracker(db_path=config.get("USAGE_DB_PATH", "usage.db"))
web_search = WebSearch()
task_manager = TaskManager(db_path=config.get("TASKS_DB_PATH", "tasks.db"))
alice_skill = AliceSkill(port=config.get("ALICE_PORT", 8090))
scheduler = SchedulerService(db_path=f"sqlite:///{config.get('JOBS_DB_PATH', 'jobs.db')}")
infra_manager = InfrastructureManager()
notify_manager = NotificationManager()  # Quiet hours: 23:00-08:00 by default
linear_client = LinearClient()
digest_service = None  # Will be initialized after other services
calendar_client = CalendarClient()

# Admin ID for sensitive commands (update)
ADMIN_ID = int(config.get("ALLOWED_USERS", "").split(",")[0] or 0)

# System prompt for AI responses
SYSTEM_PROMPT = f"""Ты - Гоня (Gonya), умный AI ассистент в системе 'Unified System'.
Ты управляешь сервером igor-gaming-1 и умным домом Home Assistant.
Твоя инфраструктура:
{infra_manager.get_summary()}

Твоя главная цель - быть полезным и исполнительным.

У тебя есть доступ к следующим ИНСТРУМЕНТАМ (Tools):
1. ПРОВЕРКА ВАКАНСИЙ: "проверить почту", "найти работу", "просканировать вакансии" → [[RUN:SCAN]]
2. СТАТУС СИСТЕМЫ: "как дела", "статус", "мониторинг", "здоровье сервера" → [[RUN:STATUS]]
3. КОМАНДЫ СЕРВЕРА: "выполни команду", "запусти на сервере", "проверь процессы" → [[RUN:CMD:<команда>]]
4. СВЯЗЬ С ANTIGRAVITY: "спроси у Antigravity", "передай Antigravity", "нужна помощь агента" → [[ASK:ANTIGRAVITY:<вопрос>]]
5. ПОИСК В ИНТЕРНЕТЕ: "погугли", "найди инфу", "кто такой...", "погода в..." → [[RUN:SEARCH:<запрос>]]

ПРИМЕРЫ:
User: "Найди мне работу"
AI: "Хорошо, запускаю анализ свежих вакансий. [[RUN:SCAN]]"

User: "Проверь, сколько памяти использует сервер"
AI: "Проверяю использование памяти... [[RUN:CMD:free -h]]"

User: "Спроси у Antigravity, как настроить автозапуск"
AI: "Передаю вопрос главному агенту... [[ASK:ANTIGRAVITY:Как настроить автозапуск службы?]]"

User: "Погугли новости AI"
AI: "Ищу новости... [[RUN:SEARCH:AI news]]"

ВАЖНО: Ты можешь выполнять ТОЛЬКО безопасные команды (чтение, статус). Никогда не удаляй файлы и не останавливай критические службы без подтверждения пользователя."""

# Authorized users (Telegram User IDs)
ALLOWED_USERS = [
    708531393,    # Igor (Admin)
    5569219290,   # Oksana
]

ADMIN_ID = 708531393  # Igor's ID for approval notifications

def require_auth(func):
    """Decorator to check if user is authorized."""
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id not in ALLOWED_USERS:
            user_name = update.effective_user.first_name or "Unknown"
            username = update.effective_user.username or "no_username"
            
            logger.warning(f"Unauthorized access attempt from user {user_id} (@{username})")
            
            # Send approval request to admin
            from telegram import InlineKeyboardButton, InlineKeyboardMarkup
            keyboard = [
                [
                    InlineKeyboardButton("✅ Одобрить", callback_data=f"approve_{user_id}"),
                    InlineKeyboardButton("❌ Отклонить", callback_data=f"deny_{user_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"🔔 **Запрос на доступ**\n\n"
                         f"👤 Имя: {user_name}\n"
                         f"🆔 User ID: `{user_id}`\n"
                         f"📱 Username: @{username}\n\n"
                         f"Одобрить доступ?",
                    parse_mode="Markdown",
                    reply_markup=reply_markup
                )
            except Exception as e:
                logger.error(f"Failed to send approval request: {e}")
            
            await update.message.reply_text(
                "⏳ Запрос на доступ отправлен администратору.\n\n"
                "Пожалуйста, ожидайте одобрения."
            )
            return
        return await func(update, context)
    return wrapper


@require_auth
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "👋 Привет! Я твой AI ассистент Unified System.\n\n"
        "Команды:\n"
        "/scan - 🕵️‍♂️ Запустить поиск вакансий (Job Hunter)\n"
        "/status - 📊 Статус системы\n"
        "/models - 📋 Список моделей (с быстрым переключением)\n"
        "/clear - 🧹 Очистить историю диалога\n"
        "/setprovider <name> - ⚙️ Выбрать AI (ollama/openai/gemini)\n"
        "/setendpoint <url> - 🔗 Адрес API\n"
        "/setapikey <key> - 🔑 Установить ключ\n"
        "/setmodel <name> - 🧠 Выбрать модель\n"
        "/setapikey <key> - 🔑 Установить ключ\n"
        "/setmodel <name> - 🧠 Выбрать модель\n"
        "/imagine <prompt> - 🎨 Создать изображение\n"
        "/usage - 📈 Статистика токенов\n"
        "/search <query> - 🌐 Поиск в интернете\n"
        "/todo <cmd> - 📝 Задачи (add/list/done)\n"
        "/remind <time> <text> - ⏰ Напоминание (10m, 1h)\n"
        "/infra - 🏗 Инфраструктура\n"
        "/update - 🔄 Обновить бота\n"
        "/ha <cmd> - 🏠 Управление умным домом\n"
         
         
        "/help - ❓ Помощь"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await cmd_start(update, context)


@require_auth
async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command - show full system dashboard."""
    user_id = update.effective_user.id
    
    # Send "typing"
    await update.message.chat.send_action("typing")
    msg = await update.message.reply_text("🔍 Проверяю системы...")
    
    # 1. System Metrics
    import psutil
    import time
    from datetime import datetime, timedelta
    
    cpu_usage = psutil.cpu_percent()
    mem = psutil.virtual_memory()
    uptime = time.time() - psutil.boot_time()
    
    def format_uptime(seconds):
        days, remainder = divmod(seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(days)}d {int(hours)}h {int(minutes)}m"
    
    uptime_str = format_uptime(uptime)
    
    # 2. Inference Health
    inf_status = "✅ OK" if await inference.health_check() else "❌ Error"
    
    # 3. HA Health
    ha_status = "❓ Unknown"
    try:
        ha_res = await ha_controller.get_status()
        if ha_res and ha_res.get("status") == "ok":
            ha_status = f"✅ Online ({ha_res.get('version', 'unknown')})"
        else:
            ha_status = f"❌ Error: {ha_res.get('message', 'unknown')}"
    except:
        ha_status = "❌ Unreachable"

    # 4. DB Stats
    try:
        # Check if DB files exist
        import os
        usage_db = config.get('USAGE_DB_PATH', 'usage.db')
        tasks_db = config.get('TASKS_DB_PATH', 'tasks.db')
        
        usage_size = os.path.getsize(usage_db) / 1024 if os.path.exists(usage_db) else 0
        tasks_size = os.path.getsize(tasks_db) / 1024 if os.path.exists(tasks_db) else 0
        
        db_status = f"✅ usage.db ({usage_size:.1f}KB), tasks.db ({tasks_size:.1f}KB)"
    except Exception as e:
        db_status = f"⚠️ Warning: {e}"

    # 5. Build Message
    dashboard = (
        f"📊 **System Status**\n\n"
        f"🖥 **Server**\n"
        f"• CPU: `{cpu_usage}%`\n"
        f"• RAM: `{mem.percent}%` ({mem.used // 1024 // 1024}MB / {mem.total // 1024 // 1024}MB)\n"
        f"• Uptime: `{uptime_str}`\n\n"
        
        f"🧠 **AI Core**\n"
        f"• Provider: `{inference.provider}`\n"
        f"• Model: `{inference.model}`\n"
        f"• Status: {inf_status}\n\n"
        
        f"🏠 **Home Assistant**\n"
        f"• Status: {ha_status}\n\n"
        
        f"🗄 **Databases**\n"
        f"• {db_status}\n\n"
        
        f"🕒 Time: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
    )
    
    await msg.edit_text(dashboard, parse_mode="Markdown")


async def cmd_setendpoint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setendpoint command - set inference base URL."""
    if not context.args:
        await update.message.reply_text(
            "Usage: /setendpoint <url>\n"
            "Example: /setendpoint http://100.127.194.111:11434"
        )
        return
    
    url = context.args[0]
    config.set("INFERENCE_BASE_URL", url)
    logger.info(f"Inference URL updated to: {url}", extra={"user_id": update.effective_user.id})
    
    await update.message.reply_text(f"✅ Inference URL set to: `{url}`", parse_mode="Markdown")


async def cmd_setapikey(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setapikey command - set API key."""
    if not context.args:
        await update.message.reply_text(
            "Usage: /setapikey <key>\n"
            "⚠️ Delete this message after setting the key!"
        )
        return
    
    api_key = context.args[0]
    provider = config.get("INFERENCE_PROVIDER", "ollama").lower()
    
    # Set both provider-specific and generic key for compatibility
    if provider == "gemini":
        config.set("GEMINI_API_KEY", api_key)
    elif provider == "openai":
        config.set("OPENAI_API_KEY", api_key)
    config.set("INFERENCE_API_KEY", api_key)
    
    logger.info(f"API key updated for provider: {provider}", extra={"user_id": update.effective_user.id})
    
    # Try to delete the message containing the API key
    try:
        await update.message.delete()
    except Exception:
        pass
    
    await update.message.reply_text(f"✅ API key has been set for {provider.upper()} and encrypted.")


async def cmd_setmodel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setmodel command - set model name."""
    if not context.args:
        await update.message.reply_text(
            "Usage: /setmodel <name>\n"
            "Example: /setmodel llama3.2"
        )
        return
    
    model = context.args[0]
    config.set("MODEL_NAME", model)
    logger.info(f"Model updated to: {model}", extra={"user_id": update.effective_user.id})
    
    await update.message.reply_text(f"✅ Model set to: `{model}`", parse_mode="Markdown")

    await update.message.reply_text(f"✅ Model set to: `{model}`", parse_mode="Markdown")


@require_auth
async def cmd_usage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /usage command - show token stats."""
    user_id = update.effective_user.id
    stats = usage_tracker.get_user_stats(user_id)
    
    if not stats:
        await update.message.reply_text("📊 Статистики пока нет.")
        return
    
    msg = (
        f"📊 **Статистика за 30 дней**\n\n"
        f"Всего запросов: `{stats['requests']}`\n"
        f"Токенов всего: `{stats['total_tokens']}`\n"
        f"Input: `{stats['prompt_tokens']}`\n"
        f"Output: `{stats['completion_tokens']}`\n\n"
        f"**По моделям:**\n"
    )
    
    for model, tokens in stats["by_model"].items():
        msg += f"- `{model}`: {tokens}\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")
@require_auth
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming photos."""
    user_id = update.effective_user.id
    
    # Get the largest photo
    photo = update.message.photo[-1]
    
    # Get caption or default prompt
    prompt = update.message.caption or "Что изображено на этой картинке? Опиши подробно."
    
    await update.message.chat.send_action("typing")
    await update.message.reply_text("👀 Смотрю на фото...")
    
    try:
        import os
        import tempfile
        
        # Download photo
        file = await photo.get_file()
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            temp_path = f.name
            
        await file.download_to_drive(temp_path)
        
        # Analyze
        response = await inference.analyze_image(temp_path, prompt)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        await update.message.reply_text(response, parse_mode="Markdown")
        
    except Exception as e:
        logger.error(f"Photo handling failed: {e}")
        await update.message.reply_text(f"❌ Ошибка анализа фото: {e}")


@require_auth
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming voice messages."""
    user_id = update.effective_user.id
    
    # Send typing action
    await update.message.chat.send_action("typing")
    await update.message.reply_text("🎤 Слушаю...")
    
    try:
        # Get voice file
        voice_file = await update.message.voice.get_file()
        
        # Download to temp file
        import os
        import tempfile
        
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
            temp_path = f.name
        
        await voice_file.download_to_drive(temp_path)
        
        # Transcribe
        transcript = await inference.transcribe_audio(temp_path)
        
        # Cleanup
        os.remove(temp_path)
        
        if not transcript or "[Error" in transcript:
            await update.message.reply_text(f"❌ Не удалось распознать речь: {transcript}")
            return
            
        await update.message.reply_text(f"🗣 Распознано: \"_{transcript}_\"", parse_mode="Markdown")
        
        # Process as text command
        response = await process_text_request(transcript, user_id)
        
        # Split and send response
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i:i+4000])
        else:
            await update.message.reply_text(response)
            
    except Exception as e:
        logger.error(f"Voice handling failed: {e}")
        await update.message.reply_text("❌ Ошибка обработки голосового сообщения.")


@require_auth
async def cmd_scan(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /scan command - trigger Job Hunter."""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} requested Job Scan", extra={"user_id": user_id})
    await update.message.reply_text("🕵️‍♂️ Запускаю поиск вакансий (Job Hunter/Analyzer)... ожидай отчета.")
    
    # Path to job_hunter.py on the server
    # We assume standard deployment path
    script_path = "/home/gonya/Documents/Unified_System/Scripts/automation/job_hunter.py"
    venv_python = "/home/gonya/Documents/Unified_System/venv/bin/python"
    
    import subprocess
    try:
        # Run asynchronously in background so we don't block the bot
        # But for simplicity here using subprocess.Popen or asyncio.create_subprocess_exec
        process = await asyncio.create_subprocess_exec(
            venv_python, script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # We don't wait for full completion here as it communicates via Telegram itself
        # But we could wait a bit to check for immediate startup errors
        # await process.communicate()
        
    except Exception as e:
        logger.error(f"Failed to start Job Hunter: {e}")
        await update.message.reply_text(f"❌ Ошибка запуска: {e}")



@require_auth
async def cmd_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /imagine command - generate image."""
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("Usage: /imagine <description>\nExample: /imagine futuristic cyberpunk city")
        return
    
    prompt = " ".join(context.args)
    await update.message.reply_text(f"🎨 Generating image for: \"{prompt[:50]}...\"\n⏳ Please wait...")
    
    try:
        image_path = await image_gen.generate(prompt, user_id)
        if image_path:
            await update.message.reply_photo(photo=open(image_path, 'rb'))
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        await update.message.reply_text(f"❌ Image generation failed: {e}")


async def post_init(application: Application) -> None:
    """Post-initialization hook."""
    # Set commands
    commands = [
        BotCommand("start", "🚀 Запустить бота"),
        BotCommand("help", "❓ Помощь"),
        BotCommand("status", "📊 Статус системы"),
        BotCommand("models", "🧠 Выбор модели"),
        BotCommand("scan", "🕵️‍♂️ Поиск вакансий"),
        BotCommand("imagine", "🎨 Генерация картинок"),
        BotCommand("search", "🌐 Поиск"),
        BotCommand("todo", "📝 Задачи"),
        BotCommand("ha", "🏠 Умный дом"),
        BotCommand("clear", "🧹 Очистить контекст"),
    ]
    await application.bot.set_my_commands(commands)
    
    # Start Alice Skill
    alice_skill.set_handler(process_text_request)
    await alice_skill.start()
    
    # Start Scheduler
    scheduler.set_application(application)
    scheduler.start()

    # Determine public URL (mock or real)
    logger.info("Alice Skill running on port 8090. Needs tunnel for public access.")

@require_auth
async def cmd_ha(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /ha subcommands."""
    if not ha_controller.HA_AVAILABLE:
         await update.message.reply_text("❌ Home Assistant Integration not available.")
         return

    if not context.args:
        await update.message.reply_text("Usage:\n/ha status\n/ha lights on/off\n/ha sensors\n/ha script <name>\n/ha scene <name>")
        return
        
    cmd = context.args[0].lower()
    
    if cmd == "status":
        status = await ha_controller.get_status()
        await update.message.reply_text(f"🏠 HA Status:\n{status}")
        
    elif cmd == "sensors":
        report = await ha_controller.get_sensors_report()
        await update.message.reply_text(report, parse_mode="Markdown")
        
    elif cmd == "lights":
        if len(context.args) < 2:
             await update.message.reply_text("Usage: /ha lights on OR /ha lights off")
             return
        action = context.args[1].lower()
        if action == "on":
             # This is dangerous (turns on ALL lights), maybe specific entity?
             # For safety let's ask for entity or just demo
             await ha_controller.turn_on_light("all") 
             await update.message.reply_text("💡 Turning ON lights (mock/all)")
        elif action == "off":
             await ha_controller.turn_off_light("all")
             await update.message.reply_text("🌑 Turning OFF lights")
             
    elif cmd == "script":
        if len(context.args) < 2:
             await update.message.reply_text("Usage: /ha script <script_name>")
             return
        script_name = context.args[1]
        if not script_name.startswith("script."):
            script_name = f"script.{script_name}"
        await ha_controller.run_script(script_name)
        await update.message.reply_text(f"▶️ Executing script: {script_name}")
        
    elif cmd == "scene":
        if len(context.args) < 2:
             await update.message.reply_text("Usage: /ha scene <scene_name>")
             return
        scene_name = context.args[1]
        if not scene_name.startswith("scene."):
            scene_name = f"scene.{scene_name}"
        await ha_controller.activate_scene(scene_name)
        await update.message.reply_text(f"🎬 Activating scene: {scene_name}")

    else:
        await update.message.reply_text(f"Unknown HA command: {cmd}")


@require_auth
async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /clear command - clear conversation history."""
    user_id = update.effective_user.id
    
    if conv_manager.clear_history(user_id):
        await update.message.reply_text(
            "🧹 История диалогов очищена!\n\n"
            "Следующее сообщение начнёт новый контекст."
        )
        logger.info(f"Cleared conversation history for user {user_id}")
    else:
        await update.message.reply_text(
            "ℹ️ История диалогов уже пуста."
        )


async def cmd_setprovider(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setprovider command - set inference provider."""
    providers = ["ollama", "openai", "gemini"]
    
    if not context.args:
        current = config.get("INFERENCE_PROVIDER", "ollama")
        await update.message.reply_text(
            f"Current provider: `{current}`\n\n"
            f"Usage: /setprovider <provider>\n"
            f"Available: {', '.join(providers)}\n\n"
            f"Examples:\n"
            f"`/setprovider ollama`\n"
            f"`/setprovider openai`\n"
            f"`/setprovider gemini`",
            parse_mode="Markdown"
        )
        return
    
    provider = context.args[0].lower()
    if provider not in providers:
        await update.message.reply_text(
            f"❌ Unknown provider: `{provider}`\n"
            f"Available: {', '.join(providers)}",
            parse_mode="Markdown"
        )
        return
    
    config.set("INFERENCE_PROVIDER", provider)
    logger.info(f"Provider updated to: {provider}", extra={"user_id": update.effective_user.id})
    
    # Show help for setting up the provider
    if provider == "openai":
        hint = "Set your API key with /setapikey"
    elif provider == "gemini":
        hint = "Set your Gemini API key with /setapikey"
    else:
        hint = "Make sure Ollama is running"
    
    await update.message.reply_text(
        f"✅ Provider set to: `{provider}`\n\n💡 {hint}",
        parse_mode="Markdown"
    )


async def cmd_models(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /models command - list available models with quick-switch buttons."""
    await update.message.reply_text("🔍 Fetching available models...")
    
    models = await inference.list_models()
    
    if not models:
        base_url = config.get("INFERENCE_BASE_URL")
        await update.message.reply_text(
            f"❌ Could not fetch models from `{base_url}`\n\n"
            "Make sure the endpoint is accessible.",
            parse_mode="Markdown"
        )
        return
    
    # Get current model
    current_model = inference.model
    
    # Create inline keyboard buttons for quick switching
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
    buttons = []
    for model in models[:20]:  # Limit to 20 to avoid keyboard overflow
        indicator = "✅" if model == current_model else "🔄"
        button_text = f"{indicator} {model}"
        buttons.append([InlineKeyboardButton(button_text, callback_data=f"model:{model}")])
    
    keyboard = InlineKeyboardMarkup(buttons)
    
    await update.message.reply_text(
        f"📋 **Available Models** ({len(models)})\n\n"
        f"Current: `{current_model}`\n\n"
        f"Click to switch:",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


@require_auth
async def cmd_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /search command - perform a web search."""
    if not context.args:
        await update.message.reply_text("Usage: /search <query>\nExample: /search latest AI news")
        return
    
    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Ищу: \"{query[:50]}...\"\n⏳ Пожалуйста, подождите...")
    
    try:
        search_result = await web_search.search(query)
        if search_result:
            await update.message.reply_text(search_result, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Не удалось найти результаты для вашего запроса.")
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        await update.message.reply_text(f"❌ Ошибка при выполнении поиска: {e}")


@require_auth
async def cmd_remind(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /remind command."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /remind <time> <text>\nExample: /remind 10m Выключи духовку\nTime units: s, m, h, d")
        return
        
    time_str = context.args[0].lower()
    text = " ".join(context.args[1:])
    user_id = update.effective_user.id
    
    # Parse time
    import re
    from datetime import datetime, timedelta
    
    match = re.match(r"^(\d+)([smhd])$", time_str)
    if not match:
        await update.message.reply_text("❌ Invalid time format. Use 10s, 5m, 1h, 2d")
        return
        
    amount = int(match.group(1))
    unit = match.group(2)
    
    delta = timedelta()
    if unit == 's': delta = timedelta(seconds=amount)
    elif unit == 'm': delta = timedelta(minutes=amount)
    elif unit == 'h': delta = timedelta(hours=amount)
    elif unit == 'd': delta = timedelta(days=amount)
    
    run_date = datetime.now() + delta
    
    if scheduler.add_reminder(user_id, text, run_date):
        await update.message.reply_text(f"✅ Напоминание установлено на {run_date.strftime('%H:%M:%S')}")
    else:
        await update.message.reply_text("❌ Ошибка планировщика. Проверьте логи.")


@require_auth
async def cmd_infra(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /infra command."""
    await update.message.chat.send_action("typing")
    report = await infra_manager.check_nodes()
    await update.message.reply_text(report, parse_mode="Markdown")


@require_auth
async def cmd_backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Create and send database backup."""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    await update.message.chat.send_action("upload_document")
    
    import zipfile
    import os
    from datetime import datetime
    
    # Files to backup
    files = ["tasks.db", "usage.db", "jobs.db", "windows_ai_core.json"]
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    # Resolve paths (assume current working dir is project root or src parent)
    # We will search in current dir and known subdirs
    
    try:
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            found = False
            for file in files:
                # Try relative path
                if os.path.exists(file):
                    zipf.write(file)
                    found = True
                # Try config/ or root/
                elif os.path.exists(f"Windows_AI_Core/{file}"):
                    zipf.write(f"Windows_AI_Core/{file}", arcname=file)
                    found = True
                elif os.path.exists(f"config/{file}"):
                     zipf.write(f"config/{file}", arcname=file)
                     found = True
            
            if not found:
                await update.message.reply_text("⚠️ Не найдено файлов баз данных для бэкапа.")
                os.remove(backup_name)
                return

        # Send file
        await update.message.reply_document(
            document=open(backup_name, "rb"),
            caption=f"📦 Database Backup ({datetime.now().strftime('%Y-%m-%d')})"
        )
        
        # Cleanup
        os.remove(backup_name)
        
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        await update.message.reply_text(f"❌ Backup error: {e}")

@require_auth
async def cmd_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /update command - self-update via git and restart."""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ Только главный администратор может обновлять бота.")
        return
        
    await update.message.reply_text("🔄 Начинаю обновление...\n1. Git Pull...")
    
    import subprocess
    try:
        # 1. Git Pull
        # Assume running in project root or src parent
        project_dir = "/home/gonya/Documents/Unified_System"
        
        proc = await asyncio.create_subprocess_shell(
            f"cd {project_dir} && git pull",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            await update.message.reply_text(f"❌ Git Pull Failed:\n{stderr.decode()}")
            return
            
        await update.message.reply_text(f"✅ Code updated.\nOutput: {stdout.decode()[:200]}...\n\n2. Updating Dependencies...")
        
        # 2. Pip Install
        venv_pip = f"{project_dir}/venv/bin/pip"
        proc = await asyncio.create_subprocess_shell(
            f"{venv_pip} install -r {project_dir}/Windows_AI_Core/requirements.txt",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        if proc.returncode != 0:
            await update.message.reply_text(f"⚠️ Pip Install Warning (continuing):\n{stderr.decode()[:300]}")
        else:
            await update.message.reply_text("✅ Dependencies updated.")
            
        # 3. Restart
        await update.message.reply_text("♻️ Перезапускаю сервис (systemd)... Я вернусь через 5-10 секунд.")
        
        # We use the NOPASSWD sudo rule we configured earlier
        subprocess.Popen(["sudo", "systemctl", "restart", "ai-bot"])
        
    except Exception as e:
        logger.error(f"Update failed: {e}")
        await update.message.reply_text(f"❌ Critical Update Error: {e}")


@require_auth
async def cmd_costs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show detailed cost breakdown."""
    user_id = update.effective_user.id
    
    # User's personal stats
    user_stats = usage_tracker.get_user_stats(user_id, days=30)
    
    if not user_stats:
        await update.message.reply_text("📊 Нет данных об использовании за последние 30 дней.")
        return
    
    msg = "💰 **Детальная статистика (30 дней)**\n\n"
    msg += f"📈 **Всего токенов**: {user_stats['total_tokens']:,}\n"
    msg += f"📝 **Запросов**: {user_stats['requests']}\n\n"
    
    msg += "**По моделям:**\n"
    for model, tokens in user_stats['by_model'].items():
        msg += f"  • {model}: {tokens:,} токенов\n"
    
    # Provider breakdown (all users, admin only)
    if user_id == ADMIN_ID:
        msg += "\n🌐 **По провайдерам (все пользователи):**\n"
        providers = usage_tracker.get_provider_breakdown(days=30)
        for provider, data in providers.items():
            msg += f"  • {provider}: {data['tokens']:,} токенов ({data['requests']} запросов)\n"
        
        # All users stats
        all_users = usage_tracker.get_all_users_stats(days=30)
        if all_users['users']:
            msg += "\n👥 **По пользователям:**\n"
            for u in all_users['users'][:5]:  # Top 5
                msg += f"  • {u['username']}: {u['total_tokens']:,} токенов\n"
    
    await update.message.reply_text(msg, parse_mode="Markdown")


@require_auth
async def cmd_notify(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manage notification settings."""
    if not context.args:
        quiet = notify_manager.is_quiet_hours()
        status = "🌙 Тихий режим" if quiet else "🔔 Активный режим"
        await update.message.reply_text(
            f"{status}\n\n"
            f"Тихие часы: {notify_manager.quiet_start.strftime('%H:%M')} - {notify_manager.quiet_end.strftime('%H:%M')}\n\n"
            "Команды:\n"
            "/notify status - текущий статус\n"
            "/notify quiet HH:MM HH:MM - установить тихие часы"
        )
        return
    
    cmd = context.args[0].lower()
    
    if cmd == "status":
        quiet = notify_manager.is_quiet_hours()
        await update.message.reply_text("🌙 Сейчас тихие часы" if quiet else "🔔 Сейчас активный режим")
    
    elif cmd == "quiet":
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /notify quiet 23:00 08:00")
            return
        
        try:
            from datetime import datetime
            start_str = context.args[1]
            end_str = context.args[2]
            
            start = datetime.strptime(start_str, "%H:%M").time()
            end = datetime.strptime(end_str, "%H:%M").time()
            
            notify_manager.quiet_start = start
            notify_manager.quiet_end = end
            
            await update.message.reply_text(f"✅ Тихие часы установлены: {start_str} - {end_str}")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка формата времени: {e}")


@require_auth
async def cmd_digest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Generate and send daily digest."""
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "User"
    
    if not digest_service:
        await update.message.reply_text("❌ Digest service not initialized.")
        return
    
    await update.message.chat.send_action("typing")
    
    try:
        digest = await digest_service.generate_digest(user_id, username)
        await update.message.reply_text(digest, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Digest generation failed: {e}")
        await update.message.reply_text(f"❌ Не удалось создать дайджест: {e}")


@require_auth
async def cmd_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Calendar management."""
    if not calendar_client.service:
        await update.message.reply_text("❌ Google Calendar not configured.\n\nSet GOOGLE_CALENDAR_API_KEY in .env")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📅 **Calendar Commands:**\n\n"
            "/calendar today - события сегодня\n"
            "/calendar week - на неделю",
            parse_mode="Markdown"
        )
        return
    
    cmd = context.args[0].lower()
    
    if cmd == "today":
        events = calendar_client.get_today_events()
        if not events:
            await update.message.reply_text("📅 Сегодня нет событий.")
            return
        
        msg = f"📅 **События сегодня ({len(events)}):**\n\n"
        for event in events:
            formatted = calendar_client.format_event(event)
            msg += f"• {formatted}\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    
    elif cmd == "week":
        events = calendar_client.get_upcoming_events(days=7)
        if not events:
            await update.message.reply_text("📅 На этой неделе нет событий.")
            return
        
        msg = f"📅 **События на неделю ({len(events)}):**\n\n"
        for event in events:
            formatted = calendar_client.format_event(event)
            msg += f"• {formatted}\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    
    else:
        await update.message.reply_text(f"Unknown command: {cmd}")


@require_auth
async def cmd_linear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Linear task management."""
    if not linear_client.api_key:
        await update.message.reply_text("❌ Linear API key not configured.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "📋 **Linear Commands:**\n\n"
            "/linear me - мои задачи\n"
            "/linear create <title> - создать задачу\n"
            "/linear teams - список команд",
            parse_mode="Markdown"
        )
        return
    
    cmd = context.args[0].lower()
    
    if cmd == "me":
        issues = linear_client.get_my_issues(limit=10)
        if not issues:
            await update.message.reply_text("📭 У вас нет активных задач в Linear.")
            return
        
        msg = "📋 **Ваши задачи в Linear:**\n\n"
        for issue in issues:
            priority_emoji = {0: "⚪", 1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢"}
            emoji = priority_emoji.get(issue.get("priority", 0), "⚪")
            msg += f"{emoji} [{issue['identifier']}]({issue['url']}) {issue['title']}\n"
            msg += f"   └ {issue['state']['name']}\n\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown", disable_web_page_preview=True)
    
    elif cmd == "create":
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /linear create <title>")
            return
        
        title = " ".join(context.args[1:])
        issue = linear_client.create_issue(title, priority=3)  # Normal priority
        
        if issue:
            await update.message.reply_text(
                f"✅ Задача создана: [{issue['identifier']}]({issue['url']})\n{issue['title']}",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text("❌ Не удалось создать задачу.")
    
    elif cmd == "teams":
        teams = linear_client.get_teams()
        if not teams:
            await update.message.reply_text("❌ Не удалось получить список команд.")
            return
        
        msg = "👥 **Ваши команды в Linear:**\n\n"
        for team in teams:
            msg += f"• {team['name']} (`{team['key']}`)\n"
        
        await update.message.reply_text(msg, parse_mode="Markdown")
    
    else:
        await update.message.reply_text(f"Unknown command: {cmd}")


@require_auth
async def cmd_todo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /todo command - manage tasks."""
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "📝 **Task Manager**\n\n"
            "Usage:\n"
            "`/todo add <text>` - Add task\n"
            "`/todo list` - List pending tasks\n"
            "`/todo done <id>` - Complete task",
            parse_mode="Markdown"
        )
        return

    subcmd = context.args[0].lower()
    
    if subcmd == "add":
        text = " ".join(context.args[1:])
        if not text:
            await update.message.reply_text("Usage: /todo add <text>")
            return
        
        task_id = task_manager.add_task(user_id, text)
        await update.message.reply_text(f"✅ Задача добавлена! ID: `{task_id}`", parse_mode="Markdown")
        
    elif subcmd == "list":
        tasks = task_manager.list_tasks(user_id)
        if not tasks:
            await update.message.reply_text("📝 Задач нет. Отдыхай!")
            return
            
        msg = "📋 **Твои задачи:**\n\n"
        for t in tasks:
            msg += f"• `#{t['id']}` {t['text']}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")
        
    elif subcmd == "done":
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /todo done <id>")
            return
        try:
            task_id = int(context.args[1])
            if task_manager.complete_task(user_id, task_id):
                await update.message.reply_text(f"✅ Задача `#{task_id}` выполнена!", parse_mode="Markdown")
            else:
                await update.message.reply_text(f"❌ Не удалось найти или обновить задачу `#{task_id}`.")
        except ValueError:
            await update.message.reply_text("❌ ID должен быть числом.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming text messages."""
    user_id = update.effective_user.id
    
    # Authorization check
    if user_id not in ALLOWED_USERS:
        logger.warning(f"Unauthorized access attempt from user {user_id}")
        await update.message.reply_text(
            "⛔ Доступ запрещён.\n\n"
            "Этот бот доступен только авторизованным пользователям.\n"
            "Если вы считаете, что это ошибка, свяжитесь с администратором."
        )
        return
    
    message_text = update.message.text
    user_name = update.effective_user.first_name or "User"
    
    logger.info(f"Message from {user_name}: {message_text[:50]}...", extra={"user_id": user_id})
    
    # Send typing indicator
    await update.message.chat.send_action("typing")
    
    # Get conversation history for context
    history = conv_manager.get_context_messages(user_id, limit=5)
    
    # Add current message
    current_message = {"role": "user", "content": message_text}
    messages = history + [current_message]
    
    # Save user message to history
    conv_manager.add_message(user_id, "user", message_text)
    
    # Get AI response with conversation context
    response, usage = await inference.chat(messages, system_prompt=SYSTEM_PROMPT)
    
    # Save assistant response to history
    conv_manager.add_message(user_id, "assistant", response)
    
    # Log usage stats
    if usage and usage.get("total_tokens", 0) > 0:
        logger.info(f"Token Usage: {usage}", extra={"user_id": user_id})
        # Persist usage
        usage_tracker.log_usage(
            user_id=user_id,
            username=update.effective_user.username or user_name,
            provider=inference.provider,
            model=inference.model,
            usage_stats=usage
        )

    logger.info(f"AI response: {response[:50]}...", extra={"user_id": user_id})
    
    # Check for Tool Triggers
    trigger_scan = "[[RUN:SCAN]]" in response
    trigger_status = "[[RUN:STATUS]]" in response
    trigger_cmd = "[[RUN:CMD:" in response
    trigger_antigravity = "[[ASK:ANTIGRAVITY:" in response
    trigger_search = "[[RUN:SEARCH:" in response
    
    # Clean response
    clean_response = response.replace("[[RUN:SCAN]]", "").replace("[[RUN:STATUS]]", "")
    
    # Extract CMD if present
    cmd_to_run = None
    if trigger_cmd:
        import re
        match = re.search(r'\[\[RUN:CMD:(.+?)\]\]', response)
        if match:
            cmd_to_run = match.group(1)
            clean_response = clean_response.replace(f"[[RUN:CMD:{cmd_to_run}]]", "")
    
    # Extract Antigravity question if present
    antigravity_question = None
    if trigger_antigravity:
        import re
        match = re.search(r'\[\[ASK:ANTIGRAVITY:(.+?)\]\]', response)
        if match:
            antigravity_question = match.group(1)
            clean_response = clean_response.replace(f"[[ASK:ANTIGRAVITY:{antigravity_question}]]", "")
            
    # Extract Search query if present
    search_query = None
    if trigger_search:
        import re
        match = re.search(r'\[\[RUN:SEARCH:(.+?)\]\]', response)
        if match:
            search_query = match.group(1)
            clean_response = clean_response.replace(f"[[RUN:SEARCH:{search_query}]]", "")
    
    clean_response = clean_response.strip()
    
    # Send response (handle long messages)
    if clean_response:
        if len(clean_response) > 4000:
            for i in range(0, len(clean_response), 4000):
                await update.message.reply_text(clean_response[i:i+4000])
        else:
            await update.message.reply_text(clean_response)

    # Execute Triggers
    if trigger_scan:
        logger.info("Executing Tool: SCAN")
        await cmd_scan(update, context)
    
    if trigger_status:
        logger.info("Executing Tool: STATUS")
        await cmd_status(update, context)
    
    if trigger_cmd and cmd_to_run:
        logger.info(f"Executing Server Command: {cmd_to_run}")
        # Whitelist safe commands
        safe_commands = ['free', 'df', 'uptime', 'ps', 'systemctl status', 'journalctl', 'ls', 'cat', 'grep', 'tail', 'head']
        is_safe = any(cmd_to_run.startswith(safe) for safe in safe_commands)
        
        if is_safe:
            import subprocess
            try:
                result = subprocess.run(
                    ['ssh', 'igor-gaming-1', cmd_to_run],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                output = result.stdout[:1000] if result.stdout else result.stderr[:1000]
                await update.message.reply_text(f"```\n{output}\n```", parse_mode="Markdown")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка: {e}")
        else:
            await update.message.reply_text("⚠️ Команда не в whitelist. Для безопасности отклонено.")
    
    if trigger_antigravity and antigravity_question:
        logger.info(f"Forwarding to Antigravity: {antigravity_question}")
        # TODO: Implement actual Antigravity API call
        # For now, just acknowledge
        await update.message.reply_text(
            f"📨 Вопрос передан Antigravity Core:\n\"{antigravity_question}\"\n\n"
            f"💡 Пока эта функция в разработке. Antigravity ответит через основной интерфейс."
        )
        
    if trigger_search and search_query:
        logger.info(f"Executing Search: {search_query}")
        await update.message.reply_text(f"🔍 Ищу: {search_query}...")
        search_result = await web_search.search(search_query)
        await update.message.reply_text(search_result, parse_mode="Markdown")
        
        # Optional: Feed result back to AI?
        # For now, just showing to user.


async def handle_approval_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle approval/denial button clicks AND model switching."""
    query = update.callback_query
    await query.answer()
    
    # Handle model switching
    if query.data.startswith("model:"):
        model = query.data.split(":", 1)[1]
        provider = inference.provider
        
        # Set model based on provider
        if provider == "gemini":
            config.set("GEMINI_MODEL", model)
        elif provider == "openai":
            config.set("OPENAI_MODEL", model)
        else:  # ollama
            config.set("OLLAMA_MODEL", model)
        
        config.set("MODEL_NAME", model)
        
        await query.edit_message_text(
            f"✅ **Model switched to:**\n\n`{model}`",
            parse_mode="Markdown"
        )
        logger.info(f"User {query.from_user.id} switched to model: {model}")
        return
    
    # Only admin can approve users
    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("⛔ Только администратор может одобрять пользователей.")
        return
    
    action, user_id_str = query.data.split("_")
    user_id = int(user_id_str)
    
    if action == "approve":
        if user_id not in ALLOWED_USERS:
            ALLOWED_USERS.append(user_id)
            
            # Save to file for persistence
            config_path = Path(__file__).parent.parent / ".env"
            try:
                with open(config_path, "a") as f:
                    f.write(f"\n# Auto-approved user {user_id}\n")
                logger.info(f"User {user_id} approved by admin")
            except Exception as e:
                logger.error(f"Failed to save approved user: {e}")
            
            await query.edit_message_text(
                f"✅ **Пользователь одобрен**\n\n"
                f"🆔 User ID: `{user_id}`\n\n"
                f"Пользователь может теперь использовать бота.\n"
                f"⚠️ Ему нужно будет установить свой API ключ через `/setapikey`",
                parse_mode="Markdown"
            )
            
            # Notify approved user
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="✅ **Доступ одобрен!**\n\n"
                         "Вы можете использовать бота.\n\n"
                         "⚠️ Для работы с AI моделями установите API ключ:\n"
                         "`/setapikey ваш_ключ`\n\n"
                         "Или используйте `/setprovider ollama` для локальной модели.",
                    parse_mode="Markdown"
                )
            except Exception as e:
                logger.error(f"Failed to notify approved user: {e}")
        else:
            await query.edit_message_text(f"ℹ️ Пользователь {user_id} уже в whitelist.")
    
    elif action == "deny":
        await query.edit_message_text(
            f"❌ **Доступ отклонён**\n\n"
            f"🆔 User ID: `{user_id}`",
            parse_mode="Markdown"
        )
        
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Доступ к боту отклонён администратором."
            )
        except Exception:
            pass


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
    
    # Notify user if possible
    if isinstance(update, Update) and update.effective_message:
        text = "❌ Произошла внутренняя ошибка. Администратор уведомлен."
        try:
            await update.effective_message.reply_text(text)
        except:
            pass
            
    # Send traceback to admins (optional, maybe too noisy)
    # import traceback
    # tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    # tb_string = "".join(tb_list)
    # logger.error(tb_string)


async def process_text_request(text: str, user_id: int) -> str:
    """Process a text request from any source (Telegram, Alice) and return response string."""
    # 1. Get context
    history = conv_manager.get_context_messages(user_id, limit=3) # Limit context for Alice
    messages = history + [{"role": "user", "content": text}]
    
    # 2. Add to history
    conv_manager.add_message(user_id, "user", text)
    
    # 3. Inference
    response, usage = await inference.chat(messages, system_prompt=SYSTEM_PROMPT)
    
    # 4. Save response
    conv_manager.add_message(user_id, "assistant", response)
    
    # 5. Log Usage
    if usage and usage.get("total_tokens", 0) > 0:
        logger.info(f"Token Usage: {usage}", extra={"user_id": user_id})
        usage_tracker.log_usage(user_id, "AliceUser", inference.provider, inference.model, usage)

    # 6. Process Triggers (Simplified for Alice)
    clean_response = response
    
    if "[[RUN:SCAN]]" in response:
        clean_response = clean_response.replace("[[RUN:SCAN]]", "").strip()
        # Alice can't see the scan result immediately if it's async, allow simple ack
        clean_response += "\n(Запускаю сканирование...)"
        # Fire and forget scan
        # We need 'update' object for cmd_scan, which we don't have here. 
        # So skips scanning implementation for Alice for now or mock it.
        
    if "[[RUN:STATUS]]" in response:
         clean_response = clean_response.replace("[[RUN:STATUS]]", "").strip()
         status = config.get_status()
         clean_response += f"\nСтатус: {status}"

    # Handle HA commands via text intent if possible (not implemented fully via generic chat yet)
    # But if user says "vkluchi light", AI might output text description.
    
    return clean_response


async def post_init(application: Application) -> None:
    """Post-initialization hook."""
    # Set commands
    commands = [
        BotCommand("start", "🚀 Запустить бота"),
        BotCommand("help", "❓ Помощь"),
        BotCommand("status", "📊 Статус системы"),
        BotCommand("models", "🧠 Выбор модели"),
        BotCommand("scan", "🕵️‍♂️ Поиск вакансий"),
        BotCommand("imagine", "🎨 Генерация картинок"),
        BotCommand("search", "🌐 Поиск"),
        BotCommand("todo", "📝 Задачи"),
        BotCommand("remind", "⏰ Напоминания"),
        BotCommand("infra", "🏗 Инфраструктура"),
        BotCommand("backup", "📦 Бэкап"),
        BotCommand("notify", "🔔 Уведомления"),
        BotCommand("update", "🔄 Обновить систему"),
        BotCommand("ha", "🏠 Умный дом"),
        BotCommand("clear", "🧹 Очистить контекст"),
    ]
    await application.bot.set_my_commands(commands)
    
    # Start Alice Skill
    alice_skill.set_handler(process_text_request)
    await alice_skill.start()
    
    # Start Scheduler
    scheduler.set_application(application)
    scheduler.start()
    
    # Initialize Digest Service (needs other services)
    global digest_service
    digest_service = DigestService(usage_tracker, task_manager, linear_client, infra_manager, calendar_client)
    
    # Schedule Daily Digest (at 09:00 AM)
    scheduler.scheduler.add_job(
        send_daily_digest,
        'cron',
        hour=9,
        minute=0,
        args=[application]
    )
    
    # Schedule Daily Backup (at 03:00 AM)
    scheduler.scheduler.add_job(
        run_auto_backup,
        'cron',
        hour=3,
        minute=0,
        args=[application]
    )

    logger.info("Alice Skill & Scheduler started.")
    
    # Start Periodic Scheduler
    asyncio.create_task(run_periodic_scan(application))
    
    # Start Web Dashboard
    dashboard = DashboardService(port=8096, context={
        "infra": infra_manager,
        "usage": usage_tracker
    })
    dashboard.start()
    logger.info("Web Dashboard started on port 8096")


async def send_daily_digest(application: Application):
    """Send daily digest to all users."""
    try:
        # Send to admin (or all allowed users)
        if ADMIN_ID and digest_service:
            # Get admin username from config or use default
            username = "Admin"
            digest = await digest_service.generate_digest(ADMIN_ID, username)
            
            await notify_manager.send(
                application.bot,
                ADMIN_ID,
                digest,
                priority=NotificationManager.NORMAL,
                parse_mode="Markdown"
            )
            logger.info("Daily digest sent")
    except Exception as e:
        logger.error(f"Failed to send daily digest: {e}")


async def run_auto_backup(application: Application):
    """Run automatic daily backup."""
    # We need to send to admin
    try:
        # Re-use cmd_backup logic or perform simplified backup
        # Since cmd_backup requires 'update' object, we write custom logic here 
        # OR mock update object. Writing custom logic is cleaner.
        
        import zipfile
        import os
        from datetime import datetime
        
        files = ["tasks.db", "usage.db", "jobs.db"]
        backup_name = f"daily_backup_{datetime.now().strftime('%Y%m%d')}.zip"
        
        with zipfile.ZipFile(backup_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files:
                 if os.path.exists(file):
                    zipf.write(file)
        
        # Send to Admin
        if ADMIN_ID:
             await notify_manager.send(
                 application.bot,
                 ADMIN_ID,
                 "📦 Автоматический ежедневный бэкап",
                 priority=NotificationManager.NORMAL  # Don't wake up at 3am
             )
             # Attach file separately (send doesn't support document)
             await application.bot.send_document(
                chat_id=ADMIN_ID,
                document=open(backup_name, "rb")
            )
             os.remove(backup_name)
             
    except Exception as e:
        logger.error(f"Auto-backup failed: {e}")


async def run_periodic_scan(application: Application):
    """Run Job Hunter every 4 hours automatically."""
    interval_hours = 4
    logger.info(f"⏰ Scheduler started. Will scan every {interval_hours} hours.")
    
    while True:
        try:
            # Wait first (don't run immediately on restart to avoid spam loop if crashing)
            await asyncio.sleep(interval_hours * 3600)
            
            logger.info("⏰ Auto-Running Job Hunter...")
            # We need a dummy update/context or just run the logic directly.
            # cmd_scan expects (update, context) which we don't have.
            # So we reproduce the cmd_scan logic here but formatted for broadcast/admin only.
            
            # Assuming we only notify the ADMIN (User ID from config or last known)
            # For now, let's just log it or try to find a way to reuse cmd_scan.
            # The easier way is to just call the script logic directly.
            
            script_path = "/home/gonya/Documents/Unified_System/Scripts/automation/job_hunter.py"
            venv_python = "/home/gonya/Documents/Unified_System/venv/bin/python"
            
            import subprocess
            process = await asyncio.create_subprocess_exec(
                venv_python, script_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            logger.info(f"⏰ Job Hunter launched via Scheduler (PID: {process.pid})")
            
        except Exception as e:
            logger.error(f"Scheduler Error: {e}")
            await asyncio.sleep(600) # Retry in 10 mins on error


def get_health_info() -> dict:
    """Return health info for the health check endpoint."""
    return {
        "inference_url": config.get("INFERENCE_BASE_URL"),
        "model": config.get("MODEL_NAME"),
    }


def main() -> None:
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("🚀 AI Telegram Bot Starting...")
    logger.info("=" * 60)
    
    # Start health server
    start_health_server(port=8095, health_callback=get_health_info)
    
    # Get bot token
    token = config.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        sys.exit(1)
    
    # Build application
    application = (
        Application.builder()
        .token(token)
        .post_init(post_init)
        .build()
    )
    
    # Add handlers
    application.add_handler(CommandHandler("start", cmd_start))
    application.add_handler(CommandHandler("help", cmd_help))
    application.add_handler(CommandHandler("status", cmd_status))
    application.add_handler(CommandHandler("models", cmd_models))
    application.add_handler(CommandHandler("clear", cmd_clear))
    application.add_handler(CommandHandler("imagine", cmd_imagine))
    application.add_handler(CommandHandler("ha", cmd_ha))
    application.add_handler(CommandHandler("setprovider", cmd_setprovider))
    application.add_handler(CommandHandler("setendpoint", cmd_setendpoint))
    application.add_handler(CommandHandler("setapikey", cmd_setapikey))
    application.add_handler(CommandHandler("setmodel", cmd_setmodel))
    application.add_handler(CommandHandler("usage", cmd_usage))
    application.add_handler(CommandHandler("costs", cmd_costs))
    application.add_handler(CommandHandler("search", cmd_search))
    application.add_handler(CommandHandler("linear", cmd_linear))
    application.add_handler(CommandHandler("digest", cmd_digest))
    application.add_handler(CommandHandler("calendar", cmd_calendar))
    application.add_handler(CommandHandler("todo", cmd_todo))
    application.add_handler(CommandHandler("remind", cmd_remind))
    application.add_handler(CommandHandler("infra", cmd_infra))
    application.add_handler(CommandHandler("backup", cmd_backup))
    application.add_handler(CommandHandler("notify", cmd_notify))
    application.add_handler(CommandHandler("update", cmd_update))
    application.add_handler(CommandHandler("scan", cmd_scan))
    
    # Handle voice messages
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    # Handle photos
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add callback query handler for approval buttons
    from telegram.ext import CallbackQueryHandler
    application.add_handler(CallbackQueryHandler(handle_approval_callback))
    
    application.add_error_handler(error_handler)
    
    logger.info("✅ Bot is online and listening...")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
