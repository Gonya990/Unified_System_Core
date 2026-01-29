import argparse
import html
import json
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
# Use override=True to ensure configuration from file wins over shell env
load_dotenv(ROOT_DIR / ".env", override=True)
load_dotenv(ROOT_DIR / "LLM_Council/.env", override=True)

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
        "parse_mode": "HTML",
        "disable_notification": silent,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"❌ Failed to send Telegram report: {e}")
        # Print the response body if available for debugging
        if hasattr(e, "response") and e.response is not None:
            print(f"DEBUG: {e.response.text}")
        return False


def report_production_start(topic: str):
    safe_topic = html.escape(topic)
    msg = (
        f"🚀 <b>ADF Production Started</b>\n\n"
        f"📌 <b>Topic:</b> {safe_topic}\n"
        f"🛠 <b>Phase:</b> Planning & Research\n"
        f"🤖 <b>Model:</b> NVIDIA NIM (Chairman)"
    )
    return send_telegram_report(msg)


def report_phase_complete(phase: str, details: str = ""):
    safe_phase = html.escape(phase)
    safe_details = html.escape(details)
    msg = f"✅ <b>Phase Complete: {safe_phase}</b>\n\n{safe_details}"
    return send_telegram_report(msg)


def report_production_error(error: str):
    safe_error = html.escape(error)
    msg = f"⚠️ <b>ADF Production Alert</b>\n\n❌ <b>Error:</b> {safe_error}"
    return send_telegram_report(msg)


def report_recent_production():
    """Scan outputs and send a summary of recent ADF activity."""
    outputs_dir = ROOT_DIR / "outputs"
    if not outputs_dir.exists():
        return send_telegram_report("📂 <b>ADF Report:</b> No outputs directory found.")

    # 1. Check for today's documentary
    today_str = datetime.now().strftime("%Y-%m-%d")
    doc_dir = outputs_dir / f"documentary_{today_str}"
    doc_msg = ""
    if doc_dir.exists():
        data_file = doc_dir / "documentary_data.json"
        if data_file.exists():
            try:
                with open(data_file) as f:
                    data = json.load(f)
                    title = html.escape(data.get("title", "Untitled Documentary"))
                    doc_msg = (
                        f"🎬 <b>New Documentary:</b> {title}\n"
                        f"📦 <b>Path:</b> <code>{html.escape(doc_dir.name)}/</code>\n\n"
                    )
            except Exception as e:
                print(f"Warning: Failed to parse documentary data: {e}")

    # 2. Check for recent MP4s in root outputs
    recent_videos = []
    for f in outputs_dir.glob("*.mp4"):
        # Get files from last 48 hours
        if (datetime.now().timestamp() - f.stat().st_mtime) < 172800:
            if "_final.mp4" in f.name:
                recent_videos.append(f.name)

    video_list = (
        "\n".join([f"• 📹 <code>{html.escape(v)}</code>" for v in recent_videos])
        if recent_videos
        else "• <i>No recent videos found.</i>"
    )

    msg = (
        f"🏭 <b>Content Factory: Production Summary</b>\n"
        f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"{doc_msg}"
        f"<b>Recent Generations (48h):</b>\n"
        f"{video_list}\n\n"
        f"✨ <i>All systems nominal. Ready for next cycle.</i>"
    )
    return send_telegram_report(msg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ADF Telegram Reporter")
    parser.add_argument("--test", action="store_true", help="Send a test message")
    parser.add_argument("--recent", action="store_true", help="Send recent production summary")
    parser.add_argument("--msg", help="Send a custom message")
    args = parser.parse_args()

    if args.test:
        print("🧪 Testing Telegram Reporter...")
        send_telegram_report("🤖 <b>ADF Launch System:</b> Online & Synchronized")
    elif args.recent:
        print("📊 Sending recent production summary...")
        report_recent_production()
    elif args.msg:
        send_telegram_report(html.escape(args.msg))
    else:
        # Default behavior: send test
        report_recent_production()
