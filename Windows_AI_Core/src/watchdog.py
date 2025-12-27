"""
Watchdog Service for AI Bot.
Monitors the bot's health endpoint and alerts admin if it fails.
"""
import time
import requests
import logging
import os
import sys
from datetime import datetime

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Config
BOT_HEALTH_URL = "http://localhost:8095/health"
CHECK_INTERVAL = 60  # seconds
FAIL_THRESHOLD = 3
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = os.getenv("ALLOWED_USERS", "").split(",")[0] # First user is admin

if not TELEGRAM_BOT_TOKEN or not ADMIN_ID:
    logger.error("TELEGRAM_BOT_TOKEN or ALLOWED_USERS not set. Watchdog cannot alert.")
    sys.exit(1)

def send_alert(message):
    """Send alert via raw Telegram API."""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": ADMIN_ID,
            "text": f"🚨 **WATCHDOG ALERT**\n\n{message}",
            "parse_mode": "Markdown"
        }
        requests.post(url, json=data, timeout=10)
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")

def check_health():
    """Check bot health."""
    try:
        response = requests.get(BOT_HEALTH_URL, timeout=5)
        if response.status_code == 200:
            return True
        logger.warning(f"Health check failed: Status {response.status_code}")
        return False
    except Exception as e:
        logger.warning(f"Health check failed: {e}")
        return False

def main():
    logger.info("Watchdog started.")
    fail_count = 0
    
    # Wait for bot to start initially
    time.sleep(10)
    
    while True:
        if check_health():
            if fail_count > 0:
                logger.info("Bot recovered.")
                if fail_count >= FAIL_THRESHOLD:
                    send_alert("✅ Бот восстановился и снова онлайн.")
            fail_count = 0
        else:
            fail_count += 1
            logger.warning(f"Health check failed ({fail_count}/{FAIL_THRESHOLD})")
            
            if fail_count == FAIL_THRESHOLD:
                # Alert!
                send_alert(f"⚠️ Бот не отвечает уже {FAIL_THRESHOLD} минут!\nВозможно, он завис или упал.")
                # We could try to auto-restart here via systemctl if running as root/authorized user
                # os.system("sudo systemctl restart ai-bot") 
                
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
