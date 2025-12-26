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
from .health import start_health_server
from .logging_config import setup_logging

# Initialize logging first
setup_logging()
logger = logging.getLogger(__name__)

# Global instances
config = ConfigManager()
inference = InferenceClient(config)

# System prompt for AI responses
SYSTEM_PROMPT = """Ты - Гоня (Gonya), умный AI ассистент в системе 'Unified System'.
Ты работаешь на сервере `igor-gaming-1`.
Твоя главная цель - быть полезным и исполнительным.

У тебя есть доступ к следующим ИНСТРУМЕНТАМ (Tools):
1. ПРОВЕРКА ВАКАНСИЙ: Если пользователь просит "проверить почту", "найти работу", "просканировать вакансии", "job hunt" - ты должен добавить в ответ специальный тег: [[RUN:SCAN]].
2. СТАТУС СИСТЕМЫ: Если пользователь спрашивает "как дела", "статус", "мониторинг" - добавь тег: [[RUN:STATUS]].

ПРИМЕРЫ:
User: "Найди мне работу"
AI: "Хорошо, запускаю анализ свежих вакансий через Job Hunter. [[RUN:SCAN]]"

User: "Как там сервер?"
AI: "Проверяю системы... [[RUN:STATUS]]"

В обычных разговорах просто отвечай на вопрос."""


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "👋 Привет! Я твой AI ассистент Unified System.\n\n"
        "Команды:\n"
        "/scan - 🕵️‍♂️ Запустить поиск вакансий (Job Hunter)\n"
        "/status - 📊 Статус системы\n"
        "/models - 📋 Список моделей\n"
        "/setprovider <name> - ⚙️ Выбрать AI (ollama/openai/gemini)\n"
        "/setendpoint <url> - 🔗 Адрес API\n"
        "/setapikey <key> - 🔑 Установить ключ\n"
        "/setmodel <name> - 🧠 Выбрать модель\n"
        "/help - ❓ Помощь"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await cmd_start(update, context)


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
    """Handle /models command - list available models from provider."""
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
    
    # Format models list (limit to 30 for readability)
    models_display = models[:30]
    models_text = "\n".join([f"• `{m}`" for m in models_display])
    
    if len(models) > 30:
        models_text += f"\n\n_...and {len(models) - 30} more_"
    
    await update.message.reply_text(
        f"📋 **Available Models ({len(models)})**\n\n{models_text}",
        parse_mode="Markdown"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular text messages - send to AI."""
    user_text = update.message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "User"
    
    logger.info(f"Message from {user_name}: {user_text[:50]}...", extra={"user_id": user_id})
    
    # Send typing indicator
    await update.message.chat.send_action("typing")
    
    # Build message for AI
    messages = [{"role": "user", "content": user_text}]
    
    # Get AI response
    response = await inference.chat(messages, system_prompt=SYSTEM_PROMPT)
    
    logger.info(f"AI response: {response[:50]}...", extra={"user_id": user_id})
    
    # Check for Tool Triggers
    trigger_scan = "[[RUN:SCAN]]" in response
    trigger_status = "[[RUN:STATUS]]" in response
    
    # Clean response
    clean_response = response.replace("[[RUN:SCAN]]", "").replace("[[RUN:STATUS]]", "").strip()
    
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
    application.add_handler(CommandHandler("setprovider", cmd_setprovider))
    application.add_handler(CommandHandler("setendpoint", cmd_setendpoint))
    application.add_handler(CommandHandler("setapikey", cmd_setapikey))
    application.add_handler(CommandHandler("setmodel", cmd_setmodel))
    application.add_handler(CommandHandler("scan", cmd_scan))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    logger.info("✅ Bot is online and listening...")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
