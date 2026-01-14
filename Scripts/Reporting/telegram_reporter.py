import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
load_dotenv(ROOT_DIR / "LLM_Council/.env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")


def send_telegram_report(message: str, silent: bool = False):
    """Send a status report to the Admin Telegram chat."""
    if not BOT_TOKEN or not CHAT_ID:
        print("⚠️ Telegram Config Missing (BOT_TOKEN or CHAT_ID)")
        return False

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_notification": silent,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to send Telegram report: {e}")
        return False


def report_production_start(topic: str):
    msg = f"🚀 *ADF Production Started*\n\n📌 *Topic:* {topic}\n🛠 *Phase:* Planning & Research\n🤖 *Model:* NVIDIA NIM (Chairman)"
    return send_telegram_report(msg)


def report_phase_complete(phase: str, details: str = ""):
    msg = f"✅ *Phase Complete: {phase}*\n\n{details}"
    return send_telegram_report(msg)


def report_production_error(error: str):
    msg = f"⚠️ *ADF Production Alert*\n\n❌ *Error:* {error}"
    return send_telegram_report(msg)


if __name__ == "__main__":
    # Test
    print("🧪 Testing Telegram Reporter...")
    success = send_telegram_report("🤖 *ADF Launch System:* Online & Synchronized")
    if success:
        print("✅ Test message sent!")
    else:
        print("❌ Test failed.")
