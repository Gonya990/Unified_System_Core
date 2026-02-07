import os
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Add src to path (must be before internal imports)
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
FACTORY_DIR = ROOT_DIR / 'Projects/Content_Factory'
MEDIA_DIR = ROOT_DIR / 'Local_Dev/Media/daily_auto'

sys.path.insert(0, str(FACTORY_DIR / 'src'))

from audio.music_generator import MusicGenerator  # noqa: E402
from pipeline.add_ai_watermark import add_ai_watermark  # noqa: E402
from pipeline.orchestrator_v3_no_face import run_no_face_pipeline  # noqa: E402
from pipeline.vibranium_creativity import generate_dynamic_content  # noqa: E402
from uploaders.telegram_uploader import upload_telegram  # noqa: E402
from uploaders.youtube_uploader import upload_video  # noqa: E402
from video.ai_video_generator import VideoGenerator  # noqa: E402

load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

# Initialize AI tools
music_gen = MusicGenerator(use_ai=True)
# Fallback to runway as Luma is in beta
video_gen = VideoGenerator(provider="runway")

def notify_manual_upload(video_path: Path, caption: str):
    try:
        import telebot
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        admin_chat_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
        if bot_token and admin_chat_id:
            bot = telebot.TeleBot(bot_token)
            msg = f'🎬 **IG/FB Manual Upload**\n\n{caption}'
            bot.send_message(admin_chat_id, msg, parse_mode='Markdown')
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
    
    output_path = str(output_dir / base_name)
    success = run_no_face_pipeline(
        script_ru, lang='ru', output_name=output_path, scenes=scenes
    )
    
    if success:
        temp_video = output_dir / f'{base_name}_final.mp4'
        final_video = output_dir / f'{base_name}_final_ai.mp4'
        add_ai_watermark(temp_video, final_video)
        
        upload_telegram(str(final_video), caption)
        upload_video(
            final_video, title, caption, tags=['AI', 'Future'], privacy_status='public'
        )
        notify_manual_upload(final_video, caption)
        print(f'✅ Production Complete: {final_video}')

if __name__ == '__main__':
    main()
