import logging
import os
import asyncio
import aiohttp
import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import bot_config

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3" # Will fallback or be configurable

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='bot_journal.log',
    filemode='a'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        rf'Привет, {user.mention_html()}! Я Antigravity (Local Node). Я подключен к Ollama и файловой системе.'
    )

async def check_auth(update: Update) -> bool:
    user_id = update.effective_user.id
    if user_id not in bot_config.ALLOWED_USER_IDS:
        logger.warning(f"Unauthorized access attempt from {user_id}")
        return False
    return True

async def query_ollama(prompt: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            # First, list models to find the best one
            # For now, hardcode llama3 or mistral, usually present.
            payload = {
                "model": "llama3", 
                "prompt": prompt,
                "stream": False
            }
            async with session.post(OLLAMA_URL, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("response", "No response from model.")
                else:
                    return f"Error from Ollama: {response.status}"
    except Exception as e:
        return f"Ollama Connection Error: {e}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_auth(update):
        return

    user_text = update.message.text
    user_id = update.effective_user.id
    
    logger.info(f"Query from {user_id}: {user_text}")
    
    # Simple Logic: Check if command starts with specific keywords for file ops
    # Otherwise send to AI
    
    response_text = "Analysis..."
    loading_msg = await update.message.reply_text("Thinking...")

    # AI Processing
    ai_response = await query_ollama(user_text)
    
    await context.bot.edit_message_text(
        chat_id=update.effective_chat.id,
        message_id=loading_msg.message_id,
        text=ai_response
    )

def main():
    application = Application.builder().token(bot_config.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print('Bot V2 is running...')
    application.run_polling()

if __name__ == '__main__':
    main()
