import asyncio
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Setup Paths
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
FAMILY_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

# Load both AI_Core and main environment configurations
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")
load_dotenv(ROOT_DIR / ".env")

# Import VAPIClient for voice delivery
VAPI_AVAILABLE = False
try:
    sys.path.insert(0, str(ROOT_DIR / "Projects/AI_Core/src"))
    from vapi_client import VAPIClient

    VAPI_AVAILABLE = True
except ImportError as e:
    logger_init = logging.getLogger("MorningBrief")
    logger_init.debug(f"VAPI client not available: {e}")

# Logging
LOG_DIR = ROOT_DIR / "logs/family"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_DIR / "morning_brief.log"), logging.StreamHandler()],
)
logger = logging.getLogger("MorningBrief")

# User Configuration with Phone Numbers
USERS = {
    "Admin": {"telegram_id": 708531393, "phone": os.getenv("PHONE_ADMIN", ""), "name": "Igor"},
    "Azure": {
        "telegram_id": 578363419,
        "phone": os.getenv("PHONE_AZURE", os.getenv("PHONE_KOSTYA", "")),
        "name": "Azure",
    },
}

# Delivery Settings
ENABLE_VOICE = os.getenv("BRIEF_ENABLE_VOICE", "false").lower() == "true"
ENABLE_TELEGRAM = os.getenv("BRIEF_ENABLE_TELEGRAM", "true").lower() == "true"


def get_weather(lat=32.08, lon=34.78):  # Tel Aviv by default
    """Fetch real weather from OpenMeteo"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            cw = data.get("current_weather", {})
            temp = cw.get("temperature")
            # Code mapping could be added, but simple temp is fine
            return f"{temp}°C"
        return "N/A"
    except Exception as e:
        logger.error(f"Weather error: {e}")
        return "Unavailable"


async def get_homework_summary():
    """Fetch homework from Sentinel + Mashov"""
    report = []

    # 1. Gmail Sentinel
    try:
        from Scripts.Family.homework_sentinel import scan_mailbox, summarize_tasks

        emails = scan_mailbox()
        if emails:
            gmail_summary = summarize_tasks(emails)
            report.append(f"📧 **Д/З из почты:**\n{gmail_summary}")
        else:
            report.append("📧 Gmail: Нет новых писем с домашкой.")
    except Exception as e:
        logger.error(f"Sentinel error: {e}")
        report.append(f"📧 Ошибка Sentinel: {e}")

    # 2. Mashov/Webtop (School Data)
    try:
        # Check for WEBTOP_TOKEN first as it supersedes Mashov credentials
        webtop_token = os.getenv("WEBTOP_TOKEN")
        if webtop_token:
            from Projects.AI_Core.src.webtop_client import WebtopClient

            webtop = WebtopClient(webtop_token)
            if webtop.check_auth():
                hw = webtop.fetch_homework() or []
                grades = webtop.fetch_grades() or []

                summary_lines = []
                if hw:
                    summary_lines.append(f"📚 {len(hw)} заданий в Webtop")
                if grades:
                    summary_lines.append(f"📊 {len(grades)} новых оценок")

                if not hw and not grades:
                    summary_lines.append("✅ Нет новых заданий или оценок")

                report.append("🏫 **Школа (Webtop):**\n" + "\n".join(summary_lines))
            else:
                report.append("🏫 Webtop: Ошибка авторизации (Token expired?)")

        else:
            # Fallback to legacy Mashov
            from Projects.AI_Core.src.mashov_client import MashovClient

            user = os.getenv("MASHOV_USER")
            pwd = os.getenv("MASHOV_PASS")
            school = os.getenv("MASHOV_SCHOOL")

            if user and pwd and school and school != "0":
                mashov = MashovClient(username=user, password=pwd, school_id=int(school))
                if await mashov.login():
                    student_id = mashov.get_student_id()
                    if student_id:
                        hw = await mashov.fetch_homework(student_id)
                        report.append(f"🏫 **Mashov:** {len(hw) if hw else 0} заданий")
                    else:
                        report.append("🏫 Mashov: Ошибка получения ID")
                else:
                    report.append("🏫 Mashov: Ошибка входа")
            else:
                logger.debug("[SCHOOL] No school credentials configured")

    except Exception as e:
        logger.error(f"[SCHOOL] Integration error: {e}")
        report.append(f"🏫 Школа: Ошибка {str(e)}")

    return "\n\n".join(report)


async def send_voice_brief(vapi_client: "VAPIClient", phone: str, name: str, message: str):
    """Send morning brief as voice call via VAPI."""
    if not phone or not phone.startswith("+"):
        logger.warning(f"Invalid phone number for {name}: {phone}")
        return False

    try:
        # Convert text brief to natural speech format (remove Markdown)
        speech_message = (
            message.replace("**", "")
            .replace("*", "")
            .replace("🌅", "")
            .replace("🌡️", "")
            .replace("📚", "")
            .replace("🚀", "")
        )

        # Create system prompt for voice assistant
        system_prompt = (
            f"You are a friendly morning briefing assistant. "
            f"Read the following information clearly in Russian to {name}: {speech_message}"
        )

        call_info = await vapi_client.create_phone_call(phone_number=phone, system_message=system_prompt)

        if call_info:
            call_id = call_info.get("id", "unknown")
            logger.info(f"Voice call initiated for {name} to {phone}: {call_id}")
            return True
        else:
            logger.error(f"Failed to initiate call for {name}")
            return False

    except Exception as e:
        logger.error(f"Voice call failed for {name}: {e}")
        return False


async def send_brief():
    logger.info("Generating Morning Brief...")

    # Date in Russian manually to avoid locale issues on minimal envs
    now = datetime.now()
    months = [
        "Января",
        "Февраля",
        "Марта",
        "Апреля",
        "Мая",
        "Июня",
        "Июля",
        "Августа",
        "Сентября",
        "Октября",
        "Ноября",
        "Декабря",
    ]
    weekdays = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]

    date_str = f"{weekdays[now.weekday()]}, {now.day} {months[now.month - 1]} {now.year}"

    weather = get_weather()
    # news = get_news_summary() # Keep mock or remove if irrelevant
    homework = await get_homework_summary()

    message = (
        f"🌅 **Утренняя Сводка** | {date_str}\n\n"
        f"🌡️ **Погода:** {weather}\n\n"
        f"📚 **Школа и Задачи:**\n{homework}\n\n"
        f"🚀 **Хорошего дня!**"
    )

    logger.info(f"Brief Content:\n{message}")

    # Initialize VAPI client for voice delivery
    vapi_client = None
    if ENABLE_VOICE and VAPI_AVAILABLE:
        vapi_key = os.getenv("VAPI_API_KEY")
        if vapi_key:
            try:
                vapi_client = VAPIClient(vapi_key)
                if not vapi_client.is_valid():
                    logger.warning("VAPI client invalid, voice calls disabled")
                    vapi_client = None
            except Exception as e:
                logger.error(f"Failed to init VAPI: {e}")
    elif ENABLE_VOICE:
        logger.warning("Voice delivery enabled but VAPI SDK not available")

    # Telegram delivery
    if ENABLE_TELEGRAM:
        token = os.getenv("TELEGRAM_BOT_TOKEN")

        if token:
            for name, user_info in USERS.items():
                chat_id = user_info.get("telegram_id")
                if chat_id:
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    try:
                        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
                        res = requests.post(url, json=payload, timeout=5)
                        if res.status_code == 200:
                            logger.info(f"Telegram brief sent to {name}")
                        else:
                            logger.error(f"Failed to send to {name}: {res.text}")
                    except Exception as e:
                        logger.error(f"Telegram send failed for {name}: {e}")
                else:
                    logger.warning(f"Skipping {name} (No Telegram ID)")
        else:
            logger.warning("Bot Token missing. Telegram delivery skipped.")
    else:
        logger.info("Telegram delivery disabled")

    # Voice delivery
    if ENABLE_VOICE and vapi_client:
        for name, user_info in USERS.items():
            phone = user_info.get("phone")
            user_name = user_info.get("name", name)
            if phone:
                success = await send_voice_brief(vapi_client, phone, user_name, message)
                if success:
                    logger.info(f"Voice brief sent to {name}")
            else:
                logger.info(f"No phone number for {name}, skipping voice delivery")


if __name__ == "__main__":
    asyncio.run(send_brief())
