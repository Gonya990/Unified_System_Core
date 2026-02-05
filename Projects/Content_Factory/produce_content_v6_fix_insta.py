import sys
import os
import datetime
import telebot
import subprocess
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SRC_DIR = Path('/home/gonya/Unified_System_Core/Projects/Content_Factory/src')
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(SRC_DIR / 'pipeline'))
sys.path.insert(0, str(SRC_DIR / 'uploaders'))

try:
    import insta_uploader_v2
except ImportError as e:
    print(f"Warning: {e}")

load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

def convert_for_instagram(input_path: Path) -> Path:
    output_path = input_path.parent / (input_path.stem + "_insta_ready.mp4")
    print(f"Converting: {input_path}")
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-maxrate", "8M", 
        "-bufsize", "16M",
        "-profile:v", "high",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-r", "30",
        "-movflags", "+faststart",
        str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Conversion Complete""")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Conversion Failed: {e}")
        return None

def run():
    print("CONTENT FACTORY V6: INSTAGRAM REPAIR")
    
    day_str = datetime.datetime.now().strftime('%Y-%m-%d')
    assets_dir = ROOT_DIR / 'Local_Dev' / 'Media' / 'daily_auto' / day_str
    existing_video = assets_dir / "daily_infinite_game_final.mp4"
    
    caption_full = """♾️ **Бесконечная Игра 2026**

Бизнес — это не спринт. Победит тот, кто останется в игре, когда остальные выгорят.

Пока конкуренты ищут мотивацию, Agentic AI ищет возможности. 24/7.

#Business2026 #AI #UnifiedSystem #Strategy #Wealth"""

    if existing_video.exists():
        print(f"Found video: {existing_video}")
        insta_video = convert_for_instagram(existing_video)
        
        if insta_video and insta_video.exists():
            print("Retrying Instagram Upload...")
            try:
                insta_uploader_v2.upload_reel(insta_video, caption_full)
            except Exception as e:
                print(f"Instagram Error: {e}")
    else:
        print("Video file not found.")

if __name__ == '__main__':
    run()
