import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timedelta
from typing import Any, Optional

import aiohttp
from agent_orchestrator import PIPELINES, AgentOrchestrator
from calendar_client import CalendarClient
from config_manager import ConfigManager
from conversation_manager import ConversationManager
from daily_scheduler import DailyScheduler
from google_auth import GoogleAuthManager
from inference_client import InferenceClient
from telegram import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
)
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from telegram_schema_expert import TelegramSchemaExpert

# Setup logger
logger = logging.getLogger(__name__)

# Ensure we can import sibling modules irrespective of execution context
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Try Firestore first, fallback to SQLite
try:
    from firestore_db import FirestoreDB

    _USE_FIRESTORE = True
except ImportError:
    from user_context_db import UserContextDB

    _USE_FIRESTORE = False

# Optional imports with fallbacks
try:
    from ha_controller import HAController

    ha_controller = HAController()
except ImportError:
    ha_controller = None

try:
    from web_search import WebSearch

    web_search = WebSearch()
except ImportError:
    web_search = None

try:
    from infrastructure import InfrastructureManager

    infra_manager = InfrastructureManager()
except ImportError:
    infra_manager = None

try:
    from gmail_client import GmailClient

    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False

try:
    from notion_client import NotionClient

    notion_client = NotionClient()
except ImportError:
    notion_client = None

try:
    from linear_client import LinearClient

    linear_client = LinearClient()
except ImportError:
    linear_client = None

try:
    from health_integration import HealthIntegration

    health_integration = HealthIntegration()
except ImportError:
    health_integration = None

try:
    from usage_tracker import UsageTracker

    usage_tracker = UsageTracker()
except ImportError:
    usage_tracker = None

try:
    from task_manager import TaskManager

    task_manager = TaskManager()
except ImportError:
    task_manager = None

try:
    from notify_manager import NotifyManager

    notify_manager = NotifyManager()
except ImportError:
    notify_manager = None

try:
    from digest_service import DigestService

    _DIGEST_AVAILABLE = True
except ImportError:
    _DIGEST_AVAILABLE = False
    digest_service = None

# MCP Agent Mail Integration
try:
    agent_mail_path = os.path.join(current_dir, "Scripts", "Orchestration")
    if agent_mail_path not in sys.path:
        sys.path.append(agent_mail_path)
    from agent_mail_client import AgentMailClient

    agent_mail = AgentMailClient()
    logger.info("AgentMailClient initialized")
except Exception as e:
    agent_mail = None
    logger.warning(f"AgentMailClient not available: {e}")

# Setup logging first
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot_journal.log",
    filemode="a",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger("").addHandler(console)

logger = logging.getLogger(__name__)

# Configuration
config = ConfigManager()

inference = InferenceClient(config)

# Initialize database (Firestore or SQLite fallback)
if _USE_FIRESTORE:
    db = FirestoreDB()
    logger.info("Using Firestore database")
else:
    db_path = config.get("SQLITE_DB_PATH", "user_context.db")
    db = UserContextDB(db_path=db_path)
    logger.info(f"Using SQLite database (local mode): {db_path}")

auth_manager = GoogleAuthManager(
    client_secrets_file=os.path.join("config", "gmail_credentials.json")
)
conv_manager = ConversationManager()
tl_expert = TelegramSchemaExpert()
agent_orchestrator = AgentOrchestrator(inference)

# Initialize digest service (requires other services)
if _DIGEST_AVAILABLE and usage_tracker and task_manager:
    digest_service = DigestService(
        usage_tracker, task_manager, linear_client, infra_manager
    )
    logger.info("Digest service initialized")
else:
    digest_service = None

# Admin access configuration
allowed_users_str = config.get("ALLOWED_USERS", "708531393,5569219290,578363419")
logger.info(f"Raw ALLOWED_USERS from config: '{allowed_users_str}'")
try:
    # Hardcoded admins + env var users
    DEFAULT_ADMINS = [708531393, 5569219290, 578363419]
    parsed_ids = [int(i.strip()) for i in allowed_users_str.split(",") if i.strip()]
    ALLOWED_IDS = list(set(DEFAULT_ADMINS + parsed_ids))
    logger.info(f"Final Global ALLOWED_IDS: {ALLOWED_IDS}")
except Exception as e:
    logger.error(f"Failed to parse ALLOWED_USERS: {e}")
    ALLOWED_IDS = [708531393, 5569219290, 578363419]

# User aliases for messaging (name -> Telegram user ID)
USER_ALIASES = {
    "костя": 578363419,
    "kostya": 578363419,
    "kosta": 578363419,
    "коста": 578363419,
    "nibbler": 578363419,
    "nibbler420": 578363419,
    "toxicfi7h": 578363419,
    "igor": 708531393,
    "игорь": 708531393,
    "игорьку": 708531393,
    "игорю": 708531393,
    "игорек": 708531393,
    "igoreha9": 708531393,
    "игореха": 708531393,
    "игореха9": 708531393,
    "admin": 708531393,
}

ADMIN_ID = 708531393  # Primary admin for notifications


# keyboards
def get_main_menu(user_id: int):
    keyboard = [
        ["📅 Обзор дня", "➕ Новая задача"],
        ["🧠 Память/Контекст", "⚙️ Настройки", "❓ Помощь"],
    ]
    if user_id in ALLOWED_IDS:
        keyboard.append(["🛠 Админ-панель"])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_admin_menu():
    keyboard = [
        [InlineKeyboardButton("📊 Статус сервисов", callback_data="admin_services")],
        [InlineKeyboardButton("🔑 Управление ключами", callback_data="admin_keys")],
        [InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton("⏳ Заявки на доступ", callback_data="admin_pending")],
        [InlineKeyboardButton("🔙 Назад", callback_data="show_help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_settings_menu():
    """Settings menu with model/provider options."""
    current_provider = config.get("INFERENCE_PROVIDER", "ollama")
    current_model = config.get("MODEL_NAME", "unknown")
    keyboard = [
        [
            InlineKeyboardButton(
                f"🤖 Модель: {current_model}", callback_data="settings_model"
            )
        ],
        [
            InlineKeyboardButton(
                f"🔌 Провайдер: {current_provider.upper()}",
                callback_data="settings_provider",
            )
        ],
        [InlineKeyboardButton("📊 Статистика", callback_data="settings_usage")],
        [InlineKeyboardButton("🔙 Назад", callback_data="show_help")],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_calendar_client(user_id: int) -> Optional[CalendarClient]:
    user_data = db.get_user(user_id)
    if user_data and user_data["is_google_connected"] and user_data["google_creds"]:
        try:
            creds_dict = json.loads(user_data["google_creds"])
            return CalendarClient(credentials_dict=creds_dict)
        except Exception as e:
            logger.error(f"Failed to create CalendarClient for {user_id}: {e}")
    return None


def get_gmail_client(user_id: int) -> Optional[GmailClient]:
    """Get Gmail client for user using their OAuth credentials from Firestore."""
    if not GMAIL_AVAILABLE:
        return None
    user_data = db.get_user(user_id)
    if user_data and user_data["is_google_connected"] and user_data["google_creds"]:
        try:
            creds_dict = json.loads(user_data["google_creds"])
            return GmailClient(credentials_dict=creds_dict)
        except Exception as e:
            logger.error(f"Failed to create GmailClient for {user_id}: {e}")
    return None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    logger.info(f"[CMD] /start from {user.id} (@{user.username})")

    # 1. Register User & Update Interaction
    db.add_user(user.id, user.username, user.full_name)
    db.update_last_interaction(user.id)
    logger.info(f"[CMD] User {user.id} registered/updated in DB")

    # 2. Check Auth/Approval
    if not db.is_approved(user.id):
        # Auto-approve if in ALLOWED_IDS
        logger.info(
            f"[CMD] Checking if user {user.id} is in global ALLOWED_IDS: {ALLOWED_IDS}"
        )

        if user.id in ALLOWED_IDS:
            db.approve_user(user.id, True)
            logger.info(f"[CMD] Auto-approved user {user.id}")
        else:
            logger.warning(f"[CMD] User {user.id} not in ALLOWED_IDS, denying access")
            await update.message.reply_text(
                f"⛔️ **Доступ ограничен**\n\n"
                f"Ваш ID: `{user.id}`\n"
                f"Заявка отправлена администратору.\n\n"
                f"Ожидайте одобрения.",
                parse_mode="Markdown",
            )
            # Notify admin about new user request with approve button
            try:
                keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "✅ Одобрить", callback_data=f"approve_user:{user.id}"
                            ),
                            InlineKeyboardButton(
                                "❌ Отклонить", callback_data=f"deny_user:{user.id}"
                            ),
                        ]
                    ]
                )
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=(
                        f"🆕 **Новая заявка на доступ**\n\n"
                        f"👤 {user.full_name}\n"
                        f"📱 @{user.username or 'нет username'}\n"
                        f"🆔 `{user.id}`"
                    ),
                    parse_mode="Markdown",
                    reply_markup=keyboard,
                )
                logger.info(
                    f"[CMD] Sent approval request to admin {ADMIN_ID} for user {user.id}"
                )
            except Exception as e:
                logger.error(f"[CMD] Failed to notify admin about new user: {e}")
            return

    # 3. Check Google Connection
    user_data = db.get_user(user.id)
    if not user_data or not user_data["is_google_connected"]:
        # Show Connect Button
        keyboard = [
            [
                InlineKeyboardButton(
                    "🔗 Connect Google Calendar", callback_data="connect_google"
                )
            ],
            [InlineKeyboardButton("❓ Help", callback_data="help_onboarding")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_html(
            rf"Welcome, {user.mention_html()}! 🚀"
            "\n\nTo assist you properly, I need access to your Calendar.",
            reply_markup=reply_markup,
        )
    else:
        # Show Main Menu
        await update.message.reply_html(
            rf"Welcome back, {user.mention_html()}! Ready to assist.",
            reply_markup=get_main_menu(user.id),
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge

    data = query.data
    user_id = update.effective_user.id
    db.update_last_interaction(user_id)

    if data == "connect_google":
        auth_url = auth_manager.get_auth_url(user_id=user_id)
        if auth_url:
            # Use HTML parse mode to avoid Markdown breaking URLs with underscores
            await query.edit_message_text(
                f"🔗 <b>Connect Google Calendar</b>\n\n"
                f"1. Click this link:\n{auth_url}\n\n"
                f"2. Authorize access to your calendar\n\n"
                "3. You'll be redirected to a page (it may show error - that's OK!)\n\n"
                "4. Copy the <code>code=</code> value from URL and paste it here.\n\n"
                f"Example: if URL is <code>http://localhost/...?code=4/0ABC...</code> "
                f"then paste: <code>4/0ABC...</code>",
                parse_mode="HTML",
            )
        else:
            await query.edit_message_text(
                "❌ Error: `client_secret.json` is missing on the server. Please contact Admin."
            )

    elif data == "help_onboarding":
        await show_advanced_help(query, context, edit=True)

    elif data.startswith("confirm_event_"):
        pending = context.user_data.get("pending_event")
        if not pending:
            await query.edit_message_text("❌ Событие не найдено или сессия истекла.")
            return

        client = get_calendar_client(user_id)
        if not client:
            await query.edit_message_text(
                "❌ Календарь не подключен. Используйте /start."
            )
            return

        # Parse time
        try:
            start_time = datetime.fromisoformat(pending["time"].replace("Z", "+00:00"))
        except (ValueError, TypeError) as e:
            logger.warning(
                f"Failed to parse event time '{pending.get('time')}': {e}, using default"
            )
            start_time = datetime.now() + timedelta(hours=1)

        # Conflict detection
        existing_events = client.get_upcoming_events(days=1)
        conflict = None
        for e in existing_events:
            e_start_str = e.get("start", {}).get("dateTime") or e.get("start", {}).get(
                "date"
            )
            if e_start_str:
                # Simplistic check
                if pending["time"] in e_start_str:
                    conflict = e["summary"]
                    break

        if conflict:
            await query.edit_message_text(
                f"⚠️ **Конфликт!** В это время уже запланировано: `{conflict}`.\nВсё равно добавить?",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "✅ Да, добавить", callback_data="force_confirm_event"
                            )
                        ],
                        [
                            InlineKeyboardButton(
                                "❌ Отмена", callback_data="cancel_event"
                            )
                        ],
                    ]
                ),
            )
            return

        await process_event_creation(
            query, user_id, client, pending, start_time, context
        )

    elif data == "force_confirm_event":
        pending = context.user_data.get("pending_event")
        client = get_calendar_client(user_id)
        start_time = datetime.fromisoformat(pending["time"].replace("Z", "+00:00"))
        await process_event_creation(
            query, user_id, client, pending, start_time, context
        )

    elif data == "cancel_event":
        context.user_data.pop("pending_event", None)
        await query.edit_message_text("❌ Создание события отменено.")

    elif data == "edit_context":
        await query.edit_message_text(
            "Feature coming soon! For now, try adding the event again with more details."
        )

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
        current_provider = config.get("INFERENCE_PROVIDER", "ollama")
        current_model = config.get("MODEL_NAME", "unknown")
        await query.edit_message_text(
            f"⚙️ **Настройки AI**\n\n"
            f"🤖 Модель: `{current_model}`\n"
            f"🔌 Провайдер: `{current_provider.upper()}`\n\n"
            f"Выберите опцию для изменения:",
            parse_mode="Markdown",
            reply_markup=get_settings_menu(),
        )

    elif data == "settings_model":
        # Show model selection
        await query.edit_message_text("🔍 Загружаю список моделей...")
        models = await inference.list_models()
        if not models:
            await query.edit_message_text(
                "❌ Не удалось загрузить модели. Проверьте подключение к провайдеру.",
                reply_markup=get_settings_menu(),
            )
            return
        current_model = inference.model
        buttons = []
        for model in models[:15]:  # Limit to 15 models
            indicator = "✅" if model == current_model else "🔄"
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{indicator} {model}", callback_data=f"model:{model}"
                    )
                ]
            )
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="settings_cb")])
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            f"🤖 **Выбор модели**\n\n"
            f"Текущая: `{current_model}`\n"
            f"Провайдер: `{config.get('INFERENCE_PROVIDER', 'ollama').upper()}`\n\n"
            f"Нажмите для переключения:",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    elif data == "settings_provider":
        # Show provider selection
        providers = ["ollama", "openai", "gemini", "openrouter", "council"]
        current = config.get("INFERENCE_PROVIDER", "ollama")
        buttons = []
        provider_info = {
            "ollama": "🦙 Локальный (бесплатно)",
            "openai": "🧠 OpenAI GPT-4o",
            "gemini": "💎 Google Gemini",
            "openrouter": "🌐 Claude/GPT через OpenRouter",
            "council": "👥 Совет всех AI (ансамбль)",
        }
        for provider in providers:
            indicator = "✅" if provider == current else "🔄"
            info = provider_info.get(provider, provider)
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{indicator} {info}", callback_data=f"provider:{provider}"
                    )
                ]
            )
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="settings_cb")])
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            f"🔌 **Выбор провайдера**\n\nТекущий: `{current.upper()}`\n\nНажмите для переключения:",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    elif data == "settings_usage":
        # Show usage stats
        if usage_tracker:
            stats = usage_tracker.get_user_stats(user_id, days=30)
            if stats:
                msg = (
                    f"📊 **Статистика (30 дней)**\n\n"
                    f"📈 Токенов: `{stats.get('total_tokens', 0):,}`\n"
                    f"📝 Запросов: `{stats.get('requests', 0)}`\n"
                )
            else:
                msg = "📊 Нет данных об использовании."
        else:
            msg = "📊 Трекер использования не настроен."
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔙 Назад", callback_data="settings_cb")]]
        )
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=keyboard)

    # Admin Handlers
    elif data == "admin_services":
        if user_id not in ALLOWED_IDS:
            return

        # Service status check
        import psutil

        try:
            # Check if AI inference is reachable
            ollama_up = "🟢" if await inference.health_check() else "🔴"

            # System metrics
            cpu_percent = psutil.cpu_percent(interval=0.5)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            status = (
                f"{ollama_up} AI Inference (Ollama)\n"
                f"🟢 Telegram Bot: Running\n"
                f"🟢 Scheduler: Active\n\n"
                f"📊 System:\n"
                f"  CPU: {cpu_percent:.1f}%\n"
                f"  RAM: {memory.percent:.1f}% "
                f"({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)\n"
                f"  Disk: {disk.percent:.1f}% "
                f"({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)"
            )
        except Exception as e:
            status = f"🔴 Error checking status: {e}"

        await query.edit_message_text(
            f"🛠 **Service Status:**\n\n```\n{status}\n```",
            parse_mode="Markdown",
            reply_markup=get_admin_menu(),
        )

    elif data == "admin_keys":
        if user_id not in ALLOWED_IDS:
            return

        status = config.get_status()
        resp = (
            "🔑 **Key Management**\n\n"
            f"Provider: `{config.get('INFERENCE_PROVIDER')}`\n"
            f"Model: `{config.get('MODEL_NAME')}`\n"
            f"API Key set: `{'✅' if status['api_key_set'] else '❌'}`\n\n"
            "To set a key, use: `/set_key [NAME] [VALUE]`\n"
            "Example: `/set_key OPENAI_API_KEY sk-...`"
        )
        await query.edit_message_text(
            resp, parse_mode="Markdown", reply_markup=get_admin_menu()
        )

    elif data == "admin_users":
        if user_id not in ALLOWED_IDS:
            return
        users = db.get_inactive_users(hours=0)  # Get all users
        resp = "👥 **User Management:**\n\n"
        for u in users:
            status = "✅" if u["is_approved"] else "⏳"
            resp += f"{status} {u['full_name']} (@{u['username']}) - `{u['user_id']}`\n"
        await query.edit_message_text(resp, reply_markup=get_admin_menu())

    elif data == "admin_pending":
        # Show pending approval requests with inline buttons
        if user_id not in ALLOWED_IDS:
            return

        users = db.get_inactive_users(hours=0)  # Get all users
        pending_users = [u for u in users if not u["is_approved"]]

        if not pending_users:
            await query.edit_message_text(
                "✅ **Нет ожидающих заявок**\n\nВсе пользователи одобрены.",
                parse_mode="Markdown",
                reply_markup=get_admin_menu(),
            )
            return

        resp = f"⏳ **Заявки на доступ ({len(pending_users)}):**\n\n"
        buttons = []
        for u in pending_users[:10]:  # Limit to 10
            resp += (
                f"👤 {u['full_name']} (@{u['username']})\n   ID: `{u['user_id']}`\n\n"
            )
            buttons.append(
                [
                    InlineKeyboardButton(
                        f"✅ Одобрить {u['full_name']}",
                        callback_data=f"approve_user:{u['user_id']}",
                    ),
                    InlineKeyboardButton(
                        "❌", callback_data=f"deny_user:{u['user_id']}"
                    ),
                ]
            )
        buttons.append([InlineKeyboardButton("🔙 Назад", callback_data="show_admin")])
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(
            resp, parse_mode="Markdown", reply_markup=keyboard
        )

    elif data.startswith("approve_user:"):
        # Approve user via inline button
        if user_id not in ALLOWED_IDS:
            return

        target_id = int(data.split(":")[1])
        db.approve_user(target_id, True)
        logger.info(
            f"[ADMIN] User {user_id} approved user {target_id} via inline button"
        )

        # Notify the approved user
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    "🎉 **Доступ одобрен!**\n\n"
                    "Ваша заявка была одобрена администратором.\n\n"
                    "Отправьте /start чтобы начать."
                ),
                parse_mode="Markdown",
            )
        except Exception as e:
            logger.warning(f"Could not notify user {target_id}: {e}")

        await query.edit_message_text(
            f"✅ Пользователь `{target_id}` одобрен!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 К заявкам", callback_data="admin_pending")]]
            ),
        )

    elif data.startswith("deny_user:"):
        # Deny user access
        if user_id not in ALLOWED_IDS:
            return

        target_id = int(data.split(":")[1])
        logger.info(f"[ADMIN] User {user_id} denied user {target_id}")

        # Notify the denied user
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text="❌ Ваша заявка на доступ была отклонена.",
            )
        except Exception as e:
            logger.warning(f"Could not notify user {target_id}: {e}")

        await query.edit_message_text(
            f"❌ Пользователь `{target_id}` отклонён.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔙 К заявкам", callback_data="admin_pending")]]
            ),
        )

    elif data == "show_admin":
        if user_id not in ALLOWED_IDS:
            return
        await query.edit_message_text(
            "🛠 **Центр управления админа**",
            parse_mode="Markdown",
            reply_markup=get_admin_menu(),
        )

    # Model selection callback
    elif data.startswith("model:"):
        model_name = data.split(":", 1)[1]
        config.set("MODEL_NAME", model_name)
        inference.model = model_name
        logger.info(f"[CALLBACK] User {user_id} switched model to: {model_name}")
        await query.edit_message_text(
            f"✅ Модель изменена на: `{model_name}`", parse_mode="Markdown"
        )

    # Provider selection callback
    elif data.startswith("provider:"):
        provider_name = data.split(":", 1)[1]
        config.set("INFERENCE_PROVIDER", provider_name)
        inference.provider = provider_name
        logger.info(f"[CALLBACK] User {user_id} switched provider to: {provider_name}")
        await query.edit_message_text(
            f"✅ Провайдер изменён на: `{provider_name.upper()}`",
            parse_mode="Markdown",
        )


async def process_event_creation(query, user_id, client, pending, start_time, context):
    success = client.create_event(
        summary=pending["summary"],
        start_time=start_time,
        description=pending.get("context", ""),
    )

    if success:
        db.add_event_context(
            user_id, pending["summary"], pending.get("context", ""), start_time
        )
        await query.edit_message_text(
            f"✅ Запланировано: **{pending['summary']}**\nВремя: {pending['time']}",
            parse_mode="Markdown",
        )
    else:
        await query.edit_message_text("❌ Не удалось создать событие в Google Calendar.")

    context.user_data.pop("pending_event", None)


async def show_advanced_help(update_or_query, context, edit=False):
    text = (
        "🤖 **Помощь цифрового ассистента**\n\n"
        "Я могу помочь вам с:\n"
        "• **Календарь**: Подключите Google аккаунт для управления встречами.\n"
        "• **Память**: Я запоминаю важные факты, чтобы лучше помогать.\n"
        "• **Контекст**: Спрашивайте 'Что мы решили по проекту X?', "
        "чтобы вспомнить детали.\n"
        "• **Проактивность**: Я напомню о себе, если мы давно не общались.\n\n"
        "**Быстрые действия:**"
    )
    keyboard = [
        [InlineKeyboardButton("📅 Обзор на сегодня", callback_data="daily_brief_cb")],
        [InlineKeyboardButton("🧠 Мои воспоминания", callback_data="show_memories_cb")],
        [InlineKeyboardButton("⚙️ Настройки", callback_data="settings_cb")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if edit:
        await update_or_query.edit_message_text(
            text, parse_mode="Markdown", reply_markup=reply_markup
        )
    else:
        await update_or_query.message.reply_text(
            text, parse_mode="Markdown", reply_markup=reply_markup
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text if update.message else None
    username = update.effective_user.username if update.effective_user else "unknown"

    logger.info(f"[MESSAGE] Received from {user_id} (@{username}): {user_text}")

    if not db.is_approved(user_id):
        # Auto-approve if matches global allowed list
        if user_id in ALLOWED_IDS:
            db.approve_user(user_id, True)
            logger.info(
                f"[MESSAGE] Auto-approved user {user_id} via global ALLOWED_IDS"
            )
        else:
            logger.warning(f"[MESSAGE] User {user_id} not approved, ignoring message")
            return

    # If message starts with / but is actually a Russian text (user mistake),
    # treat as text
    if user_text.startswith("/") and len(user_text) > 1:
        # Check if it's one of our registered commands
        registered_cmds = [
            "start",
            "help",
            "status",
            "models",
            "scan",
            "imagine",
            "search",
            "todo",
            "ha",
            "clear",
            "mail",
            "calendar",
            "brief",
            "settings",
            "memory",
            "beads",
            "agent",
        ]
        first_word = user_text[1:].split()[0].lower()
        if first_word not in registered_cmds:
            # It's a text request starting with /
            logger.info(f"[MESSAGE] Treating slash-text as regular input: {user_text}")
            # We proceed to process it as text
        else:
            # It's a real command, ignore here if it's handled by CommandHandler
            # But actually MessageHandler(TEXT) usually doesn't catch commands anyway
            pass

    db.update_last_interaction(user_id)
    logger.info(f"[MESSAGE] Processing message from approved user {user_id}")

    # Handle OAuth code - can start with "4/" or be a full URL
    auth_code = None
    if user_text.strip().startswith("4/"):
        auth_code = user_text.strip()
    elif "code=" in user_text:
        # Extract code from URL like http://localhost:8085/oauth2callback?code=4/0ABC...
        import re

        match = re.search(r"code=([^&\s]+)", user_text)
        if match:
            auth_code = match.group(1)

    if auth_code:
        await update.message.reply_text("🔄 Verifying code...")
        credentials = auth_manager.exchange_code(auth_code, user_id=user_id)
        if credentials:
            # Use Firestore/SQLite abstraction
            if hasattr(db, "use_firestore") and db.use_firestore:
                db.db.collection("users").document(str(user_id)).update(
                    {"google_creds": credentials.to_json(), "is_google_connected": True}
                )
            else:
                import sqlite3

                with sqlite3.connect("user_context.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE users SET google_creds = ?, is_google_connected = 1 WHERE user_id = ?",
                        (credentials.to_json(), user_id),
                    )
                    conn.commit()

            await update.message.reply_text(
                "✅ Success! Google Calendar connected.",
                reply_markup=get_main_menu(user_id),
            )
            return
        else:
            await update.message.reply_text(
                "❌ Invalid code or connection failed. Try again."
            )
            return

    if user_text == "📅 Обзор дня":
        await show_daily_brief(update, context)
        return
    elif user_text == "➕ Новая задача":
        await update.message.reply_text(
            "Что мне запланировать? (например, 'Встреча с Сарой завтра в 10 утра')"
        )
        return
    elif user_text == "🧠 Память/Контекст":
        await show_memory_context(update, context)
        return
    elif user_text == "🛠 Админ-панель":
        if user_id in ALLOWED_IDS:
            await update.message.reply_text(
                "🛠 **Центр управления админа**", reply_markup=get_admin_menu()
            )
        else:
            await update.message.reply_text("⛔️ Доступ запрещен.")
        return
    elif user_text == "❓ Помощь":
        await show_advanced_help(update, context)
        return

    # 3. AI Intent Parsing & Response
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    # Save to history
    conv_manager.add_message(user_id, "user", user_text)

    lower_text = user_text.lower()

    # Multilingual intent keywords (English / Russian / Hebrew)
    EVENT_KEYWORDS = [
        # English
        "schedule",
        "add",
        "meeting",
        "appointment",
        "reminder",
        "event",
        "book",
        # Russian
        "запиши",
        "встреча",
        "назначь",
        "добавь",
        "напомни",
        "событие",
        "запланируй",
        # Hebrew
        "תזכיר",
        "פגישה",
        "הוסף",
        "קבע",
        "תזמן",
        "אירוע",
        "הזכר",
    ]

    # Exclude messaging keywords from event detection to prevent hijacking
    MSG_START_KEYWORDS = [
        "tell",
        "say",
        "send",
        "скажи",
        "передай",
        "отправь",
        "сообщи",
        "напиши",
    ]

    # Check for "Add Event" intent
    if any(k in lower_text for k in EVENT_KEYWORDS) and not any(
        m in lower_text for m in MSG_START_KEYWORDS
    ):
        event_details = await parse_event_details(user_text)
        if event_details and "summary" in event_details:
            summary = event_details["summary"]
            time_str = event_details.get("time", "Unknown")
            context_desc = event_details.get("context", "No context provided")

            keyboard = [
                [
                    InlineKeyboardButton(
                        "✅ Confirm", callback_data=f"confirm_event_{summary[:20]}"
                    )
                ],
                [InlineKeyboardButton("✏️ Edit Context", callback_data="edit_context")],
                [InlineKeyboardButton("❌ Cancel", callback_data="cancel_event")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"📅 **Found Event:**\n"
                f"📝 Title: {summary}\n"
                f"⏰ Time: {time_str}\n"
                f"💡 Context: {context_desc}\n\n"
                "Should I add this to your calendar?",
                parse_mode="Markdown",
                reply_markup=reply_markup,
            )
            # Store event details
            context.user_data["pending_event"] = event_details
            return

    # Multilingual brief/schedule keywords
    BRIEF_KEYWORDS = [
        "schedule",
        "brief",
        "plan",
        "today",
        "agenda",  # English
        "план",
        "расписание",
        "сегодня",
        "повестка",  # Russian
        "לוח",
        "היום",
        "תוכנית",
        "סדר יום",  # Hebrew
    ]
    if any(k in lower_text for k in BRIEF_KEYWORDS):
        await show_daily_brief(update, context)
        return

    # 4. Image Generation Intent
    IMAGE_KEYWORDS = [
        "создай картинку",
        "нарисуй",
        "сгенерируй изображение",
        "картинка",
        "draw",
        "generate image",
        "imagine",
    ]
    if any(k in lower_text for k in IMAGE_KEYWORDS):
        # Extract prompt: remove the keyword
        img_prompt = user_text
        for kw in IMAGE_KEYWORDS:
            if kw in lower_text:
                # Use regex to replace case-insensitively
                import re

                img_prompt = re.sub(
                    re.escape(kw), "", img_prompt, flags=re.IGNORECASE
                ).strip()
                break

        if img_prompt:
            # Delegate to img_command logic (simulated)
            # We can just call img_command if we wrap it or copy logic
            # For simplicity, let's call img_command by creating a dummy context
            # or just call its logic
            logger.info(f"Natural language image trigger: {img_prompt}")
            # Redirect to img_command by manually setting context.args
            context.args = img_prompt.split()
            await img_command(update, context)
            return

    # Email keywords - fetch emails automatically
    EMAIL_KEYWORDS = [
        "mail",
        "email",
        "inbox",
        "письма",
        "почта",
        "почту",
        "почте",
        "входящие",
        "письмо",
        "מייל",
        "דואר",
        "הודעות",
        "вакансий",
        "вакансии",
        "vacancy",
        "vacancies",
        "резюме",
    ]
    if any(k in lower_text for k in EMAIL_KEYWORDS) and GMAIL_AVAILABLE:
        logger.info(f"Email keywords detected in: {lower_text}")
        gmail = get_gmail_client(user_id)
        if gmail and gmail.is_valid():
            await context.bot.send_chat_action(
                chat_id=update.effective_chat.id, action=ChatAction.TYPING
            )

            # Detect vacancy-related queries
            VACANCY_KEYWORDS = [
                "вакансий",
                "вакансии",
                "вакансия",
                "vacancy",
                "vacancies",
                "job",
                "работа",
                "работу",
                "предложения",
                "резюме",
            ]
            is_vacancy_query = any(v in lower_text for v in VACANCY_KEYWORDS)

            # Extract count if mentioned (e.g., "30 писем")
            import re

            count_match = re.search(r"(\d+)", lower_text)
            requested_count = int(count_match.group(1)) if count_match else 10
            max_count = min(requested_count, 50)  # Cap at 50 for context window safety

            is_analysis_requested = any(
                a in lower_text
                for a in [
                    "анализ",
                    "проанализируй",
                    "analyze",
                    "summarize",
                    "обзор",
                    "проверь",
                ]
            )

            if is_vacancy_query:
                # Search for job-related emails
                query = "(vacancy OR job OR вакансия OR предложение OR recruiter OR HR OR hh.ru OR LinkedIn OR hiring)"
                logger.info(
                    f"Searching vacancies with query: {query}, limit: {max_count}"
                )
                emails = gmail.search_emails(query, max_results=max_count)
                if emails:
                    msg = (
                        f"💼 **Найдено {len(emails)} писем о вакансиях** "
                        f"(показаны последние {min(len(emails), 30)}):\n\n"
                    )
                    # Show only top 30 to avoid hitting limits
                    for i, email in enumerate(emails[:30], 1):
                        sender = (
                            email["from"].split("<")[0].strip().strip('"')
                            if "<" in email["from"]
                            else email["from"]
                        )
                        subj = email["subject"][:60]
                        if len(email["subject"]) > 60:
                            subj += "..."
                        msg += f"{i}. **{sender}**\n   {subj}\n\n"

                    msg += "_Анализирую содержимое для подбора лучших..._"
                    await update.message.reply_text(
                        msg, parse_mode="Markdown", reply_markup=get_main_menu(user_id)
                    )

                    # Store emails in context specifically for AI to analyze
                    email_context = "EMAILS_SNAPSHOT (Top 20 most recent):\n"
                    # Limit to top 20 and truncate content to fit context window
                    for email in emails[:20]:
                        snippet = (email.get("snippet", "") or "")[:300].replace(
                            "\n", " "
                        )
                        email_context += (
                            f"- ID: {email['id']}\n  From: {email['from']}\n  "
                            f"Subject: {email['subject']}\n  Summary: {snippet}\n\n"
                        )

                    conv_manager.add_message(
                        user_id, "user", f"[SYSTEM DATA]\n{email_context}"
                    )

                    # Trigger analysis
                    analysis_prompt = (
                        "Проанализируй эти письма (выше) и выбери "
                        "5-7 самых подходящих вакансий для меня. "
                        "Моё резюме должно быть у тебя в памяти "
                        "(если нет - просто ищи руководящие/технические позиции). "
                        "Формат ответа:\n"
                        "1. **Название/Тема** (Отправитель)\n"
                        "   Почему подходит: ...\n"
                    )

                    try:
                        ai_response = await query_ollama_with_context(
                            user_id, analysis_prompt
                        )
                        if ai_response and ai_response.strip():
                            conv_manager.add_message(user_id, "assistant", ai_response)
                            await update.message.reply_text(
                                ai_response,
                                reply_markup=get_main_menu(user_id),
                                parse_mode="Markdown",
                            )
                        else:
                            await update.message.reply_text(
                                "🤔 Я изучил письма, но затрудняюсь выделить "
                                "конкретные вакансии. Попробуйте уточнить "
                                "критерии поиска.",
                                reply_markup=get_main_menu(user_id),
                            )
                    except Exception as e:
                        logger.error(f"AI Analysis failed: {e}")
                        await update.message.reply_text(
                            "❌ Произошла ошибка при анализе писем. "
                            "Попробуйте уменьшить выборку (`/mail search query`).",
                            reply_markup=get_main_menu(user_id),
                        )
                else:
                    await update.message.reply_text(
                        "📭 Писем о вакансиях не найдено.",
                        reply_markup=get_main_menu(user_id),
                    )
                return

            elif is_analysis_requested:
                await context.bot.send_chat_action(
                    chat_id=update.effective_chat.id, action=ChatAction.TYPING
                )
                emails = gmail.get_recent_emails(max_results=max_count)
                if not emails:
                    await update.message.reply_text(
                        "📭 Входящих писем не найдено.",
                        reply_markup=get_main_menu(user_id),
                    )
                    return

                await update.message.reply_text(
                    f"🔍 Загрузил последние {len(emails)} писем. "
                    "Анализирую на предмет критических уведомлений и предупреждений...",
                    reply_markup=get_main_menu(user_id),
                )

                email_context = "ПОСЛЕДНИЕ ПИСЬМА (ДЛЯ АНАЛИЗА):\n"
                for i, email in enumerate(emails, 1):
                    sender = (
                        email["from"].split("<")[0].strip().strip('"')
                        if "<" in email["from"]
                        else email["from"]
                    )
                    snippet = (email.get("snippet", "") or "")[:200].replace("\n", " ")
                    email_context += f"{i}. От: {sender} | Тема: {email['subject']} | Суть: {snippet}\n"

                full_analysis_prompt = (
                    f"Проанализируй следующий список из {len(emails)} писем.\n"
                    f"Контекст запроса пользователя: '{user_text}'\n"
                    "ИНСТРУКЦИИ:\n"
                    "1. Игнорируй предложения о работе/вакансии "
                    "(если пользователь так просил).\n"
                    "2. Выдели КРИТИЧЕСКИЕ предупреждения, счета, "
                    "уведомления безопасности или важные личные сообщения.\n"
                    "3. Сгруппируй по важности.\n"
                    "4. Отвечай кратко и по делу на языке пользователя.\n\n"
                    f"{email_context}"
                )

                try:
                    ai_response = await query_ollama_with_context(
                        user_id, full_analysis_prompt
                    )
                    if ai_response and ai_response.strip():
                        conv_manager.add_message(user_id, "assistant", ai_response)
                        await update.message.reply_text(
                            ai_response,
                            reply_markup=get_main_menu(user_id),
                            parse_mode="Markdown",
                        )
                    else:
                        await update.message.reply_text(
                            "🤔 Я просмотрел письма, но ничего критичного не обнаружил.",
                            reply_markup=get_main_menu(user_id),
                        )
                except Exception as e:
                    logger.error(f"Deep analysis failed: {e}")
                    await update.message.reply_text(
                        "❌ Ошибка при глубоком анализе почты.",
                        reply_markup=get_main_menu(user_id),
                    )
                return

            # Check if user wants to search
            if any(
                w in lower_text for w in ["найди", "поиск", "search", "find", "ищи"]
            ):
                # Extract search query (words after search keyword)
                for kw in ["найди", "поиск", "search", "find", "ищи"]:
                    if kw in lower_text:
                        query = lower_text.split(kw, 1)[-1].strip()
                        if query:
                            emails = gmail.search_emails(query, max_results=10)
                            if emails:
                                msg = f"🔍 **Найдено по '{query}':**\n\n"
                                for email in emails:
                                    sender = (
                                        email["from"].split("<")[0].strip().strip('"')
                                        if "<" in email["from"]
                                        else email["from"]
                                    )
                                    msg += (
                                        f"• **{sender}**\n  {email['subject'][:50]}\n\n"
                                    )
                                await update.message.reply_text(
                                    msg,
                                    parse_mode="Markdown",
                                    reply_markup=get_main_menu(user_id),
                                )
                            else:
                                await update.message.reply_text(
                                    f"📭 По запросу '{query}' ничего не найдено.",
                                    reply_markup=get_main_menu(user_id),
                                )
                            return

            # Default: show email summary
            summary = gmail.get_email_summary()
            await update.message.reply_text(
                summary, parse_mode="Markdown", reply_markup=get_main_menu(user_id)
            )
            return
        else:
            await update.message.reply_text(
                "📧 Gmail не подключен. Используйте /start → 🔗 Connect Google",
                reply_markup=get_main_menu(user_id),
            )
            return

    # Regular AI query with context
    ai_response = await query_ollama_with_context(user_id, user_text)

    # Validate response is not empty
    if not ai_response or not ai_response.strip():
        ai_response = "🤔 Не удалось получить ответ от AI. Попробуйте ещё раз или смените провайдер через /settings."

    # --- PROCESSS AI COMMANDS ([[TAG:args]]) ---
    import re

    # 1. ALICE TTS
    alice_matches = re.findall(r"\[\[ALICE:(.*?)\]\]", ai_response)
    for text_to_say in alice_matches:
        if ha_controller:
            await ha_controller.speak_via_yandex(text_to_say)
            logger.info(f"[HA] Alice spoke: {text_to_say}")
        ai_response = ai_response.replace(
            f"[[ALICE:{text_to_say}]]", f"🔊 _(Озвучено Алисой: {text_to_say})_"
        )

    # 2. HA LIGHTS
    ha_matches = re.findall(r"\[\[HA:(.*?):(.*?)\]\]", ai_response)
    for action, entity_name in ha_matches:
        if ha_controller:
            if action == "light_on":
                await ha_controller.turn_on_light(entity_name)
                ai_response = ai_response.replace(
                    f"[[HA:{action}:{entity_name}]]", f"💡 _(Включаю: {entity_name})_"
                )
            elif action == "light_off":
                await ha_controller.turn_off_light(entity_name)
                ai_response = ai_response.replace(
                    f"[[HA:{action}:{entity_name}]]", f"🌑 _(Выключаю: {entity_name})_"
                )
        else:
            ai_response = ai_response.replace(
                f"[[HA:{action}:{entity_name}]]", "❌ _(HA недоступен)_"
            )

    # 3. DIRECT MESSAGING (Telegram)
    msg_matches = re.findall(r"\[\[RUN:MSG:(.*?):(.*?)\]\]", ai_response)
    for target_name, msg_text in msg_matches:
        target_id = None

        # Resolve target
        target_clean = target_name.strip().lower().lstrip("@")
        if target_clean.isdigit():
            target_id = int(target_clean)
        elif target_clean in USER_ALIASES:
            target_id = USER_ALIASES[target_clean]
        else:
            # Fallback scan DB for username
            try:
                # get_inactive_users(hours=0) should return all users if DB isn't empty
                all_users = db.get_inactive_users(hours=0)
                for u in all_users:
                    if u.get("username", "").lower() == target_clean:
                        target_id = u["user_id"]
                        break
            except Exception as db_err:
                logger.error(f"[MSG] DB resolution error: {db_err}")

        if target_id:
            try:
                # Get sender info
                sender_name = (
                    update.effective_user.username or update.effective_user.first_name
                )
                await context.bot.send_message(
                    chat_id=target_id,
                    text=f"📩 **Сообщение от @{sender_name} (через Гоню):**\n\n{msg_text}",
                    parse_mode="Markdown",
                )
                ai_response = ai_response.replace(
                    f"[[RUN:MSG:{target_name}:{msg_text}]]",
                    f"✅ _(Отправлено {target_name})_",
                )
                logger.info(f"[MSG] AI forwarded message from {user_id} to {target_id}")
            except Exception as e:
                ai_response = ai_response.replace(
                    f"[[RUN:MSG:{target_name}:{msg_text}]]",
                    f"❌ _(Ошибка отправки пользователю {target_name}: {e})_",
                )
                logger.error(f"[MSG] AI failed to forward message to {target_id}: {e}")
        else:
            ai_response = ai_response.replace(
                f"[[RUN:MSG:{target_name}:{msg_text}]]",
                f"❌ _(Пользователь {target_name} не найден)_",
            )
            logger.warning(f"[MSG] Could not resolve target: {target_name}")

    conv_manager.add_message(user_id, "assistant", ai_response)
    await update.message.reply_text(
        ai_response, reply_markup=get_main_menu(user_id), parse_mode="Markdown"
    )

    # Trigger async digestion if history is long
    history = conv_manager.get_history(user_id)
    if len(history) >= 10 and len(history) % 10 == 0:
        asyncio.create_task(digest_chat_memory(user_id))


async def show_memory_context(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    memories = db.get_memories(user_id)

    if not memories:
        await update.effective_message.reply_text(
            "🧠 I haven't learned any key facts about you yet. Let's talk more!"
        )
    else:
        resp = "🧠 **My Long-term Memory:**\n\n"
        for m in memories:
            resp += f"• {m['fact_short']}\n"

        keyboard = [
            [InlineKeyboardButton("🗑 Clear Memory", callback_data="clear_memory")]
        ]
        await update.effective_message.reply_text(
            resp, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard)
        )


async def parse_event_details(text: str) -> Optional[dict[str, Any]]:
    prompt = (
        "Extract event details from this text for a calendar: '" + text + "'. "
        "Current local time: " + datetime.now().isoformat() + ". "
        "Return ONLY a JSON object with keys: summary, time (ISO format), "
        "context (reason for event)."
    )

    response = await query_ollama(
        prompt, system="You are a data extractor. Return JSON only."
    )
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        if start != -1 and end != -1:
            return json.loads(response[start:end])
    except Exception as e:
        logger.error(f"Failed to parse event JSON: {e} | Response: {response}")
    return None


async def show_daily_brief(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    client = get_calendar_client(user_id)

    if not client:
        await update.effective_message.reply_text(
            "❌ Календарь не подключен. Используйте /start."
        )
        return

    events = client.get_upcoming_events(days=1)
    if not events:
        await update.effective_message.reply_text(
            "🗓 Совсем нет планов на сегодня! Можно заняться новыми делами."
        )
    else:
        # Get stored contexts using db abstraction
        contexts = db.get_event_contexts(user_id)

        resp = "📅 **Your Daily Brief:**\n\n"
        for e in events:
            title = e.get("summary", "Untitled")
            time_formatted = client.format_event(e)
            ctx = contexts.get(title)

            resp += f"• {time_formatted}"
            if ctx:
                resp += f"\n  💡 *Context:* {ctx}"
            resp += "\n"

        await update.effective_message.reply_text(resp, parse_mode="Markdown")


async def digest_chat_memory(user_id: int):
    """Summarize recent history into long-term facts."""
    history = conv_manager.get_history(user_id, limit=20)
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in history])

    prompt = (
        "Analyze the following chat history and extract any NEW key facts "
        "or preferences about the user (e.g., job, interests, "
        "business details, names). "
        "Return results as a JSON array of objects with 'fact_short' and "
        "'fact_full' keys. "
        "If no new facts found, return empty array [].\n\nHistory:\n" + history_text
    )

    response = await query_ollama(
        prompt, system="You are a knowledge extractor. Return JSON array ONLY."
    )
    try:
        start = response.find("[")
        end = response.rfind("]") + 1
        if start != -1 and end != -1:
            facts = json.loads(response[start:end])
            for f in facts:
                db.add_memory(user_id, f["fact_short"], f["fact_full"])
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
        "You are Gonya, a powerful multilingual personal AI assistant. "
        "You fluently understand and respond in English, Russian (русский), "
        "and Hebrew (עברית). "
        "IMPORTANT: Always respond in the SAME LANGUAGE the user wrote to you.\n\n"
        "=== YOUR CAPABILITIES ===\n"
        "You have REAL access to the user's data and can perform actions:\n\n"
        "📧 EMAIL (Gmail):\n"
        "- Read emails: /mail or /mail list [count]\n"
        "- Search: /mail search <query>\n"
        "- Send: /mail send email | subject | body\n"
        "- Archive/Delete: /mail archive/trash <id>\n"
        "When user asks about emails, tell them to use /mail commands or "
        "offer to explain how.\n\n"
        "📅 CALENDAR (Google):\n"
        "- View events: /calendar or /brief\n"
        "- Create events: user can say 'добавь встречу на 15:00 название'\n"
        "- You can parse natural language requests for calendar events.\n\n"
        "🏠 HOME ASSISTANT & ALICE:\n"
        "- Control smart home: You can output COMMANDS to control devices.\n"
        "  Format: [[HA:light_on:name]] or [[HA:light_off:name]]\n"
        "- Yandex Alice TTS: If user asks to SAY something via Alice/station.\n"
        "  Format: [[ALICE:text_to_say]]\n\n"
        "📩 MESSAGING (RELAY SYSTEM):\n"
        "You serve as a relay between users. If User A asks to tell/send/message "
        "User B, you MUST NOT respond to User A as if you are talking to User B. "
        "You MUST use the relay tag.\n"
        "- Relay tag format: [[RUN:MSG:<target>:<text>]]\n"
        "- Valid targets: 'kostya', 'igor', or numeric ID.\n"
        "RULES:\n"
        "1. NEVER output plain text intended for the target directly in the chat "
        "with the sender.\n"
        "2. ALWAYS wrap the relayed message in the [[RUN:MSG:...]] tag.\n"
        "3. Example of WRONG response: 'Игорь, нам нужно встретиться...'\n"
        "4. Example of CORRECT response: 'Хорошо, передаю Игорю. "
        "[[RUN:MSG:igor:Игорь, нам нужно встретиться...]]'\n\n"
        "🔍 OTHER TOOLS:\n"
        "- Web search: /search <query>\n"
        "- Image generation: /img <prompt>\n"
        "- AI agents: /agent <name> <task>\n"
        "- System status: /status\n"
        "- Memory/context: /memory\n\n"
        "=== USER CONTEXT ===\n" + mem_text + "\n\n"
        "Known Aliases:\n"
        "- Kostya (Nibbler420): target='kostya'\n"
        "- Igor (Owner): target='igor'\n\n"
        "=== INSTRUCTIONS ===\n"
        "1. Be proactive - if user asks to tell/send something to Kostya, use "
        "[[RUN:MSG:kostya:text]].\n"
        "2. Remember: timezone is Asia/Jerusalem (IST).\n"
        "3. Give short, helpful answers in user's language.\n"
        "4. If you can help with a task directly, do it or explain how."
    )

    try:
        response_text, _ = await inference.chat(
            history + [{"role": "user", "content": prompt}], system_prompt=system_prompt
        )
        logger.info(
            f"[AI] Got response for user {user_id}, length: {len(response_text)}"
        )
        return response_text
    except Exception as e:
        logger.error(f"[AI] Error querying AI for user {user_id}: {e}")
        raise


async def query_ollama(prompt: str, system: str = None) -> str:
    """Legacy wrapper, now uses InferenceClient."""
    system_prompt = system or "You are a helpful assistant."
    response, _ = await inference.chat(
        [{"role": "user", "content": prompt}], system_prompt=system_prompt
    )
    return response


async def post_init(application: Application) -> None:
    # Register bot commands in Telegram menu
    commands = [
        BotCommand("start", "Start the bot / Main menu"),
        BotCommand("help", "Show help and available commands"),
        BotCommand("settings", "AI model & provider settings"),
        BotCommand("models", "List and switch AI models"),
        BotCommand("setprovider", "Switch AI provider"),
        BotCommand("beads", "Git-native task tracking"),
        BotCommand("agent", "Run AI agent (code-explorer, reviewer...)"),
        BotCommand("pipeline", "Run agent pipeline (feature, bugfix...)"),
        BotCommand("brief", "Get your daily calendar brief"),
        BotCommand("img", "Generate image with DALL-E 3"),
        BotCommand("memory", "View your saved memories"),
        BotCommand("msg", "Message another user"),
    ]
    await application.bot.set_my_commands(commands)
    logger.info("Bot commands registered.")

    scheduler = DailyScheduler(application, db, inference=inference)
    asyncio.create_task(scheduler.start())
    logger.info("DailyScheduler background task started via post_init.")

    # Broadcast Online Status via MCP Mail
    if agent_mail:
        try:
            # Run in executor to avoid blocking async loop with sync requests
            loop = asyncio.get_running_loop()
            if await loop.run_in_executor(None, agent_mail.health_check):
                await loop.run_in_executor(
                    None,
                    lambda: agent_mail.broadcast(
                        subject="Unified Bot Online",
                        body_md="The AI Telegram Bot V2 has successfully started and is listening for commands.",
                        importance="normal",
                    ),
                )
                logger.info("Broadcasted 'Unified Bot Online' via MCP Mail")
            else:
                logger.warning("MCP Mail Server unhealthy, skipping broadcast")
        except Exception as e:
            logger.error(f"Failed to broadcast online status: {e}")


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
        "📝 What would you like to schedule?\n\nExample: 'Meeting with Sara tomorrow at 10am'"
    )


async def set_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_IDS:
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: `/set_key NAME VALUE`", parse_mode="Markdown"
        )
        return

    key_name = context.args[0].upper()
    key_value = context.args[1]

    config.set(key_name, key_value)

    try:
        await update.message.delete()
    except Exception as e:
        logger.debug(f"Could not delete message: {e}")

    await update.message.reply_text(
        f"✅ Key `{key_name}` updated and encrypted.", parse_mode="Markdown"
    )


async def approve_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ALLOWED_IDS:
        return

    if not context.args:
        await update.message.reply_text("Usage: `/approve USER_ID`")
        return

    try:
        target_id = int(context.args[0])
        db.approve_user(target_id, True)
        await update.message.reply_text(f"✅ User {target_id} approved.")
        await context.bot.send_message(
            chat_id=target_id,
            text="🚀 Your access has been approved! Send /start to begin.",
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def tl_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /tl [query] command."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: `/tl [predicate|id|type]`\nExample: `/tl user` or `/tl 34280482`",
            parse_mode="Markdown",
        )
        return

    query = " ".join(context.args)
    result = tl_expert.lookup(query)
    await update.message.reply_text(result, parse_mode="Markdown")


async def agent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /agent [name] [task] command - run specialized AI agent."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    db.update_last_interaction(user_id)

    if not context.args:
        # Show available agents
        agents_help = (
            "🤖 **AI Агенты**\n\n"
            "Использование: `/agent <имя> <задача>`\n\n"
            "**Discovery:**\n"
            "• `code-explorer` - исследовать код\n"
            "• `api-discoverer` - найти API endpoints\n"
            "• `dependency-mapper` - карта зависимостей\n\n"
            "**Architecture:**\n"
            "• `code-architect` - спроектировать решение\n"
            "• `performance-optimizer` - оптимизация\n\n"
            "**Implementation:**\n"
            "• `implementer` - реализовать фичу\n"
            "• `bug-fixer` - исправить баг\n\n"
            "**Review:**\n"
            "• `code-reviewer` - ревью кода\n\n"
            "**Примеры:**\n"
            "`/agent code-explorer Найди паттерны аутентификации`\n"
            "`/agent code-reviewer Проверь последние изменения`"
        )
        await update.message.reply_text(agents_help, parse_mode="Markdown")
        return

    agent_name = context.args[0]
    task = " ".join(context.args[1:]) if len(context.args) > 1 else ""

    if not task:
        await update.message.reply_text(
            f"❌ Укажите задачу для агента `{agent_name}`\n\nПример: `/agent {agent_name} Опиши архитектуру проекта`",
            parse_mode="Markdown",
        )
        return

    # Check if agent exists
    agent = agent_orchestrator.get_agent(agent_name)
    if not agent:
        available = ", ".join(list(agent_orchestrator.agents.keys())[:10])
        await update.message.reply_text(
            f"❌ Агент `{agent_name}` не найден.\n\nДоступные: `{available}...`\n\nИспользуйте `/agent` для списка.",
            parse_mode="Markdown",
        )
        return

    logger.info(f"[AGENT] User {user_id} running {agent_name}: {task[:50]}...")

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    await update.message.reply_text(
        f"🤖 Запускаю агента `{agent_name}`...\n⏱ Это может занять 20-40 секунд.",
        parse_mode="Markdown",
    )

    try:
        result = await agent_orchestrator.run(agent_name, task)

        # Split long messages
        if len(result) > 4000:
            chunks = [result[i : i + 4000] for i in range(0, len(result), 4000)]
            for i, chunk in enumerate(chunks):
                await update.message.reply_text(
                    f"📄 Часть {i + 1}/{len(chunks)}:\n\n{chunk}", parse_mode="Markdown"
                )
        else:
            await update.message.reply_text(
                f"✅ **{agent_name}** завершил:\n\n{result}", parse_mode="Markdown"
            )

        logger.info(f"[AGENT] {agent_name} completed for user {user_id}")

    except Exception as e:
        logger.error(f"[AGENT] Error running {agent_name}: {e}")
        await update.message.reply_text(f"❌ Ошибка агента: {str(e)}")


async def pipeline_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pipeline [type] [task] command - run agent pipeline."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    db.update_last_interaction(user_id)

    if not context.args:
        pipelines_help = (
            "🔄 **Пайплайны агентов**\n\n"
            "Использование: `/pipeline <тип> <задача>`\n\n"
            "**Доступные пайплайны:**\n"
            "• `feature` - разработка фичи\n"
            "  (explorer → architect → implementer → reviewer)\n\n"
            "• `bugfix` - исправление бага\n"
            "  (explorer → bug-fixer → reviewer)\n\n"
            "• `refactor` - рефакторинг\n"
            "  (explorer → architect → implementer → reviewer)\n\n"
            "• `security` - проверка безопасности\n"
            "  (explorer → security-worker → reviewer)\n\n"
            "**Пример:**\n"
            "`/pipeline feature Добавить кэширование в API`\n"
            "`/pipeline bugfix Ошибка в парсинге дат`"
        )
        await update.message.reply_text(pipelines_help, parse_mode="Markdown")
        return

    pipeline_type = context.args[0].lower()
    task = " ".join(context.args[1:]) if len(context.args) > 1 else ""

    if pipeline_type not in PIPELINES:
        available = ", ".join(PIPELINES.keys())
        await update.message.reply_text(
            f"❌ Пайплайн `{pipeline_type}` не найден.\n\nДоступные: `{available}`",
            parse_mode="Markdown",
        )
        return

    if not task:
        await update.message.reply_text(
            f"❌ Укажите задачу для пайплайна `{pipeline_type}`\n\nПример: `/pipeline {pipeline_type} Описание задачи`",
            parse_mode="Markdown",
        )
        return

    logger.info(f"[PIPELINE] User {user_id} running {pipeline_type}: {task[:50]}...")

    pipeline_stages = PIPELINES[pipeline_type]
    stage_names = " → ".join([s[0] for s in pipeline_stages])

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    await update.message.reply_text(
        f"🔄 Запускаю пайплайн `{pipeline_type}`\n\nЭтапы: {stage_names}\n\n⏱ Это может занять 2-5 минут...",
        parse_mode="Markdown",
    )

    try:
        # Prepare tasks with the user's task description
        tasks = [(agent, f"{desc}: {task}") for agent, desc in pipeline_stages]

        results = await agent_orchestrator.run_pipeline(tasks)

        # Format results
        response = f"✅ **Пайплайн `{pipeline_type}` завершён**\n\n"

        for agent_name, result in results.items():
            # Truncate each result for readability
            short_result = result[:800] + "..." if len(result) > 800 else result
            response += f"**{agent_name}:**\n{short_result}\n\n---\n\n"

        # Split if too long
        if len(response) > 4000:
            chunks = [response[i : i + 4000] for i in range(0, len(response), 4000)]
            for i, chunk in enumerate(chunks):
                await update.message.reply_text(
                    f"📄 Часть {i + 1}/{len(chunks)}:\n\n{chunk}", parse_mode="Markdown"
                )
        else:
            await update.message.reply_text(response, parse_mode="Markdown")

        logger.info(f"[PIPELINE] {pipeline_type} completed for user {user_id}")

    except Exception as e:
        logger.error(f"[PIPELINE] Error running {pipeline_type}: {e}")
        await update.message.reply_text(f"❌ Ошибка пайплайна: {str(e)}")


async def img_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /img [prompt] command - generate image using DALL-E 3."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    db.update_last_interaction(user_id)

    if not context.args:
        await update.message.reply_text(
            "🎨 **Генерация изображений (DALL-E 3)**\n\n"
            "Использование: `/img <описание>`\n\n"
            "Примеры:\n"
            "• `/img Новогодняя открытка 2026 со снежинками`\n"
            "• `/img Футуристический город на закате`\n"
            "• `/img Милый котик в шапке Санты`",
            parse_mode="Markdown",
        )
        return

    prompt = " ".join(context.args)
    logger.info(f"[IMG] User {user_id} requested image: {prompt[:50]}...")

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_PHOTO
    )
    await update.message.reply_text(
        "🎨 Генерирую изображение... (это может занять до 30 секунд)"
    )

    try:
        image_url = await inference.generate_image(prompt)

        if image_url:
            # Download and send as photo
            async with aiohttp.ClientSession() as session:
                async with session.get(image_url) as resp:
                    if resp.status == 200:
                        image_data = await resp.read()
                        from io import BytesIO

                        await update.message.reply_photo(
                            photo=BytesIO(image_data), caption=f"🎨 {prompt[:200]}"
                        )
                        logger.info(f"[IMG] Successfully sent image to user {user_id}")
                    else:
                        await update.message.reply_text(
                            f"❌ Не удалось загрузить изображение. URL: {image_url}"
                        )
        else:
            await update.message.reply_text(
                "❌ Не удалось сгенерировать изображение.\n\n"
                "Возможные причины:\n"
                "• Не установлен OPENAI_API_KEY\n"
                "• Превышен лимит API\n"
                "• Промпт нарушает правила контента"
            )
    except Exception as e:
        logger.error(f"[IMG] Error generating image: {e}")
        await update.message.reply_text(f"❌ Ошибка: {str(e)}")


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command - show system status."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    msg = await update.message.reply_text("🔍 Проверяю системы...")

    import time

    import psutil

    try:
        cpu_usage = psutil.cpu_percent()
        mem = psutil.virtual_memory()
        uptime = time.time() - psutil.boot_time()

        def format_uptime(seconds):
            days, remainder = divmod(seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, _ = divmod(remainder, 60)
            return f"{int(days)}d {int(hours)}h {int(minutes)}m"

        uptime_str = format_uptime(uptime)

        # AI Health
        inf_status = "✅ OK" if await inference.health_check() else "❌ Error"

        # HA Health
        ha_status = "❓ Not configured"
        if ha_controller:
            try:
                ha_res = await ha_controller.get_status()
                if ha_res and ha_res.get("status") == "ok":
                    ha_status = "✅ Online"
                else:
                    ha_status = "❌ Error"
            except Exception as e:
                logger.debug(f"HA status check failed: {e}")
                ha_status = "❌ Unreachable"

        dashboard = (
            f"📊 **System Status**\n\n"
            f"🖥 **Server**\n"
            f"• CPU: `{cpu_usage}%`\n"
            f"• RAM: `{mem.percent}%` ({mem.used // 1024 // 1024}MB / "
            f"{mem.total // 1024 // 1024}MB)\n"
            f"• Uptime: `{uptime_str}`\n\n"
            f"🧠 **AI Core**\n"
            f"• Provider: `{inference.provider}`\n"
            f"• Model: `{inference.model}`\n"
            f"• Status: {inf_status}\n\n"
            f"🏠 **Home Assistant**\n"
            f"• Status: {ha_status}\n\n"
            f"🕒 Time: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`"
        )

        await msg.edit_text(dashboard, parse_mode="Markdown")

    except Exception as e:
        await msg.edit_text(f"❌ Error: {e}")


async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /search command - web search."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not web_search:
        await update.message.reply_text("❌ Web search not configured.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /search <query>\nExample: /search latest AI news"
        )
        return

    query = " ".join(context.args)
    await update.message.reply_text(f'🔍 Searching: "{query[:50]}..."\n⏳ Please wait...')

    try:
        result = await web_search.search(query)
        if result:
            await update.message.reply_text(result, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ No results found.")
    except Exception as e:
        await update.message.reply_text(f"❌ Search error: {e}")


async def ha_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ha command - Home Assistant control."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not ha_controller:
        await update.message.reply_text("❌ Home Assistant not configured.")
        return

    if not context.args:
        await update.message.reply_text(
            "🏠 **Home Assistant Commands:**\n\n"
            "/ha status - статус\n"
            "/ha sensors - датчики\n"
            "/ha lights on/off - свет\n"
            "/ha script <name> - скрипт\n"
            "/ha scene <name> - сцена",
            parse_mode="Markdown",
        )
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
            await ha_controller.turn_on_light("all")
            await update.message.reply_text("💡 Turning ON lights")
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


async def models_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /models command - list available models."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    await update.message.reply_text("🔍 Fetching available models...")

    models = await inference.list_models()

    if not models:
        await update.message.reply_text(
            "❌ Could not fetch models. Check endpoint configuration."
        )
        return

    current_model = inference.model

    buttons = []
    for model in models[:20]:
        indicator = "✅" if model == current_model else "🔄"
        buttons.append(
            [
                InlineKeyboardButton(
                    f"{indicator} {model}", callback_data=f"model:{model}"
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        f"📋 **Available Models** ({len(models)})\n\nCurrent: `{current_model}`\n\nClick to switch:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command - clear conversation history."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    conv_manager.clear_history(user_id)
    await update.message.reply_text(
        "🧹 История диалога очищена!\n\nСледующее сообщение начнёт новый контекст."
    )


async def infra_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /infra command - infrastructure status."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not infra_manager:
        await update.message.reply_text("❌ Infrastructure manager not configured.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    report = await infra_manager.check_nodes()
    await update.message.reply_text(report, parse_mode="Markdown")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming photos - analyze with AI."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        return

    photo = update.message.photo[-1]
    prompt = update.message.caption or (
        "Что изображено на этой картинке? Опиши подробно."
    )

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    await update.message.reply_text("👀 Analyzing photo...")

    try:
        import tempfile

        file = await photo.get_file()
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            temp_path = f.name

        await file.download_to_drive(temp_path)
        response = await inference.analyze_image(temp_path, prompt)

        os.remove(temp_path)
        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Photo handling failed: {e}")
        await update.message.reply_text(f"❌ Error analyzing photo: {e}")


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming voice messages - transcribe and process."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )
    await update.message.reply_text("🎤 Transcribing...")

    try:
        import tempfile

        voice_file = await update.message.voice.get_file()
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
            temp_path = f.name

        await voice_file.download_to_drive(temp_path)
        transcript = await inference.transcribe_audio(temp_path)

        os.remove(temp_path)

        if not transcript or "[Error" in transcript:
            await update.message.reply_text(f"❌ Could not transcribe: {transcript}")
            return

        await update.message.reply_text(
            f'🗣 Transcribed: "_{transcript}_"', parse_mode="Markdown"
        )

        # Process as text
        ai_response = await query_ollama_with_context(user_id, transcript)
        await update.message.reply_text(
            ai_response, reply_markup=get_main_menu(user_id)
        )

    except Exception as e:
        logger.error(f"Error handling voice: {e}")
        await update.message.reply_text("❌ Ошибка обработки голосового сообщения.")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle document uploads."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        return

    document = update.message.document
    file_name = document.file_name

    await update.message.reply_text(
        f"📂 Получил файл: `{file_name}`.", parse_mode="Markdown"
    )

    # Text-based files processing
    text_extensions = (
        ".txt",
        ".md",
        ".py",
        ".json",
        ".yaml",
        ".yml",
        ".csv",
        ".log",
        ".rtf",
    )
    if file_name.lower().endswith(text_extensions):
        try:
            # Check size (max 2MB for text)
            if document.file_size > 2 * 1024 * 1024:
                await update.message.reply_text(
                    "⚠️ Файл слишком большой для чтения текста (>2MB)."
                )
                return

            new_file = await document.get_file()
            file_content_byte = await new_file.download_as_bytearray()
            text_content = file_content_byte.decode("utf-8", errors="ignore")

            # Basic RTF cleanup (remove {} and control words)
            if file_name.lower().endswith(".rtf"):
                import re

                text_content = re.sub(r"[{}\\]", "", text_content)  # Very basic cleanup
                text_content = re.sub(
                    r"\\[a-z]+\d*", " ", text_content
                )  # Remove control words like \par

            # Save to context
            conv_manager.add_message(
                user_id,
                "user",
                f"[User uploaded file {file_name} content]:\n{text_content}",
            )

            await update.message.reply_text(
                "✅ Текст файла сохранен в контексте диалога."
            )

            # Trigger AI analysis immediately with specific prompt
            prompt = f"Я отправил файл {file_name}. Проанализируй его содержимое."
            ai_response = await query_ollama_with_context(user_id, prompt)

            conv_manager.add_message(user_id, "assistant", ai_response)
            await update.message.reply_text(
                ai_response, reply_markup=get_main_menu(user_id)
            )

        except Exception as e:
            logger.error(f"Failed to read document {file_name}: {e}")
            await update.message.reply_text("❌ Не удалось прочитать текст файла.")

    elif file_name.lower().endswith((".pdf", ".docx", ".doc")):
        await update.message.reply_text(
            "ℹ️ PDF/DOCX пока не поддерживаются для чтения. Пожалуйста, скопируйте текст или сохраните как .txt"
        )
    else:
        # Just notify about receipt for other types
        conv_manager.add_message(
            user_id,
            "user",
            f"[User uploaded file {file_name}, type: {document.mime_type}]",
        )
        await update.message.reply_text(
            "📦 Файл получен. Я запомнил, что вы его прислали."
        )


async def setprovider_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /setprovider command - set inference provider."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    providers = ["ollama", "openai", "gemini", "openrouter", "council"]
    current = config.get("INFERENCE_PROVIDER", "ollama")

    if context.args:
        provider = context.args[0].lower()
        if provider not in providers:
            await update.message.reply_text(
                f"❌ Unknown provider: `{provider}`\nAvailable: {', '.join(providers)}",
                parse_mode="Markdown",
            )
            return

        config.set("INFERENCE_PROVIDER", provider)
        logger.info(f"Provider updated to: {provider}")

        hint = ""
        if provider == "openai":
            hint = "Set your API key with /set_key OPENAI_API_KEY <key>"
        elif provider == "gemini":
            hint = "Set your Gemini API key with /set_key GEMINI_API_KEY <key>"
        else:
            hint = "Make sure Ollama is running"

        await update.message.reply_text(
            f"✅ Provider set to: `{provider}`\n\n💡 {hint}", parse_mode="Markdown"
        )
        return

    buttons = []
    for provider in providers:
        indicator = "✅" if provider == current else "🔄"
        buttons.append(
            [
                InlineKeyboardButton(
                    f"{indicator} {provider.upper()}",
                    callback_data=f"provider:{provider}",
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(buttons)

    await update.message.reply_text(
        f"⚙️ **Select AI Provider**\n\nCurrent: `{current.upper()}`\n\nClick to switch:",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def usage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /usage command - show usage stats."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not usage_tracker:
        await update.message.reply_text("❌ Usage tracker not configured.")
        return

    stats = usage_tracker.get_user_stats(user_id, days=30)

    if not stats:
        await update.message.reply_text(
            "📊 Нет данных об использовании за последние 30 дней."
        )
        return

    msg = (
        f"📊 **Статистика использования (30 дней)**\n\n"
        f"📈 Всего токенов: `{stats.get('total_tokens', 0):,}`\n"
        f"📝 Запросов: `{stats.get('requests', 0)}`\n\n"
        f"**По моделям:**\n"
    )

    for model, tokens in stats.get("by_model", {}).items():
        msg += f"  • {model}: {tokens:,} токенов\n"

    await update.message.reply_text(msg, parse_mode="Markdown")


async def costs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /costs command - show cost breakdown."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not usage_tracker:
        await update.message.reply_text("❌ Usage tracker not configured.")
        return

    user_stats = usage_tracker.get_user_stats(user_id, days=30)

    if not user_stats:
        await update.message.reply_text(
            "📊 Нет данных об использовании за последние 30 дней."
        )
        return

    msg = "💰 **Детальная статистика (30 дней)**\n\n"
    msg += f"📈 **Всего токенов**: {user_stats.get('total_tokens', 0):,}\n"
    msg += f"📝 **Запросов**: {user_stats.get('requests', 0)}\n\n"

    msg += "**По моделям:**\n"
    for model, tokens in user_stats.get("by_model", {}).items():
        msg += f"  • {model}: {tokens:,} токенов\n"

    if user_id == ADMIN_ID:
        msg += "\n🌐 **По провайдерам (все пользователи):**\n"
        providers = (
            usage_tracker.get_provider_breakdown(days=30)
            if hasattr(usage_tracker, "get_provider_breakdown")
            else {}
        )
        for provider, data in providers.items():
            msg += f"  • {provider}: {data.get('tokens', 0):,} токенов ({data.get('requests', 0)} запросов)\n"

    await update.message.reply_text(msg, parse_mode="Markdown")


async def imagine_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /imagine command - generate image (alias for /img)."""
    await img_command(update, context)


async def scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /scan command - trigger Job Hunter."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    await update.message.reply_text(
        "🕵️‍♂️ Запускаю поиск вакансий (Job Hunter/Analyzer)... ожидай отчета."
    )

    script_path = (
        "/home/gonya/Documents/Unified_System/Scripts/automation/job_hunter.py"
    )
    venv_python = "/home/gonya/Documents/Unified_System/venv/bin/python"

    try:
        await asyncio.create_subprocess_exec(
            venv_python,
            script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        logger.info(f"[SCAN] Job Hunter started for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to start Job Hunter: {e}")
        await update.message.reply_text(f"❌ Ошибка запуска: {e}")


async def say_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /say command - speak via Yandex Station."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not ha_controller:
        await update.message.reply_text("❌ Home Assistant not configured.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /say <текст>\nПример: /say Привет, я Гоня!"
        )
        return

    message = " ".join(context.args)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    try:
        if await ha_controller.speak_via_yandex(message):
            await update.message.reply_text(f'🔊 Алиса скажет: "{message[:50]}..."')
        else:
            await update.message.reply_text(
                "❌ Не удалось отправить сообщение на Яндекс Станцию."
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def speak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /speak command - text to speech."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage: /speak <text>\nExample: /speak Hello world"
        )
        return

    text = " ".join(context.args)
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.RECORD_VOICE
    )

    try:
        audio_data = await inference.generate_speech(text)
        if audio_data:
            await update.message.reply_voice(voice=audio_data, caption=text[:100])
        else:
            await update.message.reply_text(
                "❌ TTS generation failed (check logs/api key)."
            )
    except Exception as e:
        logger.error(f"TTS command failed: {e}")
        await update.message.reply_text(f"❌ Error: {e}")


async def mail_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /mail command - check Gmail using per-user OAuth credentials."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    gmail = get_gmail_client(user_id)
    cmd = context.args[0].lower() if context.args else None

    if cmd == "agent" or (not gmail and agent_mail):
        # Check MCP Agent Mail
        if not agent_mail:
            await update.message.reply_text("❌ MCP Mail Client not available.")
            return

        await update.message.reply_text("🔄 Checking Agent Mail...")
        try:
            loop = asyncio.get_running_loop()
            messages = await loop.run_in_executor(
                None, lambda: agent_mail.fetch_inbox(limit=5)
            )
            if not messages:
                await update.message.reply_text("📭 Agent Inbox empty.")
            else:
                msg_text = f"📬 **Agent Inbox ({len(messages)}):**\n\n"
                for m in messages:
                    status = "📖" if m.get("read") else "✉️"
                    msg_text += (
                        f"{status} From: `{m['from']}`\nSubject: {m['subject']}\n\n"
                    )
                await update.message.reply_text(msg_text, parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Error fetching agent mail: {e}")
        return

    # Fallback to Gmail if no arg or arg is not agent
    if not gmail or not gmail.is_valid():
        await update.message.reply_text(
            "❌ Gmail не подключен.\n\n"
            "Используйте /start → 🔗 Connect Google для подключения.\n"
            "Или `/mail agent` для проверки внутренней почты."
        )
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    if not context.args:
        summary = gmail.get_email_summary()
        await update.message.reply_text(summary, parse_mode="Markdown")
        # Also mention agent mail
        if agent_mail:
            await update.message.reply_text(
                "💡 Tip: Use `/mail agent` to check internal agent messages."
            )
        return

    cmd = context.args[0].lower()

    if cmd == "unread":
        count = gmail.get_unread_count()
        await update.message.reply_text(
            f"📬 Непрочитанных писем (Gmail): **{count}**", parse_mode="Markdown"
        )

    elif cmd == "search":
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /mail search <query>")
            return
        query = " ".join(context.args[1:])
        emails = gmail.search_emails(query, max_results=5)
        if not emails:
            await update.message.reply_text(
                f'🔍 По запросу "{query}" ничего не найдено.'
            )
            return
        msg = f'🔍 **Результаты по: "{query}"**\n\n'
        for email in emails:
            sender = (
                email["from"].split("<")[0].strip().strip('"')
                if "<" in email["from"]
                else email["from"]
            )
            subj = email["subject"][:40]
            if len(email["subject"]) > 40:
                subj += "..."
            msg += f"• **{sender}**\n  {subj}\n\n"
        await update.message.reply_text(msg, parse_mode="Markdown")

    elif cmd == "send":
        # /mail send email@example.com | Subject | Body text
        if len(context.args) < 2:
            await update.message.reply_text(
                "📤 **Отправка письма:**\n\n"
                "`/mail send email@example.com | Тема | Текст письма`\n\n"
                "Пример:\n"
                "`/mail send test@gmail.com | Привет! | Это тестовое письмо.`",
                parse_mode="Markdown",
            )
            return

        # Parse: /mail send email | subject | body
        full_text = " ".join(context.args[1:])
        parts = full_text.split("|")
        if len(parts) < 3:
            await update.message.reply_text(
                "❌ Формат: `/mail send email | тема | текст`", parse_mode="Markdown"
            )
            return

        to_email = parts[0].strip()
        subject = parts[1].strip()
        body = "|".join(parts[2:]).strip()  # In case body contains |

        result = gmail.send_email(to=to_email, subject=subject, body=body)
        if result:
            await update.message.reply_text(f"✅ Письмо отправлено на {to_email}")
        else:
            await update.message.reply_text(
                "❌ Ошибка отправки письма. Проверьте права OAuth."
            )

    elif cmd == "read":
        # /mail read <message_id> - read full email
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /mail read <message_id>")
            return
        msg_id = context.args[1]
        body = gmail.get_email_body(msg_id)
        if body:
            # Truncate if too long
            if len(body) > 3000:
                body = body[:3000] + "\n\n... (обрезано)"
            await update.message.reply_text(
                f"📧 **Содержимое письма:**\n\n{body[:4000]}"
            )
            gmail.mark_as_read(msg_id)
        else:
            await update.message.reply_text("❌ Не удалось прочитать письмо.")

    elif cmd == "list":
        # /mail list [count] - list recent emails with IDs
        count = 5
        if len(context.args) > 1:
            try:
                count = int(context.args[1])
                count = min(count, 10)  # Max 10
            except ValueError:
                pass

        emails = gmail.get_recent_emails(max_results=count)
        if not emails:
            await update.message.reply_text("📭 Нет писем в ящике.")
            return

        msg = f"📬 **Последние {len(emails)} писем:**\n\n"
        for i, email in enumerate(emails, 1):
            sender = (
                email["from"].split("<")[0].strip().strip('"')
                if "<" in email["from"]
                else email["from"]
            )
            status = "🔵" if email.get("unread") else "⚪"
            subj = email["subject"][:35]
            if len(email["subject"]) > 35:
                subj += "..."
            msg += f"{status} **{i}. {sender}**\n"
            msg += f"   {subj}\n"
            msg += f"   `ID: {email['id'][:20]}...`\n\n"

        msg += "_Используйте_ `/mail read <ID>` _для чтения_"
        await update.message.reply_text(msg, parse_mode="Markdown")

    elif cmd == "archive":
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /mail archive <message_id>")
            return
        if gmail.archive_email(context.args[1]):
            await update.message.reply_text("✅ Письмо архивировано.")
        else:
            await update.message.reply_text("❌ Ошибка архивации.")

    elif cmd == "trash":
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /mail trash <message_id>")
            return
        if gmail.trash_email(context.args[1]):
            await update.message.reply_text("🗑️ Письмо удалено.")
        else:
            await update.message.reply_text("❌ Ошибка удаления.")

    else:
        await update.message.reply_text(
            "📧 **Gmail Commands:**\n\n"
            "**Чтение:**\n"
            "`/mail` - сводка непрочитанных\n"
            "`/mail unread` - количество непрочитанных\n"
            "`/mail list [N]` - список N последних писем\n"
            "`/mail read <ID>` - прочитать письмо\n"
            "`/mail search <query>` - поиск\n\n"
            "**Отправка:**\n"
            "`/mail send email | тема | текст`\n\n"
            "**Управление:**\n"
            "`/mail archive <ID>` - архивировать\n"
            "`/mail trash <ID>` - удалить",
            parse_mode="Markdown",
        )


async def notify_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /notify command - manage notification settings."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not notify_manager:
        await update.message.reply_text("❌ Notify manager not configured.")
        return

    if not context.args:
        quiet = notify_manager.is_quiet_hours()
        status = "🌙 Тихий режим" if quiet else "🔔 Активный режим"
        await update.message.reply_text(
            f"{status}\n\n"
            f"Тихие часы: {notify_manager.quiet_start.strftime('%H:%M')} - "
            f"{notify_manager.quiet_end.strftime('%H:%M')}\n\n"
            "Команды:\n"
            "/notify status - текущий статус\n"
            "/notify quiet HH:MM HH:MM - установить тихие часы"
        )
        return

    cmd = context.args[0].lower()

    if cmd == "status":
        quiet = notify_manager.is_quiet_hours()
        await update.message.reply_text(
            "🌙 Сейчас тихие часы" if quiet else "🔔 Сейчас активный режим"
        )

    elif cmd == "quiet":
        if len(context.args) < 3:
            await update.message.reply_text("Usage: /notify quiet 23:00 08:00")
            return

        try:
            start_str = context.args[1]
            end_str = context.args[2]
            start = datetime.strptime(start_str, "%H:%M").time()
            end = datetime.strptime(end_str, "%H:%M").time()
            notify_manager.quiet_start = start
            notify_manager.quiet_end = end
            await update.message.reply_text(
                f"✅ Тихие часы установлены: {start_str} - {end_str}"
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка формата времени: {e}")


async def remind_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /remind command - set a reminder."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /remind <time> <text>\nExample: /remind 10m Выключи духовку\nTime units: s, m, h, d"
        )
        return

    import re

    time_str = context.args[0].lower()
    text = " ".join(context.args[1:])

    match = re.match(r"^(\d+)([smhd])$", time_str)
    if not match:
        await update.message.reply_text("❌ Invalid time format. Use 10s, 5m, 1h, 2d")
        return

    amount = int(match.group(1))
    unit = match.group(2)

    delta = timedelta()
    if unit == "s":
        delta = timedelta(seconds=amount)
    elif unit == "m":
        delta = timedelta(minutes=amount)
    elif unit == "h":
        delta = timedelta(hours=amount)
    elif unit == "d":
        delta = timedelta(days=amount)

    run_date = datetime.now() + delta

    # Schedule reminder (simplified - stores in context for now)
    context.job_queue.run_once(
        lambda ctx: ctx.bot.send_message(
            chat_id=user_id, text=f"⏰ Напоминание: {text}"
        ),
        when=delta,
        name=f"remind_{user_id}_{run_date.timestamp()}",
    )

    await update.message.reply_text(
        f"✅ Напоминание установлено на {run_date.strftime('%H:%M:%S')}"
    )


async def note_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /note command - create a Notion page."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not notion_client:
        await update.message.reply_text("❌ Notion not configured.")
        return

    if not context.args:
        await update.message.reply_text(
            "Example: /note Meeting Notes | Discussed project X\nUsage: /note <title> [| content]"
        )
        return

    full_text = " ".join(context.args)
    if "|" in full_text:
        title, content = full_text.split("|", 1)
        title = title.strip()
        content = content.strip()
    else:
        title = full_text
        content = ""

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    try:
        url = await notion_client.create_page(title, content)
        if url:
            await update.message.reply_text(
                f"✅ Created Note: [{title}]({url})", parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                "❌ Failed to create note. Check logs/config."
            )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")


async def digest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /digest command - generate daily digest."""
    user_id = update.effective_user.id
    username = update.effective_user.first_name or "User"

    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not digest_service:
        await update.message.reply_text("❌ Digest service not initialized.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.TYPING
    )

    try:
        digest = await digest_service.generate_digest(user_id, username)
        await update.message.reply_text(digest, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Digest generation failed: {e}")
        await update.message.reply_text(f"❌ Не удалось создать дайджест: {e}")


async def backup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /backup command - create and send database backup."""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text("⛔️ Admin only command.")
        return

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=ChatAction.UPLOAD_DOCUMENT
    )

    import zipfile

    files = [
        "tasks.db",
        "usage.db",
        "jobs.db",
        "user_context.db",
        "windows_ai_core.json",
    ]
    backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"

    try:
        with zipfile.ZipFile(backup_name, "w", zipfile.ZIP_DEFLATED) as zipf:
            found = False
            for file in files:
                if os.path.exists(file):
                    zipf.write(file)
                    found = True
                elif os.path.exists(f"Projects/AI_Core/{file}"):
                    zipf.write(f"Projects/AI_Core/{file}", arcname=file)
                    found = True

            if not found:
                await update.message.reply_text(
                    "⚠️ Не найдено файлов баз данных для бэкапа."
                )
                os.remove(backup_name)
                return

        await update.message.reply_document(
            document=open(backup_name, "rb"),
            caption=(f"📦 Database Backup ({datetime.now().strftime('%Y-%m-%d')})"),
        )
        os.remove(backup_name)

    except Exception as e:
        logger.error(f"Backup failed: {e}")
        await update.message.reply_text(f"❌ Backup error: {e}")


async def update_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /update command - self-update via git and restart."""
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        await update.message.reply_text(
            "❌ Только главный администратор может обновлять бота."
        )
        return

    await update.message.reply_text(
        "🔄 Начинаю обновление...\n1. Git Fetch & Reset (Force Update)..."
    )

    import subprocess

    try:
        project_dir = "/home/gonya/Documents/Unified_System"
        git_command = (
            f"cd {project_dir} && git fetch origin && git reset --hard origin/main"
        )

        proc = await asyncio.create_subprocess_shell(
            git_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            await update.message.reply_text(f"❌ Git Update Failed:\n{stderr.decode()}")
            return

        await update.message.reply_text(
            f"✅ Code force-updated.\nOutput: {stdout.decode()[:200]}...\n\n2. Restarting service..."
        )

        await update.message.reply_text(
            "♻️ Перезапускаю сервис (systemd)... Я вернусь через 5-10 секунд."
        )
        subprocess.Popen(["sudo", "systemctl", "restart", "ai-bot"])

    except Exception as e:
        logger.error(f"Update failed: {e}")
        await update.message.reply_text(f"❌ Critical Update Error: {e}")


async def health_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /health command - view health stats."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not health_integration:
        await update.message.reply_text("❌ Health integration not configured.")
        return

    if not context.args:
        stats = health_integration.get_today_stats(user_id)
        msg = (
            "🩺 **Твое здоровье (Сегодня):**\n\n"
            f"👣 Шаги: `{stats.get('steps', 0):,.0f}`\n"
            f"⚖️ Вес: `{stats.get('weight', 0):.1f} kg`\n"
            f"😴 Сон: `{stats.get('sleep', 0):.1f} h`\n\n"
            "Команды:\n"
            "`/health add <metric> <value>`\n"
            "`/health goal <metric> <value>`"
        )
        await update.message.reply_text(msg, parse_mode="Markdown")
        return

    cmd = context.args[0].lower()

    if cmd == "add":
        if len(context.args) < 3:
            await update.message.reply_text(
                "Usage: /health add <steps|weight|sleep> <value>"
            )
            return

        metric = context.args[1].lower()
        try:
            val = float(context.args[2])
        except ValueError:
            await update.message.reply_text("❌ Значение должно быть числом.")
            return

        unit = "count"
        if metric == "weight":
            unit = "kg"
        elif metric == "sleep":
            unit = "hours"

        if health_integration.add_metric(user_id, metric, val, unit, "manual"):
            await update.message.reply_text(f"✅ Записано: {metric} = {val}")
        else:
            await update.message.reply_text("❌ Ошибка записи.")

    elif cmd == "goal":
        if len(context.args) < 3:
            await update.message.reply_text(
                "Usage: /health goal <steps|weight|sleep> <value>"
            )
            return
        metric = context.args[1].lower()
        try:
            val = float(context.args[2])
            health_integration.set_goal(user_id, metric, val)
            await update.message.reply_text(f"🎯 Цель обновлена: {metric} = {val}")
        except ValueError:
            await update.message.reply_text("❌ Значение должно быть числом.")


async def calendar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /calendar command - calendar management."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    client = get_calendar_client(user_id)
    if not client:
        await update.message.reply_text(
            "❌ Google Calendar not configured.\n\nUse /start to connect."
        )
        return

    if not context.args:
        await update.message.reply_text(
            "📅 **Calendar Commands:**\n\n/calendar today - события сегодня\n/calendar week - на неделю",
            parse_mode="Markdown",
        )
        return

    cmd = context.args[0].lower()

    if cmd == "today":
        events = client.get_upcoming_events(days=1)
        if not events:
            await update.message.reply_text("📅 Сегодня нет событий.")
            return

        msg = f"📅 **События сегодня ({len(events)}):**\n\n"
        for event in events:
            formatted = client.format_event(event)
            msg += f"• {formatted}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")

    elif cmd == "week":
        events = client.get_upcoming_events(days=7)
        if not events:
            await update.message.reply_text("📅 На этой неделе нет событий.")
            return

        msg = f"📅 **События на неделю ({len(events)}):**\n\n"
        for event in events:
            formatted = client.format_event(event)
            msg += f"• {formatted}\n"
        await update.message.reply_text(msg, parse_mode="Markdown")

    else:
        await update.message.reply_text(f"Unknown command: {cmd}")


async def linear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /linear command - Linear task management."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not linear_client or not linear_client.api_key:
        await update.message.reply_text("❌ Linear API key not configured.")
        return

    if not context.args:
        await update.message.reply_text(
            "📋 **Linear Commands:**\n\n"
            "/linear me - мои задачи\n"
            "/linear create <title> - создать задачу\n"
            "/linear teams - список команд",
            parse_mode="Markdown",
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
        await update.message.reply_text(
            msg, parse_mode="Markdown", disable_web_page_preview=True
        )

    elif cmd == "create":
        if len(context.args) < 2:
            await update.message.reply_text("Usage: /linear create <title>")
            return

        title = " ".join(context.args[1:])
        issue = linear_client.create_issue(title, priority=3)

        if issue:
            await update.message.reply_text(
                f"✅ Задача создана: [{issue['identifier']}]({issue['url']})\n{issue['title']}",
                parse_mode="Markdown",
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


async def todo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /todo command - manage tasks."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    if not task_manager:
        await update.message.reply_text("❌ Task manager not configured.")
        return

    if not context.args:
        await update.message.reply_text(
            "📝 **Task Manager**\n\n"
            "Usage:\n"
            "`/todo add <text>` - Add task\n"
            "`/todo list` - List pending tasks\n"
            "`/todo done <id>` - Complete task",
            parse_mode="Markdown",
        )
        return

    subcmd = context.args[0].lower()

    if subcmd == "add":
        text = " ".join(context.args[1:])
        if not text:
            await update.message.reply_text("Usage: /todo add <text>")
            return

        task_id = task_manager.add_task(user_id, text)
        await update.message.reply_text(
            f"✅ Задача добавлена! ID: `{task_id}`", parse_mode="Markdown"
        )

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
                await update.message.reply_text(
                    f"✅ Задача `#{task_id}` выполнена!", parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    f"❌ Не удалось найти или обновить задачу `#{task_id}`."
                )
        except ValueError:
            await update.message.reply_text("❌ ID должен быть числом.")


async def beads_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /beads command - Git-native issue tracking with Beads."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    # Beads working directory
    beads_dir = "/Users/macbook/Documents/Unified_System"

    if not context.args:
        await update.message.reply_text(
            "📿 **Beads - Git-native Issue Tracker**\n\n"
            "**Команды:**\n"
            "`/beads list` - Активные задачи\n"
            "`/beads create <title>` - Создать задачу\n"
            "`/beads show <id>` - Детали задачи\n"
            "`/beads start <id>` - Начать работу\n"
            "`/beads done <id>` - Завершить задачу\n"
            "`/beads sync` - Синхронизировать\n\n"
            "💡 Beads хранит задачи прямо в репозитории!",
            parse_mode="Markdown",
        )
        return

    subcmd = context.args[0].lower()

    try:
        if subcmd == "list":
            # List active tasks
            process = await asyncio.create_subprocess_exec(
                "bd",
                "list",
                "--status",
                "in_progress,todo",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=beads_dir,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await update.message.reply_text(f"❌ Ошибка: {stderr.decode()}")
                return

            output = stdout.decode().strip()
            if not output or "No issues found" in output:
                await update.message.reply_text("📭 Нет активных задач в Beads.")
                return

            # Parse and format output
            lines = output.split("\n")
            msg = "📿 **Активные задачи Beads:**\n\n"
            for line in lines[:15]:  # Limit to 15
                if line.strip():
                    # Format: ID | Status | Title
                    msg += f"• `{line.strip()}`\n"
            await update.message.reply_text(msg, parse_mode="Markdown")

        elif subcmd == "create":
            if len(context.args) < 2:
                await update.message.reply_text(
                    "Usage: `/beads create <title>`", parse_mode="Markdown"
                )
                return

            title = " ".join(context.args[1:])
            process = await asyncio.create_subprocess_exec(
                "bd",
                "create",
                title,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=beads_dir,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await update.message.reply_text(f"❌ Ошибка: {stderr.decode()}")
                return

            output = stdout.decode().strip()
            await update.message.reply_text(
                f"✅ Задача создана!\n\n`{output}`", parse_mode="Markdown"
            )

        elif subcmd == "show":
            if len(context.args) < 2:
                await update.message.reply_text(
                    "Usage: `/beads show <issue-id>`", parse_mode="Markdown"
                )
                return

            issue_id = context.args[1]
            process = await asyncio.create_subprocess_exec(
                "bd",
                "show",
                issue_id,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=beads_dir,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await update.message.reply_text(
                    f"❌ Задача не найдена: {stderr.decode()}"
                )
                return

            output = stdout.decode().strip()
            await update.message.reply_text(
                f"📿 **Детали задачи:**\n\n```\n{output[:3000]}\n```",
                parse_mode="Markdown",
            )

        elif subcmd == "start":
            if len(context.args) < 2:
                await update.message.reply_text(
                    "Usage: `/beads start <issue-id>`", parse_mode="Markdown"
                )
                return

            issue_id = context.args[1]
            process = await asyncio.create_subprocess_exec(
                "bd",
                "update",
                issue_id,
                "--status",
                "in_progress",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=beads_dir,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await update.message.reply_text(f"❌ Ошибка: {stderr.decode()}")
                return

            await update.message.reply_text(
                f"▶️ Задача `{issue_id}` в работе!", parse_mode="Markdown"
            )

        elif subcmd == "done":
            if len(context.args) < 2:
                await update.message.reply_text(
                    "Usage: `/beads done <issue-id>`", parse_mode="Markdown"
                )
                return

            issue_id = context.args[1]
            process = await asyncio.create_subprocess_exec(
                "bd",
                "update",
                issue_id,
                "--status",
                "done",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=beads_dir,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await update.message.reply_text(f"❌ Ошибка: {stderr.decode()}")
                return

            await update.message.reply_text(
                f"✅ Задача `{issue_id}` завершена!", parse_mode="Markdown"
            )

        elif subcmd == "sync":
            await update.message.reply_text("🔄 Синхронизирую...")
            process = await asyncio.create_subprocess_exec(
                "bd",
                "sync",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=beads_dir,
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                await update.message.reply_text(
                    f"❌ Ошибка синхронизации: {stderr.decode()}"
                )
                return

            await update.message.reply_text("✅ Beads синхронизирован с репозиторием!")

        else:
            await update.message.reply_text(
                f"❌ Неизвестная команда: `{subcmd}`\n\nИспользуйте /beads для справки.",
                parse_mode="Markdown",
            )

    except Exception as e:
        logger.error(f"[BEADS] Error: {e}")
        await update.message.reply_text(f"❌ Ошибка Beads: {str(e)}")


async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /settings command - show settings menu."""
    user_id = update.effective_user.id
    if not db.is_approved(user_id):
        await update.message.reply_text("⛔️ Access denied.")
        return

    current_provider = config.get("INFERENCE_PROVIDER", "ollama")
    current_model = config.get("MODEL_NAME", "unknown")
    await update.message.reply_text(
        f"⚙️ **Настройки AI**\n\n"
        f"🤖 Модель: `{current_model}`\n"
        f"🔌 Провайдер: `{current_provider.upper()}`\n\n"
        f"Выберите опцию для изменения:",
        parse_mode="Markdown",
        reply_markup=get_settings_menu(),
    )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by updates."""
    logger.error(f"[ERROR] Exception while handling an update: {context.error}")
    import traceback

    tb_str = "".join(
        traceback.format_exception(None, context.error, context.error.__traceback__)
    )
    logger.error(f"[ERROR] Traceback:\n{tb_str}")

    # Try to notify the user
    if update and hasattr(update, "effective_chat") and update.effective_chat:
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ An error occurred while processing your request. Please try again.",
            )
        except Exception as e:
            logger.error(f"[ERROR] Failed to send error message to user: {e}")


async def msg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /msg <user_id|username> <text> command."""
    sender_id = update.effective_user.id
    sender_name = update.effective_user.username or update.effective_user.full_name

    if not db.is_approved(sender_id):
        return

    if not context.args or len(context.args) < 2:
        await update.message.reply_text(
            "Usage: `/msg <id|username> <message>`", parse_mode="Markdown"
        )
        return

    target = context.args[0]
    message = " ".join(context.args[1:])

    target_id = None

    # Try to resolve target
    if target.isdigit():
        target_id = int(target)
    else:
        # Simple scan of inactive users (all users in DB)
        all_users = db.get_inactive_users(hours=0)
        target_clean = target.lstrip("@")
        for u in all_users:
            if u.get("username") == target_clean:
                target_id = u["user_id"]
                break

    if target_id:
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=f"📩 **Сообщение от @{sender_name}:**\n\n{message}",
                parse_mode="Markdown",
            )
            await update.message.reply_text(f"✅ Отправлено пользователю `{target_id}`")
        except Exception as e:
            await update.message.reply_text(
                f"❌ Не удалось отправить (пользователь заблокировал бота?): {e}"
            )
    else:
        await update.message.reply_text(f"❌ Пользователь `{target}` не найден.")


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
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("brief", brief_command))
    application.add_handler(CommandHandler("memory", memory_command))
    application.add_handler(CommandHandler("newtask", newtask_command))
    application.add_handler(CommandHandler("msg", msg_command))
    application.add_handler(CommandHandler("agent", agent_command))
    application.add_handler(CommandHandler("pipeline", pipeline_command))
    application.add_handler(CommandHandler("img", img_command))
    application.add_handler(CommandHandler("имаж", img_command))
    application.add_handler(CommandHandler("картинка", img_command))
    application.add_handler(CommandHandler("image", img_command))
    application.add_handler(CommandHandler("tl", tl_command))
    application.add_handler(CommandHandler("set_key", set_key))
    application.add_handler(CommandHandler("approve", approve_user))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("ha", ha_command))
    application.add_handler(CommandHandler("models", models_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(CommandHandler("infra", infra_command))
    application.add_handler(CommandHandler("setprovider", setprovider_command))
    application.add_handler(CommandHandler("usage", usage_command))
    application.add_handler(CommandHandler("costs", costs_command))
    application.add_handler(CommandHandler("imagine", imagine_command))
    application.add_handler(CommandHandler("scan", scan_command))
    application.add_handler(CommandHandler("say", say_command))
    application.add_handler(CommandHandler("speak", speak_command))
    application.add_handler(CommandHandler("mail", mail_command))
    application.add_handler(CommandHandler("notify", notify_command))
    application.add_handler(CommandHandler("remind", remind_command))
    application.add_handler(CommandHandler("note", note_command))
    application.add_handler(CommandHandler("digest", digest_command))
    application.add_handler(CommandHandler("backup", backup_command))
    application.add_handler(CommandHandler("update", update_command))
    application.add_handler(CommandHandler("health", health_command))
    application.add_handler(CommandHandler("calendar", calendar_command))
    application.add_handler(CommandHandler("linear", linear_command))
    application.add_handler(CommandHandler("todo", todo_command))
    application.add_handler(CommandHandler("beads", beads_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    logger.info("[STARTUP] All handlers registered")

    logger.info("[STARTUP] Starting polling...")
    print("Bot V2 (AI_Core) is running...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
