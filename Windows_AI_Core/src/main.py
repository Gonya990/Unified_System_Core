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
SYSTEM_PROMPT = """You are Gonya, a smart and helpful AI assistant in the 'Unified System'.
You run on a configurable inference backend (Ollama, OpenAI, or custom).
Always answer helpfully and concisely.
If asked about the system, mention you are a cloud-native Telegram bot."""


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "👋 Hello! I'm your AI assistant.\n\n"
        "Commands:\n"
        "/status - Show current configuration\n"
        "/models - List available models\n"
        "/setendpoint <url> - Set inference API URL\n"
        "/setapikey <key> - Set API key\n"
        "/setmodel <name> - Set model name\n"
        "/help - Show this help message"
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command."""
    await cmd_start(update, context)


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command - show current configuration."""
    status = config.get_status()
    
    # Check inference health
    is_healthy = await inference.health_check()
    health_emoji = "✅" if is_healthy else "❌"
    
    await update.message.reply_text(
        f"📊 **Bot Status**\n\n"
        f"🔗 Inference URL: `{status['inference_url']}`\n"
        f"🤖 Model: `{status['model']}`\n"
        f"🔑 API Key: {'✅ Set' if status['api_key_set'] else '❌ Not set'}\n"
        f"💚 Connection: {health_emoji} {'Online' if is_healthy else 'Offline'}",
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
    config.set("INFERENCE_API_KEY", api_key)
    logger.info("API key updated", extra={"user_id": update.effective_user.id})
    
    # Try to delete the message containing the API key
    try:
        await update.message.delete()
    except Exception:
        pass
    
    await update.message.reply_text("✅ API key has been set and encrypted.")


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
    
    # Send response (handle long messages)
    if len(response) > 4000:
        # Split into chunks
        for i in range(0, len(response), 4000):
            await update.message.reply_text(response[i:i+4000])
    else:
        await update.message.reply_text(response)


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
        BotCommand("setendpoint", "Set inference API URL"),
        BotCommand("setapikey", "Set API key"),
        BotCommand("setmodel", "Set model name"),
    ]
    await application.bot.set_my_commands(commands)


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
    start_health_server(port=8080, health_callback=get_health_info)
    
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
    application.add_handler(CommandHandler("setendpoint", cmd_setendpoint))
    application.add_handler(CommandHandler("setapikey", cmd_setapikey))
    application.add_handler(CommandHandler("setmodel", cmd_setmodel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    logger.info("✅ Bot is online and listening...")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
