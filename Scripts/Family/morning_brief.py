
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
sys.path.append(str(ROOT_DIR))
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")

# Logging
LOG_DIR = ROOT_DIR / "logs/family"
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "morning_brief.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MorningBrief")

# Chat IDs
USERS = {
    "Admin": 708531393,
    "Kostya": 578363419
}

def get_weather(lat=32.08, lon=34.78): # Tel Aviv by default
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

def get_homework_summary():
    """Fetch homework from Sentinel + Mashov"""
    report = []
    
    # 1. Gmail Sentinel
    try:
        from Scripts.Family.homework_sentinel import scan_mailbox, summarize_tasks
        emails = scan_mailbox()
        if emails:
            gmail_summary = summarize_tasks(emails)
            report.append(f"📧 **Gmail Homework:**\n{gmail_summary}")
        else:
            report.append("📧 Gmail: No new homework emails.")
    except Exception as e:
        logger.error(f"Sentinel error: {e}")
        report.append(f"📧 Sentinel Error: {e}")

    # 2. Mashov (if configured)
    try:
        from Scripts.Family.mashov_login import login_mashov, fetch_homework, fetch_grades
        user = os.getenv("MASHOV_USER")
        pwd = os.getenv("MASHOV_PASS")
        school = os.getenv("MASHOV_SCHOOL")
        
        if user and pwd and school and school != "0":
            session, data = login_mashov(user, pwd, int(school))
            if session and data:
                uid = data['credential']['userId']
                hw = fetch_homework(session, uid)
                if hw:
                    report.append(f"🏫 **Mashov Homework:** {len(hw)} tasks pending.")
                else:
                    report.append("🏫 Mashov: No pending tasks.")
            else:
                report.append("🏫 Mashov: Login failed.")
        else:
            report.append("🏫 Mashov: Not configured (Missing School Symbol).")
            
    except Exception as e:
        logger.error(f"Mashov error: {e}")

    return "\n\n".join(report)

async def send_brief():
    logger.info("Generating Morning Brief...")

    date_str = datetime.now().strftime("%A, %d %B %Y")
    weather = get_weather()
    # news = get_news_summary() # Keep mock or remove if irrelevant
    homework = get_homework_summary()

    message = f"🌅 **Morning Brief** | {date_str}\n\n" \
              f"🌡️ **Weather:** {weather}\n\n" \
              f"📚 **School Update:**\n{homework}\n\n" \
              f"🚀 **Have a great day!**"

    logger.info(f"Brief Content:\n{message}")

    # Send via Bot API
    token = os.getenv("TELEGRAM_BOT_TOKEN") or "8518131338:AAH_mDgVZ2UclJvUVT0RI5uypeazSORx2Wk"

    if token:
        for name, chat_id in USERS.items():
            if chat_id:
                url = f"https://api.telegram.org/bot{token}/sendMessage"
                try:
                    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
                    res = requests.post(url, json=payload, timeout=5)
                    if res.status_code == 200:
                        logger.info(f"Sent to {name} ({chat_id})")
                    else:
                        logger.error(f"Failed to send to {name}: {res.text}")
                except Exception as e:
                    logger.error(f"Failed to send to {name}: {e}")
            else:
                logger.warning(f"Skipping {name} (No Chat ID)")
    else:
        logger.warning("Bot Token missing. Brief generated but not sent.")

if __name__ == "__main__":
    asyncio.run(send_brief())
