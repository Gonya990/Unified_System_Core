import os
import sys
import argparse
from pathlib import Path

# Add paths for dependencies
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory/src")
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")

from uploaders.youtube_uploader import upload_video
from uploaders.telegram_uploader import upload_telegram

def publish_documentary():
    # 1. Credentials (using the ones found in GCP Secret Manager/Env)
    tg_token = "8518131338:AAFQJFjzEIEGVd7_6ER9aKcGB5Gcylade8I"
    admin_chat_id = "708531393"
    
    # Set env vars for the uploaders
    os.environ["TELEGRAM_BOT_TOKEN"] = tg_token
    os.environ["TELEGRAM_ADMIN_CHAT_ID"] = admin_chat_id
    
    video_en = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_EN.mp4"
    video_ru = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_RU.mp4"
    
    print("🚀 Publishing documentaries...")
    
    # 2. Send to Telegram (Immediate result for user)
    print("📱 Sending Russian version to Telegram...")
    tg_success_ru = upload_telegram(
        video_path=video_ru,
        caption="🎬 Твой документальный фильм готов (RU)! \n\nЕдиная Система Ядро 2026. Будущее ИТ уже здесь."
    )
    
    print("📱 Sending English version to Telegram...")
    tg_success_en = upload_telegram(
        video_path=video_en,
        caption="🎬 Your documentary is ready (EN)! \n\nUnified System Core 2026. The future of IT infrastructure."
    )
    
    # 3. Upload RU to YouTube
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
    
    if youtube_success and tg_success_ru:
        print("✅ All publishing tasks completed successfully!")
    else:
        print(f"⚠️ Partial success. YouTube: {youtube_success}, Telegram RU: {tg_success_ru}, TG EN: {tg_success_en}")

if __name__ == "__main__":
    publish_documentary()
