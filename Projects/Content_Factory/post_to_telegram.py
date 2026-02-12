import os
from pathlib import Path

import telebot
from dotenv import load_dotenv

ROOT_DIR = Path('/home/gonya/Unified_System_Core')
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

bot = telebot.TeleBot(BOT_TOKEN)
video_path = '/home/gonya/Unified_System_Core/Local_Dev/Media/legacy_wealth_v3/2026-01-31/legacy_wealth_v3_hybrid_final.mp4'

print(f'Uploading to {CHAT_ID}...')
with open(video_path, 'rb') as video:
    bot.send_video(CHAT_ID, video, caption='🚀 Стратегия Основателя 2026\n\nПочему 90% предпринимателей провалятся? #AI #Success', parse_mode='Markdown')
print('POSTED_SUCCESSFULLY')
