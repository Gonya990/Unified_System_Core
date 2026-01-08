#!/usr/bin/env python3
import os
import sys
import random
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

# Load environment before importing local modules
load_dotenv(ROOT_DIR / ".env")

from orchestrator_v3_no_face import run_no_face_pipeline, OUTPUT_DIR
from daily_researcher import run_daily_research, generate_vision_assets, translate_to_hebrew
from insta_uploader import upload_reel
import subprocess

def agent_sync(msg):
    """Синхронизация с агентом Кости (FuchsiaCat) через MCP"""
    try:
        subprocess.run(["python3", "sync_agent.py", msg], capture_output=True, text=True)
        print(f"🔄 Agent Sync: {msg[:50]}...")
    except Exception as e:
        print(f"⚠️ Sync Error: {e}")

# Configuration
REELS_AUTO_UPLOAD = True

def get_static_fallback():
    """
    Emergency fallback if deep research fails. 
    Improved with date-based variety.
    """
    day_str = datetime.now().strftime('%Y-%m-%d')
    topics = [
        ("AI Agents Revolution", "How autonomous agents are taking over digital tasks."),
        ("Quantum Supremacy", "The race for the first practical quantum computer."),
        ("Space Exploration 2026", "Mars colonization and the moon gateway mission."),
        ("Neural interface evolution", "Connecting human brains directly to the cloud."),
        ("Sustainable Fusion Energy", "Clean, infinite power is finally within reach.")
    ]
    topic, desc = random.choice(topics)
    
    print(f"⚠️ Using static fallback content: {topic}")
    return {
        "selected_topic": f"{topic} ({day_str})",
        "description": desc,
        "script_ru": f"Будущее наступило незаметно. Сегодня, {day_str}, мы видим... как технологии {topic.lower()} меняют правила игры. Мы больше не просто наблюдатели... мы творцы новой реальности. Это момент истины... для всего человечества.",
        "scenes": [
            {"image": f"fallback_s{i}", "keyword": kw} for i, kw in enumerate([
                "futuristic technology high tech", "digital connection networking", 
                "cyber city night lights", "abstract data visualization",
                "innovation inspiration vision", "global communication earth"
            ])
        ]
    }

def generate_hebrew_content(russian_content):
    """
    HEBREW WEEKLY LOGIC
    """
    if not russian_content:
        russian_content = get_static_fallback()
        
    print("🇮🇱 Translating to Hebrew...")
    he_script = translate_to_hebrew(russian_content.get('script_ru', ""))
    
    return {
        "selected_topic": russian_content.get('selected_topic', "AI Future"),
        "script_he": he_script,
        "scenes": (russian_content.get('scenes', []) * 2)[:16],
        "description": f"מהדורת שבועית: {russian_content.get('selected_topic', '')} #AI #Israel"
    }

def run_factory_production(is_weekly=False):
    day_str = datetime.now().strftime('%Y-%m-%d')
    is_weekly_hebrew = is_weekly or (datetime.now().weekday() == 6)

    print(f"🏭 RUN: {day_str} {'(HEBREW)' if is_weekly_hebrew else ''}")
    
    # PHASE 1: DAILY RESEARCH
    agent_sync(f"Начинаю фазу исследования для {'еженедельного иврита' if is_weekly_hebrew else 'ежедневного ролика'}")
    try:
        content_data = run_daily_research()
        if not content_data:
            agent_sync("Исследование не дало результатов, использую Fallback")
            content_data = get_static_fallback()
    except Exception as e:
        agent_sync(f"Ошибка исследования: {e}")
        content_data = get_static_fallback()

    agent_sync(f"Тема выбрана: {content_data.get('selected_topic')}")

    # 2. SELECTION
    if is_weekly_hebrew:
        content_data = generate_hebrew_content(content_data)
        script = content_data['script_he']
        lang = "he"
        prefix = "weekly_he"
    else:
        script = content_data['script_ru']
        lang = "ru"
        prefix = "factory_daily"

    # 3. ASSETS
    agent_sync(f"Генерирую визуалы для {len(content_data.get('scenes', []))} сцен")
    assets_dir = ROOT_DIR / "assets" / day_str
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    final_scenes = []
    assets = generate_vision_assets(content_data.get('scenes', []), assets_dir)
    for a in assets:
        if a.get('resolved_path'):
            final_scenes.append({"image": a['resolved_path'], "keyword": a['keyword']})
            
    agent_sync(f"Ассеты готовы: {len(final_scenes)} сцен успешно скачано")
            
    if not final_scenes:
        print("❌ No assets. Aborting.")
        return

    # 4. PRODUCTION
    out_name = f"{prefix}_{day_str.replace('-', '')}"
    try:
        video_path = run_no_face_pipeline(text=script, lang=lang, output_name=out_name, scenes=final_scenes)
        
        # 5. UPLOAD (NEW)
        if REELS_AUTO_UPLOAD and video_path and video_path.exists():
            agent_sync(f"Загружаю {prefix} ролик в Instagram...")
            caption = content_data.get('description', f"New AI vision: {content_data.get('selected_topic', '')}")
            if upload_reel(str(video_path), caption):
                agent_sync("🚀 Ролик успешно загружен!")
            else:
                agent_sync("❌ Ошибка при загрузке ролика")
                
    except Exception as e:
        print(f"❌ Factory Crash: {e}")
        agent_sync(f"Критическая ошибка фабрики: {e}")

if __name__ == "__main__":
    run_factory_production()
