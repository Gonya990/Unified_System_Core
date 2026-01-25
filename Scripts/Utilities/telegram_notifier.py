#!/usr/bin/env python3
import os
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TelegramNotifier")


def send_telegram_message(message: str, bot_token: str = None, chat_id: str = None):
    """
    Sends a message to a Telegram chat.
    If bot_token or chat_id are not provided, it tries to load them from .env
    """
    if not bot_token or not chat_id:
        root_dir = Path(__file__).resolve().parent.parent.parent
        load_dotenv(root_dir / ".env")
        bot_token = bot_token or os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = chat_id or os.getenv("TELEGRAM_ADMIN_CHAT_ID")

    if not bot_token or not chat_id:
        logger.error("Telegram credentials not found!")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            logger.info("Telegram message sent successfully")
            return True
        else:
            logger.error(f"Failed to send Telegram message: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception while sending Telegram message: {e}")
        return False


if __name__ == "__main__":
    import sys

    msg = sys.argv[1] if len(sys.argv) > 1 else "Test message from Unified System"
    send_telegram_message(msg)
