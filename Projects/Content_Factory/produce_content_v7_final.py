#!/usr/bin/env python3
import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path('/home/gonya/Unified_System_Core')
FACTORY_DIR = ROOT_DIR / 'Projects/Content_Factory'
MEDIA_DIR = ROOT_DIR / 'Local_Dev/Media/daily_auto'

sys.path.insert(0, str(FACTORY_DIR / 'src'))

from pipeline.orchestrator_v3_no_face import run_no_face_pipeline
from uploaders.youtube_uploader import upload_video
from uploaders.telegram_uploader import upload_telegram
from audio.music_generator import MusicGenerator
from video.ai_video_generator import VideoGenerator

# Initialize AI tools
music_gen = MusicGenerator(use_ai=True)
video_gen = VideoGenerator(provider="runway")  # Fallback to runway as Luma is in beta
from pipeline.add_ai_watermark import add_ai_watermark
from pipeline.vibranium_creativity import generate_dynamic_content

from dotenv import load_dotenv
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

def notify_manual_upload(video_path: Path, caption: str):
    try:
        import telebot
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        admin_chat_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
        if bot_token and admin_chat_id:
            bot = telebot.TeleBot(bot_token)
            bot.send_message(admin_chat_id, f'🎬 **IG/FB Manual Upload**\n\n{caption}', parse_mode='Markdown')
            with open(video_path, 'rb') as video:
                bot.send_video(admin_chat_id, video)
    except Exception as e:
        print(f'⚠️ Notify error: {e}')

def main():
    print('🎨 Generating VIBRANIUM Content...')
    try:
        content = generate_dynamic_content()
        script_ru = content['script_ru']
        scenes = content['scenes']
        caption = content['instagram_caption']
        title = content['title']
    except Exception as e:
        print(f'❌ Creative Failed: {e}')
        return

    today = datetime.now().strftime('%Y-%m-%d')
    output_dir = MEDIA_DIR / today
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = str(int(time.time()))
    base_name = f'vibranium_{timestamp}'
    
    success = run_no_face_pipeline(script_ru, lang='ru', output_name=str(output_dir / base_name), scenes=scenes)
    
    if success:
        temp_video = output_dir / f'{base_name}_final.mp4'
        final_video = output_dir / f'{base_name}_final_ai.mp4'
        add_ai_watermark(temp_video, final_video)
        
        upload_telegram(str(final_video), caption)
        upload_video(final_video, title, caption, tags=['AI', 'Future'], privacy_status='public')
        notify_manual_upload(final_video, caption)
        print(f'✅ Production Complete: {final_video}')

if __name__ == '__main__':
    main()
