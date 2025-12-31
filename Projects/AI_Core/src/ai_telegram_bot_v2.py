import logging
import os
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ChatAction
import bot_config
from user_context_db import UserContextDB
from google_auth import GoogleAuthManager
from calendar_client import CalendarClient
from daily_scheduler import DailyScheduler

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

def get_calendar_client(user_id: int) -> Optional[CalendarClient]:
    user_data = db.get_user(user_id)
    if user_data and user_data['is_google_connected'] and user_data['google_creds']:
        try:
            creds_dict = json.loads(user_data['google_creds'])
            return CalendarClient(credentials_dict=creds_dict)
        except Exception as e:
            logger.error(f"Failed to create CalendarClient for {user_id}: {e}")
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # 1. Register User & Update Interaction
    db.add_user(user.id, user.username, user.full_name)
    db.update_last_interaction(user.id)
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
            rf'Welcome, {user.mention_html()}! 🚀'
            '\n\nTo assist you properly, I need access to your Calendar.',
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
    user_id = update.effective_user.id
    db.update_last_interaction(user_id)

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
    
    elif data.startswith("confirm_event_"):
        pending = context.user_data.get('pending_event')
        if not pending:
            await query.edit_message_text("❌ No pending event found or session expired.")
            return
        
        client = get_calendar_client(user_id)
        if not client:
            await query.edit_message_text("❌ Calendar not connected. Please run /start.")
            return
        
        # Parse time
        try:
            start_time = datetime.fromisoformat(pending['time'].replace('Z', '+00:00'))
        except:
            start_time = datetime.now() + timedelta(hours=1) # Default
            
        success = client.create_event(
            summary=pending['summary'],
            start_time=start_time,
            description=pending.get('context', '')
        )
        
        if success:
            # Store in context DB too
            import sqlite3
            with sqlite3.connect("user_context.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO event_contexts (user_id, event_title, context_description, event_time, created_at) VALUES (?, ?, ?, ?, ?)",
                    (user_id, pending['summary'], pending.get('context', ''), start_time, datetime.now())
                )
                conn.commit()
            
            await query.edit_message_text(f"✅ Scheduled: **{pending['summary']}**\nTime: {pending['time']}", parse_mode='Markdown')
        else:
            await query.edit_message_text("❌ Failed to create event in Google Calendar.")
        
        context.user_data.pop('pending_event', None)

    elif data == "cancel_event":
        context.user_data.pop('pending_event', None)
        await query.edit_message_text("❌ Event creation cancelled.")
    
    elif data == "edit_context":
        await query.edit_message_text("Feature coming soon! For now, try adding the event again with more details.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        return

    db.update_last_interaction(user_id)
    user_text = update.message.text
    logger.info(f"Query from {user_id}: {user_text}")
    
    # 1. Check for Auth Code
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

    # 2. Handle Menu Commands
    if user_text == "📅 Daily Brief":
        await show_daily_brief(update, context)
        return
    elif user_text == "➕ New Task":
        await update.message.reply_text("What should I schedule? (e.g., 'Meeting with Sarah tomorrow at 10am')")
        return
    elif user_text == "❓ Help":
        await update.message.reply_text("I can help you manage your calendar. Try 'Show my schedule' or 'Add event'.")
        return

    # 3. AI Intent Parsing & Response
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    lower_text = user_text.lower()
    
    # Check for "Add Event" intent manually or via AI
    if any(k in lower_text for k in ["schedule", "add", "meeting", "запиши", "встреча", "назначь"]):
        event_details = await parse_event_details(user_text)
        if event_details and 'summary' in event_details:
            summary = event_details['summary']
            time_str = event_details.get('time', 'Unknown')
            context_desc = event_details.get('context', 'No context provided')
            
            keyboard = [
                [InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_event_{summary[:20]}")],
                [InlineKeyboardButton("✏️ Edit Context", callback_data="edit_context")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_event")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                f"📅 **Found Event:**\n"
                f"📝 Title: {summary}\n"
                f"⏰ Time: {time_str}\n"
                f"💡 Context: {context_desc}\n\n"
                "Should I add this to your calendar?",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            # Store event details in user_data/context for confirmation
            context.user_data['pending_event'] = event_details
            return
    
    if any(k in lower_text for k in ["schedule", "brief", "plan", "план"]):
        await show_daily_brief(update, context)
        return

    ai_response = await query_ollama(user_text)
    await update.message.reply_text(ai_response, reply_markup=get_main_menu())

async def parse_event_details(text: str) -> Optional[Dict[str, Any]]:
    prompt = (
        "Extract event details from this text for a calendar: '" + text + "'. "
        "Current local time: " + datetime.now().isoformat() + ". "
        "Return ONLY a JSON object with keys: summary, time (ISO format), context (reason for event)."
    )
    
    response = await query_ollama(prompt, system="You are a data extractor. Return JSON only.")
    try:
        # Simple extraction logic (might need more robust cleaning if Ollama adds fluff)
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != -1:
            return json.loads(response[start:end])
    except Exception as e:
        logger.error(f"Failed to parse event JSON: {e} | Response: {response}")
    return None

async def show_daily_brief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    client = get_calendar_client(user_id)
    
    if not client:
        await update.message.reply_text("❌ Calendar not connected. Please run /start to connect.")
        return
    
    events = client.get_upcoming_events(days=1)
    if not events:
        await update.message.reply_text("You have no events scheduled for today. Ready for new tasks!")
    else:
        resp = "📅 **Your Daily Brief:**\n\n"
        for e in events:
            resp += f"• {client.format_event(e)}\n"
        await update.message.reply_text(resp, parse_mode='Markdown')

async def query_ollama(prompt: str, system: str = None) -> str:
    system_prompt = system or "You are a helpful personal assistant bot. You manage the user's Google Calendar and provide insights. Be concise and professional."
    full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
    
    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": bot_config.MODEL_NAME, 
                "prompt": full_prompt,
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

async def post_init(application: Application) -> None:
    # Start the DailyScheduler
    scheduler = DailyScheduler(application, db)
    asyncio.create_task(scheduler.start())
    logger.info("DailyScheduler background task started via post_init.")

def main():
    if not bot_config.BOT_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        return

    application = Application.builder().token(bot_config.BOT_TOKEN).post_init(post_init).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print(f'Bot V2 (AI_Core) is running... Allowed Users: {bot_config.ALLOWED_USER_IDS}')
    application.run_polling()

if __name__ == '__main__':
    main()
