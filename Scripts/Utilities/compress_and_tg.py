import os
import subprocess
import sys

# Paths
VENV_PYTHON = "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/.venv/bin/python"
VIDEO_EN = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_EN.mp4"
VIDEO_RU = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_RU.mp4"
VIDEO_EN_TG = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_EN_TG.mp4"
VIDEO_RU_TG = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_2026_RU_TG.mp4"

def compress_and_upload():
    # 1. Compress RU
    print("🎬 Compressing RU video for Telegram...")
    subprocess.run([
        "ffmpeg", "-y", "-i", VIDEO_RU, 
        "-vcodec", "libx264", "-crf", "28", 
        "-acodec", "aac", "-b:a", "128k", 
        VIDEO_RU_TG
    ], check=True)
    
    # 2. Compress EN
    print("🎬 Compressing EN video for Telegram...")
    subprocess.run([
        "ffmpeg", "-y", "-i", VIDEO_EN, 
        "-vcodec", "libx264", "-crf", "28", 
        "-acodec", "aac", "-b:a", "128k", 
        VIDEO_EN_TG
    ], check=True)
    
    # 3. Upload using existing script (modified to use TG versions)
    print("📱 Uploading to Telegram...")
    # I'll just call the upload_telegram function directly in another script or modify publish_doc_v2
    
    # Trigger the upload script with the new paths
    # I'll just use manual code here to be quick
    sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory/src")
    from uploaders.telegram_uploader import upload_telegram
    
    token = "8518131338:AAFQJFjzEIEGVd7_6ER9aKcGB5Gcylade8I"
    os.environ["TELEGRAM_BOT_TOKEN"] = token
    
    print("📱 Sending RU...")
    upload_telegram(video_path=VIDEO_RU_TG, caption="🎬 Документальный фильм (RU) - Версия для Telegram")
    
    print("📱 Sending EN...")
    upload_telegram(video_path=VIDEO_EN_TG, caption="🎬 Documentary (EN) - Telegram Version")

if __name__ == "__main__":
    compress_and_upload()
