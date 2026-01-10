#!/usr/bin/env python3
import os
import sys
import random
import json
import argparse
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()
FACTORY_DIR = SRC_DIR.parent
ROOT_DIR = FACTORY_DIR.parent # Unified_System

# Add all source subdirectories to path
for d in ["researcher", "pipeline", "assets", "video", "uploaders"]:
    sys.path.append(str(SRC_DIR / d))

# Load environment before importing local modules
load_dotenv(ROOT_DIR / ".env")

from orchestrator_v3_no_face import run_no_face_pipeline, OUTPUT_DIR
from daily_researcher import run_daily_research, generate_vision_assets, translate_to_hebrew, translate_to_english
from insta_uploader import upload_reel
import subprocess

# Configuration
REELS_AUTO_UPLOAD = True  # Production Mode
POSTED_HISTORY_FILE = ROOT_DIR / "posted_history.json"

def agent_sync(msg):
    """Синхронизация с агентом Кости (FuchsiaCat) через MCP"""
    try:
        subprocess.run(["python3", "sync_agent.py", msg], capture_output=True, text=True)
        print(f"🔄 Agent Sync: {msg[:50]}...")
    except Exception as e:
        print(f"⚠️ Sync Error: {e}")

def load_history():
    if POSTED_HISTORY_FILE.exists():
        try:
            with open(POSTED_HISTORY_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(POSTED_HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def is_already_posted(topic):
    history = load_history()
    # Check if topic was posted in the last 30 entries to avoid near-duplicates
    posted_topics = [item.get("topic") for item in history[-30:]]
    return topic in posted_topics

def mark_as_posted(topic, prefix, lang):
    history = load_history()
    history.append({
        "topic": topic,
        "prefix": prefix,
        "lang": lang,
        "timestamp": datetime.now().isoformat()
    })
    # Keep history manageable
    save_history(history[-200:])

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
        ("Sustainable Fusion Energy", "Clean, infinite power is finally within reach."),
        ("Robotics in Everyday Life", "How machines are helping us in our homes."),
        ("The Future of Medicine", "AI-driven diagnostics and personalized treatments.")
    ]
    # Filter out already posted topics if possible
    available_topics = [t for t in topics if not is_already_posted(t[0])]
    if not available_topics: available_topics = topics
    
    topic, desc = random.choice(available_topics)
    
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

def generate_english_content(russian_content):
    if not russian_content:
        russian_content = get_static_fallback()
    print("🇬🇧 Translating to English...")
    en_script = translate_to_english(russian_content.get('script_ru', ""))
    return {
        "selected_topic": russian_content.get('selected_topic', "AI Future"),
        "script_en": en_script,
        "scenes": (russian_content.get('scenes', []) * 2)[:16],
        "description": f"Weekly Edition: {russian_content.get('selected_topic', '')} #AI #Future #Tech"
    }

def run_factory_production(mode="daily"):
    day_str = datetime.now().strftime('%Y-%m-%d')
    
    # Auto-detect mode based on day if not specified
    if mode == "auto":
        weekday = datetime.now().weekday()
        if weekday == 6: # Sunday
            mode = "hebrew"
        elif weekday == 2: # Wednesday
            mode = "english"
        else:
            mode = "daily"

    print(f"🏭 RUN: {day_str} | MODE: {mode.upper()}")
    
    # PHASE 1. RESEARCH
    agent_sync(f"🔍 Запускаю исследование (Mode: {mode})...")
    
    style = "cartoon" if mode == "cartoon" else "impact"
    
    try:
        content_data = run_daily_research(style=style)
        if not content_data:
            agent_sync("Исследование не дало результатов, использую Fallback")
            content_data = get_static_fallback()
            
        # Uniqueness check
        topic = content_data.get('selected_topic', '')
        if is_already_posted(topic):
            agent_sync(f"Тема '{topic}' уже была опубликована. Пытаюсь найти другую...")
            content_data = run_daily_research() # Retry once
            if not content_data or is_already_posted(content_data.get('selected_topic', '')):
                content_data = get_static_fallback() # Fallback ensures variety better now
    except Exception as e:
        agent_sync(f"Ошибка исследования: {e}")
        content_data = get_static_fallback()

    agent_sync(f"Тема выбрана: {content_data.get('selected_topic')}")

    # 2. SELECTION
    if mode == "hebrew":
        content_data = generate_hebrew_content(content_data)
        script = content_data['script_he']
        lang = "he"
        prefix = "weekly_he"
    elif mode == "english":
        content_data = generate_english_content(content_data)
        script = content_data['script_en']
        lang = "en"
        prefix = "weekly_en"
    elif mode == "cartoon":
        script = content_data['script_ru']
        lang = "ru"
        prefix = "cartoon_daily"
    else:
        script = content_data['script_ru']
        lang = "ru"
        prefix = "factory_daily"

    # 3. ASSETS
    agent_sync(f"Генерирую визуалы для {len(content_data.get('scenes', []))} сцен")
    assets_dir = ROOT_DIR / "assets" / day_str
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    final_scenes = []
    assets = generate_vision_assets(content_data.get('scenes', []), assets_dir, style=style)
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
        video_path = run_no_face_pipeline(text=script, lang=lang, output_name=out_name, scenes=final_scenes, style=style)
        
        # 5. UPLOAD
        if REELS_AUTO_UPLOAD and video_path and video_path.exists():
            agent_sync(f"Загружаю {prefix} ролик в Instagram...")
            caption = content_data.get('description', f"New AI vision: {content_data.get('selected_topic', '')}")
            if upload_reel(str(video_path), caption):
                agent_sync("🚀 Ролик успешно загружен!")
                mark_as_posted(content_data.get('selected_topic'), prefix, lang)
            else:
                agent_sync("❌ Ошибка при загрузке ролика")
                
    except Exception as e:
        print(f"❌ Factory Crash: {e}")
        agent_sync(f"Критическая ошибка фабрики: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Content Farm Scheduler')
    parser.add_argument('--hebrew', action='store_true', help='Force Hebrew weekly special')
    parser.add_argument('--english', action='store_true', help='Force English weekly special')
    parser.add_argument('--cartoon', action='store_true', help='Force Cartoon/Animation daily mode')
    parser.add_argument('--auto', action='store_true', help='Detect mode based on day')
    
    parser.add_argument('--auto-upload', action='store_true', help='Force enable auto upload')
    
    args = parser.parse_args()
    
    # Allow CLI override for upload
    if args.auto_upload:
        REELS_AUTO_UPLOAD = True

    mode = "daily"
    if args.hebrew: mode = "hebrew"
    elif args.english: mode = "english"
    elif args.cartoon: mode = "cartoon"
    elif args.auto: mode = "auto"
    
    run_factory_production(mode=mode)
