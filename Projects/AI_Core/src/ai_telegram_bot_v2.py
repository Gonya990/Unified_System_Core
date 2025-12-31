import logging
import os
import sys
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any

# Ensure we can import sibling modules irrespective of execution context
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.constants import ChatAction
from config_manager import ConfigManager
from inference_client import InferenceClient
from user_context_db import UserContextDB
from google_auth import GoogleAuthManager
from calendar_client import CalendarClient
from daily_scheduler import DailyScheduler
from conversation_manager import ConversationManager
from telegram_schema_expert import TelegramSchemaExpert

# Configuration
config = ConfigManager()

inference = InferenceClient(config)
db = UserContextDB()
auth_manager = GoogleAuthManager(client_secrets_file="client_secret.json")
conv_manager = ConversationManager()
tl_expert = TelegramSchemaExpert()


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
        ["📅 Обзор дня", "➕ Новая задача"],
        ["🧠 Память/Контекст", "❓ Помощь"]
    ]
    allowed_users_str = config.get("ALLOWED_USERS", "")
    allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
    if user_id in allowed_ids:
        keyboard.append(["🛠 Админ-панель"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Статус сервисов", callback_data="admin_services")],
        [InlineKeyboardButton("🔑 Управление ключами", callback_data="admin_keys")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("🔙 Назад", callback_data="show_help")]
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

    logger.info(f"[CMD] /start from {user.id} (@{user.username})")

    # 1. Register User & Update Interaction
    db.add_user(user.id, user.username, user.full_name)
    db.update_last_interaction(user.id)
    logger.info(f"[CMD] User {user.id} registered/updated in DB")

    # 2. Check Auth/Approval
    if not db.is_approved(user.id):
        # Auto-approve if in ALLOWED_USERS
        allowed_users_str = config.get("ALLOWED_USERS", "")
        logger.info(f"[CMD] ALLOWED_USERS config: '{allowed_users_str}'")
        allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
        logger.info(f"[CMD] Parsed allowed IDs: {allowed_ids}, checking user {user.id}")

        if user.id in allowed_ids:
            db.approve_user(user.id, True)
            logger.info(f"[CMD] Auto-approved user {user.id}")
        else:
            logger.warning(f"[CMD] User {user.id} not in ALLOWED_USERS, denying access")
            await update.message.reply_text(f"⛔️ Access Denied. Your ID `{user.id}` is pending approval.", parse_mode='Markdown')
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
        auth_url = auth_manager.get_auth_url(user_id=user_id)
        if auth_url:
            await query.edit_message_text(
                f"🔗 **Connect Google Calendar**\n\n"
                f"1. Click this link:\n{auth_url}\n\n"
                f"2. Authorize access to your calendar\n\n"
                f"3. You'll be redirected to a page (it may show an error - that's OK!)\n\n"
                f"4. Copy the `code=` value from the URL and paste it here.\n\n"
                f"Example: if URL is `http://localhost:8085/oauth2callback?code=4/0ABC...` "
                f"then paste: `4/0ABC...`",
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text("❌ Error: `client_secret.json` is missing on the server. Please contact Admin.")
    
    elif data == "help_onboarding":
        await show_advanced_help(query, context, edit=True)
    
    elif data.startswith("confirm_event_"):
        pending = context.user_data.get('pending_event')
        if not pending:
            await query.edit_message_text("❌ Событие не найдено или сессия истекла.")
            return
        
        client = get_calendar_client(user_id)
        if not client:
            await query.edit_message_text("❌ Календарь не подключен. Используйте /start.")
            return
        
        # Parse time
        try:
            start_time = datetime.fromisoformat(pending['time'].replace('Z', '+00:00'))
        except:
            start_time = datetime.now() + timedelta(hours=1) 
            
        # Conflict detection
        existing_events = client.get_upcoming_events(days=1)
        conflict = None
        for e in existing_events:
            e_start_str = e.get('start', {}).get('dateTime') or e.get('start', {}).get('date')
            if e_start_str:
                # Simplistic check
                if pending['time'] in e_start_str:
                    conflict = e['summary']
                    break
        
        if conflict:
            await query.edit_message_text(f"⚠️ **Конфликт!** В это время уже запланировано: `{conflict}`.\nВсё равно добавить?", parse_mode='Markdown', 
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Да, добавить", callback_data=f"force_confirm_event")], [InlineKeyboardButton("❌ Отмена", callback_data="cancel_event")]]))
            return

        await process_event_creation(query, user_id, client, pending, start_time)

    elif data == "force_confirm_event":
        pending = context.user_data.get('pending_event')
        client = get_calendar_client(user_id)
        start_time = datetime.fromisoformat(pending['time'].replace('Z', '+00:00'))
        await process_event_creation(query, user_id, client, pending, start_time)

    elif data == "cancel_event":
        context.user_data.pop('pending_event', None)
        await query.edit_message_text("❌ Создание события отменено.")
    
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
        await show_daily_brief(update, context)
    
    elif data == "show_memories_cb":
        # Simulate '🧠 Memory/Context' command
        await show_memory_context(update, context)
        
    elif data == "settings_cb":
        await query.edit_message_text("⚙️ **Settings**\n\nNotifications: ON\nProactive Nudge: ON (3 days)\nAI Model: " + config.get("MODEL_NAME", "unknown"), parse_mode='Markdown')

    # Admin Handlers
    elif data == "admin_services":
        allowed_users_str = config.get("ALLOWED_USERS", "")
        allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
        if user_id not in allowed_ids: return

        # Service status check
        import psutil
        try:
            # Check if AI inference is reachable
            ollama_up = "🟢" if await inference.health_check() else "🔴"

            # System metrics
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            status = (
                f"{ollama_up} AI Inference (Ollama)\n"
                f"🟢 Telegram Bot: Running\n"
                f"🟢 Scheduler: Active\n\n"
                f"📊 System:\n"
                f"  CPU: {cpu_percent:.1f}%\n"
                f"  RAM: {memory.percent:.1f}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)\n"
                f"  Disk: {disk.percent:.1f}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"
            )
        except Exception as e:
            status = f"🔴 Error checking status: {e}"

        await query.edit_message_text(f"🛠 **Service Status:**\n\n```\n{status}\n```", parse_mode='Markdown', reply_markup=get_admin_menu())

    elif data == "admin_keys":
        allowed_users_str = config.get("ALLOWED_USERS", "")
        allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
        if user_id not in allowed_ids: return
        
        status = config.get_status()
        resp = (
            "🔑 **Key Management**\n\n"
            f"Provider: `{config.get('INFERENCE_PROVIDER')}`\n"
            f"Model: `{config.get('MODEL_NAME')}`\n"
            f"API Key set: `{'✅' if status['api_key_set'] else '❌'}`\n\n"
            "To set a key, use: `/set_key [NAME] [VALUE]`\n"
            "Example: `/set_key OPENAI_API_KEY sk-...`"
        )
        await query.edit_message_text(resp, parse_mode='Markdown', reply_markup=get_admin_menu())

    elif data == "admin_users":
        allowed_users_str = config.get("ALLOWED_USERS", "")
        allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
        if user_id not in allowed_ids: return
        users = db.get_inactive_users(hours=0) # Get all users
        resp = "👥 **User Management:**\n\n"
        for u in users:
            status = "✅" if u['is_approved'] else "⏳"
            resp += f"{status} {u['full_name']} (@{u['username']}) - `{u['user_id']}`\n"
        await query.edit_message_text(resp, reply_markup=get_admin_menu())

async def process_event_creation(query, user_id, client, pending, start_time):
    success = client.create_event(
        summary=pending['summary'],
        start_time=start_time,
        description=pending.get('context', '')
    )
    
    if success:
        db.add_event_context(user_id, pending['summary'], pending.get('context', ''), start_time)
        await query.edit_message_text(f"✅ Запланировано: **{pending['summary']}**\nВремя: {pending['time']}", parse_mode='Markdown')
    else:
        await query.edit_message_text("❌ Не удалось создать событие в Google Calendar.")
    
    query.context.user_data.pop('pending_event', None)

async def show_advanced_help(update_or_query, context, edit=False):
    text = (
        "🤖 **Помощь цифрового ассистента**\n\n"
        "Я могу помочь вам с:\n"
        "• **Календарь**: Подключите Google аккаунт для управления встречами.\n"
        "• **Память**: Я запоминаю важные факты, чтобы лучше помогать.\n"
        "• **Контекст**: Спрашивайте 'Что мы решили по проекту X?', чтобы вспомнить детали.\n"
        "• **Проактивность**: Я напомню о себе, если мы давно не общались.\n\n"
        "**Быстрые действия:**"
    )
    keyboard = [
        [InlineKeyboardButton("📅 Обзор на сегодня", callback_data="daily_brief_cb")],
        [InlineKeyboardButton("🧠 Мои воспоминания", callback_data="show_memories_cb")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings_cb")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if edit:
        await update_or_query.edit_message_text(text, parse_mode='Markdown', reply_markup=reply_markup)
    else:
        await update_or_query.message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text if update.message else None
    username = update.effective_user.username if update.effective_user else "unknown"

    logger.info(f"[MESSAGE] Received from {user_id} (@{username}): {user_text}")

    if not db.is_approved(user_id):
        logger.warning(f"[MESSAGE] User {user_id} not approved, ignoring message")
        return

    db.update_last_interaction(user_id)
    logger.info(f"[MESSAGE] Processing message from approved user {user_id}")
    
    # Handle OAuth code - can start with "4/" or be a full URL
    auth_code = None
    if user_text.strip().startswith("4/"):
        auth_code = user_text.strip()
    elif "code=" in user_text:
        # Extract code from URL like http://localhost:8085/oauth2callback?code=4/0ABC...
        import re
        match = re.search(r'code=([^&\s]+)', user_text)
        if match:
            auth_code = match.group(1)

    if auth_code:
        await update.message.reply_text("🔄 Verifying code...")
        credentials = auth_manager.exchange_code(auth_code, user_id=user_id)
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

    if user_text == "📅 Обзор дня":
        await show_daily_brief(update, context)
        return
    elif user_text == "➕ Новая задача":
        await update.message.reply_text("Что мне запланировать? (например, 'Встреча с Сарой завтра в 10 утра')")
        return
    elif user_text == "🧠 Память/Контекст":
        await show_memory_context(update, context)
        return
    elif user_text == "🛠 Админ-панель":
        allowed_users_str = config.get("ALLOWED_USERS", "")
        allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
        if user_id in allowed_ids:
            await update.message.reply_text("🛠 **Центр управления админа**", reply_markup=get_admin_menu())
        else:
            await update.message.reply_text("⛔️ Доступ запрещен.")
        return
    elif user_text == "❓ Помощь":
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
    await update.message.reply_text(ai_response, reply_markup=get_main_menu(user_id))
    
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
        # Get stored contexts
        import sqlite3
        with sqlite3.connect("user_context.db") as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT event_title, context_description FROM event_contexts WHERE user_id = ?", (user_id,))
            contexts = {row['event_title']: row['context_description'] for row in cursor.fetchall()}

        resp = "📅 **Your Daily Brief:**\n\n"
        for e in events:
            title = e.get('summary', 'Untitled')
            time_formatted = client.format_event(e)
            ctx = contexts.get(title)
            
            resp += f"• {time_formatted}"
            if ctx:
                resp += f"\n  💡 *Context:* {ctx}"
            resp += "\n"
            
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
    logger.info(f"[AI] Querying AI for user {user_id}, prompt length: {len(prompt)}")

    # 1. Get Long-term memories
    memories = db.get_memories(user_id, limit=5)
    mem_text = "\n".join([f"- {m['fact_full']}" for m in memories])
    logger.debug(f"[AI] Found {len(memories)} memories for user {user_id}")

    # 2. Get short-term history
    history = conv_manager.get_context_messages(user_id, limit=10)
    logger.debug(f"[AI] Got {len(history)} history messages for user {user_id}")

    system_prompt = (
        "You are a helpful personal assistant. Here is what you know about the user:\n"
        + mem_text + "\n\n"
        "You also have access to the Telegram MTProto TL Schema. If the user asks technical questions "
        "about Telegram types or methods, you can provide expert details. Suggest using the `/tl` command "
        "for raw technical documentation. Provide short, helpful and professional answers."
    )


    try:
        response_text, _ = await inference.chat(history + [{"role": "user", "content": prompt}], system_prompt=system_prompt)
        logger.info(f"[AI] Got response for user {user_id}, length: {len(response_text)}")
        return response_text
    except Exception as e:
        logger.error(f"[AI] Error querying AI for user {user_id}: {e}")
        raise

async def query_ollama(prompt: str, system: str = None) -> str:
    """Legacy wrapper, now uses InferenceClient."""
    system_prompt = system or "You are a helpful assistant."
    response, _ = await inference.chat([{"role": "user", "content": prompt}], system_prompt=system_prompt)
    return response

async def post_init(application: Application) -> None:
    # Register bot commands in Telegram menu
    commands = [
        BotCommand("start", "Start the bot / Main menu"),
        BotCommand("help", "Show help and available commands"),
        BotCommand("brief", "Get your daily calendar brief"),
        BotCommand("memory", "View your saved memories"),
        BotCommand("newtask", "Create a new task or event"),
        BotCommand("tl", "Lookup Telegram TL Schema (MTProto)"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands registered.")

    scheduler = DailyScheduler(application, db, inference=inference)
    asyncio.create_task(scheduler.start())
    logger.info("DailyScheduler background task started via post_init.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    logger.info(f"[CMD] /help from {update.effective_user.id}")
    await show_advanced_help(update, context)

async def brief_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /brief command."""
    user_id = update.effective_user.id
    logger.info(f"[CMD] /brief from {user_id}")
    if not db.is_approved(user_id):
        logger.warning(f"[CMD] /brief denied - user {user_id} not approved")
        await update.message.reply_text("⛔️ Access denied.")
        return
    db.update_last_interaction(user_id)
    await show_daily_brief(update, context)

async def memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /memory command."""
    user_id = update.effective_user.id
    logger.info(f"[CMD] /memory from {user_id}")
    if not db.is_approved(user_id):
        logger.warning(f"[CMD] /memory denied - user {user_id} not approved")
        await update.message.reply_text("⛔️ Access denied.")
        return
    db.update_last_interaction(user_id)
    await show_memory_context(update, context)

async def newtask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /newtask command."""
    user_id = update.effective_user.id
    logger.info(f"[CMD] /newtask from {user_id}")
    if not db.is_approved(user_id):
        logger.warning(f"[CMD] /newtask denied - user {user_id} not approved")
        await update.message.reply_text("⛔️ Access denied.")
        return
    db.update_last_interaction(user_id)
    await update.message.reply_text(
        "📝 What would you like to schedule?\n\n"
        "Example: 'Meeting with Sara tomorrow at 10am'"
    )

async def set_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    allowed_users_str = config.get("ALLOWED_USERS", "")
    allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
    if user_id not in allowed_ids: return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: `/set_key NAME VALUE`", parse_mode='Markdown')
        return

    key_name = context.args[0].upper()
    key_value = context.args[1]
    
    config.set(key_name, key_value)
    
    try:
        await update.message.delete()
    except:
        pass

    await update.message.reply_text(f"✅ Key `{key_name}` updated and encrypted.", parse_mode='Markdown')

async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    allowed_users_str = config.get("ALLOWED_USERS", "")
    allowed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
    if user_id not in allowed_ids: return

    if not context.args:
        await update.message.reply_text("Usage: `/approve USER_ID`")
        return

    try:
        target_id = int(context.args[0])
        db.approve_user(target_id, True)
        await update.message.reply_text(f"✅ User {target_id} approved.")
        await context.bot.send_message(chat_id=target_id, text="🚀 Your access has been approved! Send /start to begin.")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

async def tl_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tl [query] command."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id): return
    
    if not context.args:
        await update.message.reply_text("Usage: `/tl [predicate|id|type]`\nExample: `/tl user` or `/tl 34280482`", parse_mode='Markdown')
        return
        
    query = " ".join(context.args)
    result = tl_expert.lookup(query)
    await update.message.reply_text(result, parse_mode='Markdown')

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"[ERROR] Exception while handling an update: {context.error}")
    import traceback
    tb_str = ''.join(traceback.format_exception(None, context.error, context.error.__traceback__))
    logger.error(f"[ERROR] Traceback:\n{tb_str}")

    # Try to notify the user
    if update and hasattr(update, 'effective_chat') and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ An error occurred while processing your request. Please try again."
            )
        except Exception as e:
            logger.error(f"[ERROR] Failed to send error message to user: {e}")

def main():
    token = config.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("[STARTUP] TELEGRAM_BOT_TOKEN not set!")
        print("Error: TELEGRAM_BOT_TOKEN not set!")
        return

    logger.info("[STARTUP] Building application...")
    application = Application.builder().token(token).post_init(post_init).build()

    # Register error handler
    application.add_error_handler(error_handler)
    logger.info("[STARTUP] Error handler registered")

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('brief', brief_command))
    application.add_handler(CommandHandler('memory', memory_command))
    application.add_handler(CommandHandler('newtask', newtask_command))
    application.add_handler(CommandHandler('tl', tl_command))
    application.add_handler(CommandHandler('set_key', set_key))
    application.add_handler(CommandHandler('approve', approve_user))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("[STARTUP] All handlers registered")

    logger.info("[STARTUP] Starting polling...")
    print(f'Bot V2 (AI_Core) is running...')
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
