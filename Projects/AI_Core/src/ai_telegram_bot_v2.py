import logging
import os
import asyncio
import aiohttp
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ChatAction
import bot_config
from user_context_db import UserContextDB
from google_auth import GoogleAuthManager
from calendar_client import CalendarClient

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
db = UserContextDB()
auth_manager = GoogleAuthManager(client_secrets_file="client_secret.json")

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

# keyboards
def get_main_menu():
    keyboard = [
        ["📅 Daily Brief", "➕ New Task"],
        ["🧠 Memory/Context", "❓ Help"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # 1. Register User
    db.add_user(user.id, user.username, user.full_name)
    logger.info(f"User {user.id} ({user.username}) started the bot.")

    # 2. Check Auth/Approval
    if not db.is_approved(user.id):
        # Auto-approve if in ALLOWED_USER_IDS
        if user.id in bot_config.ALLOWED_USER_IDS:
            db.approve_user(user.id, True)
        else:
            await update.message.reply_text("⛔️ Access Denied. Your ID is pending approval.")
            return

    # 3. Check Google Connection
    user_data = db.get_user(user.id)
    if not user_data or not user_data['is_google_connected']:
        # Show Connect Button
        keyboard = [
            [InlineKeyboardButton("🔗 Connect Google Calendar", callback_data="connect_google")],
            [InlineKeyboardButton("❓ Help", callback_data="help_onboarding")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_html(
            rf'Welcome, {user.mention_html()}! 🚀\n\nTo assist you properly, I need access to your Calendar.',
            reply_markup=reply_markup
        )
    else:
        # Show Main Menu
        await update.message.reply_html(
            rf'Welcome back, {user.mention_html()}! Ready to assist.',
            reply_markup=get_main_menu()
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Acknowledge
    
    data = query.data
    if data == "connect_google":
        auth_url = auth_manager.get_auth_url()
        if auth_url:
            await query.edit_message_text(
                f"Please visit this link to authorize:\n{auth_url}\n\n"
                "After authorizing, copy the code and send it here (starting with 4/)."
            )
        else:
            await query.edit_message_text("❌ Error: `client_secret.json` is missing on the server. Please contact Admin.")
    
    elif data == "help_onboarding":
        await query.edit_message_text("I am an AI assistant integrated with your Calendar. Connect to start.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        return

    user_text = update.message.text
    logger.info(f"Query from {user_id}: {user_text}")
    
    # Check for Auth Code
    if user_text.strip().startswith("4/"):
        await update.message.reply_text("🔄 Verifying code...")
        credentials = auth_manager.exchange_code(user_text.strip())
        if credentials:
            # Save to DB
            import sqlite3
            with sqlite3.connect("user_context.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET google_creds = ?, is_google_connected = 1 WHERE user_id = ?",
                    (credentials.to_json(), user_id)
                )
                conn.commit()
            
            await update.message.reply_text("✅ Success! Google Calendar connected.", reply_markup=get_main_menu())
            return
        else:
            await update.message.reply_text("❌ Invalid code or connection failed. Try again.")
            return

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Mock response for now
    ai_response = await query_ollama(user_text)
    await update.message.reply_text(ai_response, reply_markup=get_main_menu())

async def query_ollama(prompt: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": bot_config.MODEL_NAME, 
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

def main():
    if not bot_config.BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        return

    application = Application.builder().token(bot_config.BOT_TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print(f'Bot V2 (AI_Core) is running... Allowed Users: {bot_config.ALLOWED_USER_IDS}')
    application.run_polling()

if __name__ == '__main__':
    main()
