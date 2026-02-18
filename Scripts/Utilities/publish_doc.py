import os
import sys
from pathlib import Path

# Add paths for dependencies
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory/src")
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")

from token_broker import TokenBroker
from uploaders.telegram_uploader import upload_telegram
from uploaders.youtube_uploader import upload_video


def publish_documentary():
    # 1. Get tokens
    broker = TokenBroker()
    tg_token = broker.get_key("telegram")
    # Set env vars for the uploaders
    os.environ["TELEGRAM_BOT_TOKEN"] = tg_token
    os.environ["TELEGRAM_ADMIN_CHAT_ID"] = "708531393" # From .env

    video_en = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_EN.mp4"
    video_ru = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_RU.mp4"

    print("🚀 Publishing documentaries...")

    # 2. Upload RU to YouTube (as requested)
    print("📺 Uploading Russian version to YouTube...")
    ru_desc = """Единая Система Ядро (2026) — Документальный фильм о будущем ИТ-инфраструктуры.
Архитектура (GKE/Proxmox), Совет ИИ, Безопасность Вибраниум и финансовая свобода с Bybit.
Создано полностью с помощью ИИ конвейера."""

    youtube_success = upload_video(
        file_path=Path(video_ru),
        title="Единая Система Ядро (2026): Будущее началось",
        description=ru_desc,
        tags=["AI", "GKE", "Proxmox", "Security", "Crypto", "Bybit", "Documentary"],
        privacy_status="unlisted" # Keep unlisted for now until user reviews
    )

    # 3. Send RU to Telegram (as requested)
    print("📱 Sending Russian version to Telegram...")
    tg_success = upload_telegram(
        video_path=video_ru,
        caption="🎬 Твой документальный фильм готов (RU)! \n\nЕдиная Система Ядро 2026. Будущее ИТ уже здесь."
    )

    if youtube_success and tg_success:
        print("✅ All publishing tasks completed successfully!")
    else:
        print(f"⚠️ Partial success. YouTube: {youtube_success}, Telegram: {tg_success}")

if __name__ == "__main__":
    publish_documentary()
