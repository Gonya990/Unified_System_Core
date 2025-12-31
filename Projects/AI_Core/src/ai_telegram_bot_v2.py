import logging
import os
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ChatAction
import bot_config
from user_context_db import UserContextDB
from google_auth import GoogleAuthManager
from calendar_client import CalendarClient
from daily_scheduler import DailyScheduler
from conversation_manager import ConversationManager

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
db = UserContextDB()
auth_manager = GoogleAuthManager(client_secrets_file="client_secret.json")
conv_manager = ConversationManager()

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
def get_main_menu(user_id: int):
    keyboard = [
        ["📅 Daily Brief", "➕ New Task"],
        ["🧠 Memory/Context", "❓ Help"]
    ]
    if user_id in bot_config.ALLOWED_USER_IDS:
        keyboard.append(["🛠 Admin Panel"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)

def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Service Status", callback_data="admin_services")],
        [InlineKeyboardButton("🔑 Manage Keys", callback_data="admin_keys")],
        [InlineKeyboardButton("👥 User Management", callback_data="admin_users")],
        [InlineKeyboardButton("🔙 Back", callback_data="show_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

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
            reply_markup=get_main_menu(user.id)
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
        await show_advanced_help(query, context, edit=True)
    
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
    
    elif data == "clear_memory":
        db.clear_memories(user_id)
        conv_manager.clear_history(user_id)
        await query.edit_message_text("🗑 Memory and conversation history cleared.")
    
    elif data == "show_help":
        await show_advanced_help(query, context, edit=True)
    
    elif data == "daily_brief_cb":
        # Simulate '📅 Daily Brief' command
        await show_daily_brief(query, context)
    
    elif data == "show_memories_cb":
        # Simulate '🧠 Memory/Context' command
        await show_memory_context(query, context)
        
    elif data == "settings_cb":
        await query.edit_message_text("⚙️ **Settings**\n\nNotifications: ON\nProactive Nudge: ON (3 days)\nAI Model: " + bot_config.MODEL_NAME, parse_mode='Markdown')

    # Admin Handlers
    elif data == "admin_services":
        if user_id not in bot_config.ALLOWED_USER_IDS: return
        status = "🟢 ollama: Up 2 hours\n🟢 telegram-bot: Up 30 mins\n🟡 postgres: Restarting"
        await query.edit_message_text(f"🛠 **Service Status:**\n\n```\n{status}\n```", parse_mode='Markdown', reply_markup=get_admin_menu())

    elif data == "admin_keys":
        if user_id not in bot_config.ALLOWED_USER_IDS: return
        await query.edit_message_text("🔑 **Key Management:**\n\n- OLLAMA_URL: Set\n- TELEGRAM_TOKEN: Set\n- GOOGLE_CLIENT_ID: Set", reply_markup=get_admin_menu())

    elif data == "admin_users":
        if user_id not in bot_config.ALLOWED_USER_IDS: return
        users = db.get_inactive_users(hours=0) # Get all users
        resp = "👥 **User Management:**\n\n"
        for u in users:
            status = "✅" if u['is_approved'] else "⏳"
            resp += f"{status} {u['full_name']} (@{u['username']})\n"
        await query.edit_message_text(resp, reply_markup=get_admin_menu())

async def show_advanced_help(update_or_query, context, edit=False):
    text = (
        "🤖 **Digital Assistant Help**\n\n"
        "I can help you with:\n"
        "• **Calendar**: Connect your Google account to manage events.\n"
        "• **Memory**: I remember key facts from our chats to help you better.\n"
        "• **Insights**: Ask me 'What did we decide about X?' to recall context.\n"
        "• **Proactivity**: I'll nudge you if we haven't spoken in a while.\n\n"
        "**Quick Actions:**"
    )
    keyboard = [
        [InlineKeyboardButton("📅 Today's Brief", callback_data="daily_brief_cb")],
        [InlineKeyboardButton("🧠 My Memories", callback_data="show_memories_cb")],
        [InlineKeyboardButton("⚙️ Settings", callback_data="settings_cb")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if edit:
        await update_or_query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update_or_query.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        return

    db.update_last_interaction(user_id)
    user_text = update.message.text
    logger.info(f"Query from {user_id}: {user_text}")
    
    if user_text.strip().startswith("4/"):
        await update.message.reply_text("🔄 Verifying code...")
        credentials = auth_manager.exchange_code(user_text.strip())
        if credentials:
            import sqlite3
            with sqlite3.connect("user_context.db") as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET google_creds = ?, is_google_connected = 1 WHERE user_id = ?",
                    (credentials.to_json(), user_id)
                )
                conn.commit()
            
            await update.message.reply_text("✅ Success! Google Calendar connected.", reply_markup=get_main_menu(user_id))
            return
        else:
            await update.message.reply_text("❌ Invalid code or connection failed. Try again.")
            return

    if user_text == "📅 Daily Brief":
        await show_daily_brief(update, context)
        return
    elif user_text == "➕ New Task":
        await update.message.reply_text("What should I schedule? (e.g., 'Meeting with Sarah tomorrow at 10am')")
        return
    elif user_text == "🧠 Memory/Context":
        await show_memory_context(update, context)
        return
    elif user_text == "🛠 Admin Panel":
        if user_id in bot_config.ALLOWED_USER_IDS:
            await update.message.reply_text("🛠 **Admin Control Center**", reply_markup=get_admin_menu())
        else:
            await update.message.reply_text("⛔️ Access Denied.")
        return
    elif user_text == "❓ Help":
        await show_advanced_help(update, context)
        return

    # 3. AI Intent Parsing & Response
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    # Save to history
    conv_manager.add_message(user_id, "user", user_text)

    lower_text = user_text.lower()
    
    # Check for "Add Event" intent
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
            # Store event details
            context.user_data['pending_event'] = event_details
            return
    
    if any(k in lower_text for k in ["schedule", "brief", "plan", "план"]):
        await show_daily_brief(update, context)
        return

    # Regular AI query with context
    ai_response = await query_ollama_with_context(user_id, user_text)
    conv_manager.add_message(user_id, "assistant", ai_response)
    await update.message.reply_text(ai_response, reply_markup=get_main_menu())
    
    # Trigger async digestion if history is long
    history = conv_manager.get_history(user_id)
    if len(history) >= 10 and len(history) % 10 == 0:
        asyncio.create_task(digest_chat_memory(user_id))

async def show_memory_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    memories = db.get_memories(user_id)
    
    if not memories:
        await update.effective_message.reply_text("🧠 I haven't learned any key facts about you yet. Let's talk more!")
    else:
        resp = "🧠 **My Long-term Memory:**\n\n"
        for m in memories:
            resp += f"• {m['fact_short']}\n"
        
        keyboard = [[InlineKeyboardButton("🗑 Clear Memory", callback_data="clear_memory")]]
        await update.effective_message.reply_text(resp, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def parse_event_details(text: str) -> Optional[Dict[str, Any]]:
    prompt = (
        "Extract event details from this text for a calendar: '" + text + "'. "
        "Current local time: " + datetime.now().isoformat() + ". "
        "Return ONLY a JSON object with keys: summary, time (ISO format), context (reason for event)."
    )
    
    response = await query_ollama(prompt, system="You are a data extractor. Return JSON only.")
    try:
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
        await update.effective_message.reply_text("❌ Calendar not connected. Please run /start to connect.")
        return
    
    events = client.get_upcoming_events(days=1)
    if not events:
        await update.effective_message.reply_text("You have no events scheduled for today. Ready for new tasks!")
    else:
        resp = "📅 **Your Daily Brief:**\n\n"
        for e in events:
            resp += f"• {client.format_event(e)}\n"
        await update.effective_message.reply_text(resp, parse_mode='Markdown')

async def digest_chat_memory(user_id: int):
    """Summarize recent history into long-term facts."""
    history = conv_manager.get_history(user_id, limit=20)
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])
    
    prompt = (
        "Analyze the following chat history and extract any NEW key facts "
        "or preferences about the user (e.g., job, interests, business details, names). "
        "Return results as a JSON array of objects with 'fact_short' and 'fact_full' keys. "
        "If no new facts found, return empty array [].\n\nHistory:\n" + history_text
    )
    
    response = await query_ollama(prompt, system="You are a knowledge extractor. Return JSON array ONLY.")
    try:
        start = response.find('[')
        end = response.rfind(']') + 1
        if start != -1 and end != -1:
            facts = json.loads(response[start:end])
            for f in facts:
                db.add_memory(user_id, f['fact_short'], f['fact_full'])
            logger.info(f"Digested {len(facts)} new memories for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to digest memory JSON: {e}")

async def query_ollama_with_context(user_id: int, prompt: str) -> str:
    # 1. Get Long-term memories
    memories = db.get_memories(user_id, limit=5)
    mem_text = "\n".join([f"- {m['fact_full']}" for m in memories])
    
    # 2. Get short-term history
    history = conv_manager.get_history(user_id, limit=5)
    hist_text = "\n".join([f"{m['role']}: {m['content']}" for m in history[-5:]])
    
    full_prompt = (
        "You are a helpful personal assistant. Here is what you know about the user:\n"
        + mem_text + "\n\nRecent context:\n" + hist_text + "\n\nUser: " + prompt + "\nAssistant:"
    )
    
    return await query_ollama(full_prompt)

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
