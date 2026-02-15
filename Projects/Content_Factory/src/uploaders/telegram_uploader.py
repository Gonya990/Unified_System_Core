import os

import telebot


def upload_telegram(video_path: str, caption: str) -> bool:
    """Upload video to Telegram channel"""

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

    if not bot_token or not chat_id:
        print("❌ Telegram credentials missing")
        return False

    try:
        bot = telebot.TeleBot(bot_token)

        with open(video_path, "rb") as video:
            bot.send_video(chat_id, video, caption=caption)

        print(f"✅ Posted to Telegram: {chat_id}")
        return True
    except Exception as e:
        print(f"❌ Telegram upload failed: {e}")
        return False
