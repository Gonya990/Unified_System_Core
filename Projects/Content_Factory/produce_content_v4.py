import datetime
import os
import sys
from pathlib import Path

import telebot
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SRC_DIR = Path('/home/gonya/Unified_System_Core/Projects/Content_Factory/src')
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(SRC_DIR / 'pipeline'))

import orchestrator_v3_no_face as orchestrator

load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

def upload_telegram(video_path, caption):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    if not token or not chat_id:
        print("❌ Telegram credentials missing")
        return

    print(f"📤 Posting to Telegram {chat_id}...")
    try:
        bot = telebot.TeleBot(token)
        with open(video_path, 'rb') as v:
            bot.send_video(chat_id, v, caption=caption, parse_mode='Markdown')
        print("✅ Posted to Telegram")
    except Exception as e:
        print(f"❌ Telegram Upload Error: {e}")

def run():
    print("🏭 CONTENT FACTORY V4: ACTIVE")

    # Simple logic: Generate 1 video now to prove loop works
    # Using 'The Infinite Game' topic as next step

    day_str = datetime.datetime.now().strftime('%Y-%m-%d')
    assets_dir = ROOT_DIR / 'Local_Dev' / 'Media' / 'daily_auto' / day_str
    assets_dir.mkdir(parents=True, exist_ok=True)

    script_ru = """
Бизнес - это не спринт. Это бесконечная игра. ♾️

В две тысячи двадцать шестом году победит не тот, кто быстрее. А тот, кто дольше останется в игре. 🏃‍♂️💨

Саймон Синек говорил об этом. Но ИИ изменил правила. Теперь ваша выносливость - это мощность ваших серверов. 💻

Ваша команда не спит, не ест и не выгорает. Потому что это агентная сеть Unified Core. 🤖

Пока конкуренты ищут мотивацию, ваша система ищет возможности. 24 на 7.

Перестаньте играть ради победы в квартале. Играйте, чтобы остаться в игре навсегда. 🏆

Unified System Core. Архитектура вашего бессмертия.
"""

    # We use Pexels + AI Hybrid
    # Since we can't reliably get Pexels key if env is messy, we fallback to AI only if needed,
    # but we saved Pexels key earlier so it should work.

    scenes = [
         {'image': 'scene_infinite_1', 'keyword': 'marathon runner silhouette sunrise epic slow motion'},
         {'image': 'scene_infinite_2', 'keyword': 'futuristic server room data stream endless'},
         {'image': 'scene_infinite_3', 'keyword': 'simon sinek style lecture ted talk silhouette'},
         {'image': 'scene_infinite_4', 'keyword': 'digital brain neural network glowing infinite loop'},
         {'image': 'scene_infinite_5', 'keyword': 'business man looking at horizon city future timeline'},
         {'image': 'scene_infinite_6', 'keyword': 'immortal digital construct geometric abstract'}
    ]

    orchestrator.INPUT_DIR = assets_dir
    orchestrator.OUTPUT_DIR = assets_dir
    orchestrator.BROLL_DIR = ROOT_DIR / 'broll'

    # Ensure Pexels key matches what we found
    os.environ['PEXELS_API_KEY'] = "5KikfJFyT75Rlibf2u829q4qZOTm0FVfttKCb5znbJSYqb96qAKarEDY"

    print("🚀 Generating Daily Content: 'The Infinite Game'...")

    # Call Orchestrator (Assuming it handles asset gen internally or we mocked it)
    # Actually Orchestrator V3 usually expects assets to exist.
    # We will generate them quickly via DALL-E wrapper if missing.

    from daily_researcher import generate_vision_assets
    generate_vision_assets(scenes, assets_dir, style="cinematic_impact")

    final_video = orchestrator.run_no_face_pipeline(
        text=script_ru,
        lang="ru",
        scenes=scenes,
        output_name="daily_infinite_game",
        style="impact"
    )

    if final_video:
        print(f"✅ Video Ready: {final_video}")
        if os.getenv('AUTO_POST_TELEGRAM') == 'True':
            upload_telegram(final_video, "♾️ **Бесконечная Игра 2026**\n\n#UnifiedCore #AI #BusinessStrategy")
    else:
        print("❌ Generation Failed")

if __name__ == '__main__':
    run()
