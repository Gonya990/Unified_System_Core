import os
import sys

# Add paths
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory/src")
from uploaders.telegram_uploader import upload_telegram


def upload_final():
    token = "8518131338:AAFQJFjzEIEGVd7_6ER9aKcGB5Gcylade8I"
    chat_id = "708531393"
    os.environ["TELEGRAM_BOT_TOKEN"] = token
    os.environ["TELEGRAM_ADMIN_CHAT_ID"] = chat_id

    video_ru_tg = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_RU_TG.mp4"
    video_en_tg = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_EN_TG.mp4"

    print("📱 Sending RU version to Telegram...")
    upload_telegram(
        video_path=video_ru_tg,
        caption="🎬 **Единая Система Ядро 2026 (RU)**\n\nВерсия для Telegram. Документальный фильм о будущем ИТ.\n\nYouTube (Full HD): https://youtu.be/jbIqQ5dcURA"
    )

    print("📱 Sending EN version to Telegram...")
    upload_telegram(
        video_path=video_en_tg,
        caption="🎬 **Unified System Core 2026 (EN)**\n\nTelegram Version. A documentary about the future of IT infrastructure."
    )

if __name__ == "__main__":
    upload_final()
