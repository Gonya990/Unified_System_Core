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

# Initialize logging first
setup_logging()
logger = logging.getLogger(__name__)

# Global instances
config = ConfigManager()
inference = InferenceClient(config)
conv_manager = ConversationManager(storage_path="conversations")

# System prompt for AI responses
SYSTEM_PROMPT = """Ты - Гоня (Gonya), умный AI ассистент в системе 'Unified System'.
Ты работаешь на сервере `igor-gaming-1` и имеешь доступ к серверным командам.
Твоя главная цель - быть полезным и исполнительным.

У тебя есть доступ к следующим ИНСТРУМЕНТАМ (Tools):
1. ПРОВЕРКА ВАКАНСИЙ: "проверить почту", "найти работу", "просканировать вакансии" → [[RUN:SCAN]]
2. СТАТУС СИСТЕМЫ: "как дела", "статус", "мониторинг", "здоровье сервера" → [[RUN:STATUS]]
3. КОМАНДЫ СЕРВЕРА: "выполни команду", "запусти на сервере", "проверь процессы" → [[RUN:CMD:<команда>]]
4. СВЯЗЬ С ANTIGRAVITY: "спроси у Antigravity", "передай Antigravity", "нужна помощь агента" → [[ASK:ANTIGRAVITY:<вопрос>]]

ПРИМЕРЫ:
User: "Найди мне работу"
AI: "Хорошо, запускаю анализ свежих вакансий. [[RUN:SCAN]]"

User: "Проверь, сколько памяти использует сервер"
AI: "Проверяю использование памяти... [[RUN:CMD:free -h]]"

User: "Спроси у Antigravity, как настроить автозапуск"
AI: "Передаю вопрос главному агенту... [[ASK:ANTIGRAVITY:Как настроить автозапуск службы?]]"

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
        "/help - ❓ Помощь"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await cmd_start(update, context)


@require_auth
async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command - show current configuration."""
    status = config.get_status()
    
    # Get provider info
    provider = inference.provider.upper()
    
    # Check inference health
    is_healthy = await inference.health_check()
    health_emoji = "✅" if is_healthy else "❌"
    
    await update.message.reply_text(
        f"📊 **Статус Бота**\n\n"
        f"🌐 Провайдер: `{provider}`\n"
        f"🔗 URL: `{inference.base_url}`\n"
        f"🤖 Модель: `{inference.model}`\n"
        f"🔑 API Ключ: {'✅ Установлен' if status['api_key_set'] else '❌ Не установлен'}\n"
        f"💚 Связь: {health_emoji} {'Онлайн' if is_healthy else 'Оффлайн'}",
        parse_mode="Markdown"
    )


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
    response = await inference.chat(messages, system_prompt=SYSTEM_PROMPT)
    
    # Save assistant response to history
    conv_manager.add_message(user_id, "assistant", response)
    
    logger.info(f"AI response: {response[:50]}...", extra={"user_id": user_id})
    
    # Check for Tool Triggers
    trigger_scan = "[[RUN:SCAN]]" in response
    trigger_status = "[[RUN:STATUS]]" in response
    trigger_cmd = "[[RUN:CMD:" in response
    trigger_antigravity = "[[ASK:ANTIGRAVITY:" in response
    
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
        
        # Notify denied user
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Доступ к боту отклонён администратором."
            )
        except Exception:
            pass


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle errors."""
    logger.error(f"Update {update} caused error: {context.error}")


async def post_init(application: Application) -> None:
    """Set up bot commands after initialization."""
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help message"),
        BotCommand("status", "Show current configuration"),
        BotCommand("models", "List available models"),
        BotCommand("clear", "Clear conversation history"),
        BotCommand("setprovider", "Set provider (ollama/openai/gemini)"),
        BotCommand("setendpoint", "Set inference API URL"),
        BotCommand("setapikey", "Set API key"),
        BotCommand("setmodel", "Set model name"),
        BotCommand("scan", "Run Job Hunter Analysis"),
    ]
    await application.bot.set_my_commands(commands)
    
    # Start Periodic Scheduler
    asyncio.create_task(run_periodic_scan(application))


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
    start_health_server(port=8085, health_callback=get_health_info)
    
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
    application.add_handler(CommandHandler("setprovider", cmd_setprovider))
    application.add_handler(CommandHandler("setendpoint", cmd_setendpoint))
    application.add_handler(CommandHandler("setapikey", cmd_setapikey))
    application.add_handler(CommandHandler("setmodel", cmd_setmodel))
    application.add_handler(CommandHandler("scan", cmd_scan))
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
