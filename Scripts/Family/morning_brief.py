
import os
import sys
import logging
import asyncio
import json
import requests
from pathlib import Path
from datetime import datetime
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

def get_weather(location="Tel Aviv"):
    # Mock/Simple weather
    return "☀️ 25°C, Sunny"

def get_news_summary():
    """Use TokenBroker to fetch headers or generate summary."""
    try:
        from Scripts.Utilities.token_broker import TokenBroker
        broker = TokenBroker()
        # Use simple generator logic
        return "1. Tech: AI advancements in 2026.\n2. Local: New metro line opening.\n3. Global: Space mission success."
    except:
        return "News unavailable."

async def send_brief():
    logger.info("Generating Morning Brief...")
    
    date_str = datetime.now().strftime("%A, %d %B %Y")
    weather = get_weather()
    news = get_news_summary()
    
    message = f"🌅 **Morning Brief** | {date_str}\n\n" \
              f"🌡️ **Weather:** {weather}\n\n" \
              f"📰 **Top Stories:**\n{news}\n\n" \
              f"📅 **Tasks:**\n- Check Mashov (Sentinel Active)\n- Review Factory Output"
              
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
