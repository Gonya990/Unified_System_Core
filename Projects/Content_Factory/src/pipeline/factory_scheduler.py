#!/usr/bin/env python3
import argparse
import asyncio
import json
import os
import random
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import schedule
from dotenv import load_dotenv

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()  # Projects/Content_Factory/src
FACTORY_DIR = SRC_DIR.parent  # Projects/Content_Factory
PROJECTS_DIR = FACTORY_DIR.parent  # /Projects
ROOT_DIR = PROJECTS_DIR.parent  # Unified_System (Root)

# Add all source subdirectories to path
for d in ["researcher", "pipeline", "assets", "video", "uploaders"]:
    sys.path.append(str(SRC_DIR / d))

# Add Utilities to path
sys.path.append(str(ROOT_DIR / "Scripts/Utilities"))

# Load environment before importing local modules
load_dotenv(ROOT_DIR / ".env")


from account_manager import AccountManager  # noqa: E402
from telegram_notifier import send_telegram_message  # noqa: E402
from daily_researcher import (  # noqa: E402
    generate_vision_assets,
    run_daily_research,
    translate_to_english,
    translate_to_hebrew,
)

try:
    from insta_uploader import upload_reel  # noqa: E402

    INSTA_ENABLED = True
except ImportError:
    INSTA_ENABLED = False
    print("⚠️ Instagram uploader not available")

from orchestrator_v3_no_face import run_no_face_pipeline  # noqa: E402
from threads_browser import ThreadsBrowser  # noqa: E402

# Long-form documentary producer
try:
    from longform_producer import run_longform_production

    LONGFORM_ENABLED = True
    print("✅ Long-form Documentary Producer loaded")
except ImportError:
    LONGFORM_ENABLED = False
    print("⚠️ Long-form producer not available")

# Configuration
REELS_AUTO_UPLOAD = True  # Production Mode
POSTED_HISTORY_FILE = ROOT_DIR / "posted_history.json"

# --- MONETIZATION SAFETY LIMITS (OPTIMIZED - ToS SAFE) ---
DAILY_VIDEOS_LIMIT = 3  # Optimized: 3 videos per day (quality + reach)
MIN_INTERVAL_HOURS = 4  # 4-hour gap for better algorithm treatment
INSTA_ACTION_DELAY = 90  # Seconds between Instagram operations (safer)
# YouTube: 3/day safe | Instagram: 1-2/day safe | Threads: 3/day safe
# NO TikTok - excluded by user preference
# ----------------------------------------------------------


def agent_sync(msg):
    """Синхронизация с агентом Кости (VioletCastle) через MCP и уведомление в Telegram"""
    try:
        # Sync via MCP Agent Mail
        sync_script = ROOT_DIR / "Scripts/Orchestration/sync_agent.py"
        env = os.environ.copy()
        if "AGENT_MAIL_TOKEN" not in env:
            env["AGENT_MAIL_TOKEN"] = "c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb"

        subprocess.run(["python3", str(sync_script), msg], capture_output=True, text=True, env=env)
        print(f"🔄 Agent Sync: {msg[:50]}...")

        # Also notify via Telegram
        telegram_msg = f"🏭 **Factory Status:** {msg}"
        send_telegram_message(telegram_msg)

    except Exception as e:
        print(f"⚠️ Sync/Notification Error: {e}")


def load_history():
    if POSTED_HISTORY_FILE.exists():
        try:
            with open(POSTED_HISTORY_FILE) as f:
                return json.load(f)
        except Exception:
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
    history.append({"topic": topic, "prefix": prefix, "lang": lang, "timestamp": datetime.now().isoformat()})
    # Keep history manageable
    save_history(history[-200:])


def get_static_fallback():
    """
    Emergency fallback if deep research fails.
    Improved with date-based variety.
    """
    day_str = datetime.now().strftime("%Y-%m-%d")
    topics = [
        ("AI Agents Revolution", "How autonomous agents are taking over digital tasks."),
        ("Quantum Supremacy", "The race for the first practical quantum computer."),
        ("Space Exploration 2026", "Mars colonization and the moon gateway mission."),
        ("Neural interface evolution", "Connecting human brains directly to the cloud."),
        ("Sustainable Fusion Energy", "Clean, infinite power is finally within reach."),
        ("Robotics in Everyday Life", "How machines are helping us in our homes."),
        ("The Future of Medicine", "AI-driven diagnostics and personalized treatments."),
    ]
    # Filter out already posted topics if possible
    available_topics = [t for t in topics if not is_already_posted(t[0])]
    if not available_topics:
        available_topics = topics

    topic, desc = random.choice(available_topics)

    print(f"⚠️ Using static fallback content: {topic}")
    return {
        "selected_topic": f"{topic} ({day_str})",
        "description": desc,
        "script_ru": f"Будущее наступило незаметно. Сегодня, {day_str}, мы видим... как технологии {topic.lower()} меняют правила игры. Мы больше не просто наблюдатели... мы творцы новой реальности. Это момент истины... для всего человечества.",
        "scenes": [
            {"image": f"fallback_s{i}", "keyword": kw}
            for i, kw in enumerate(
                [
                    "futuristic technology high tech",
                    "digital connection networking",
                    "cyber city night lights",
                    "abstract data visualization",
                    "innovation inspiration vision",
                    "global communication earth",
                ]
            )
        ],
    }


def generate_hebrew_content(russian_content):
    if not russian_content:
        russian_content = get_static_fallback()
    print("🇮🇱 Translating to Hebrew...")
    he_script = translate_to_hebrew(russian_content.get("script_ru", ""))
    return {
        "selected_topic": russian_content.get("selected_topic", "AI Future"),
        "script_he": he_script,
        "scenes": (russian_content.get("scenes", []) * 2)[:16],
        "description": f"מהדורת שבועית: {russian_content.get('selected_topic', '')} #AI #Israel",
    }


def generate_english_content(russian_content):
    if not russian_content:
        russian_content = get_static_fallback()
    print("🇬🇧 Translating to English...")
    en_script = translate_to_english(russian_content.get("script_ru", ""))
    return {
        "selected_topic": russian_content.get("selected_topic", "AI Future"),
        "script_en": en_script,
        "scenes": (russian_content.get("scenes", []) * 2)[:16],
        "description": f"Weekly Edition: {russian_content.get('selected_topic', '')} #AI #Future #Tech",
    }


def run_factory_production(mode="daily", manual_topic=None, manual_outline=None, style_override=None):
    day_str = datetime.now().strftime("%Y-%m-%d")

    # Auto-detect mode based on day if not specified
    if mode == "auto":
        weekday = datetime.now().weekday()
        if weekday == 6:  # Sunday
            mode = "hebrew"
        elif weekday == 2:  # Wednesday
            mode = "english"
        else:
            mode = "daily"

    print(f"🏭 RUN: {day_str} | MODE: {mode.upper()}")
    if manual_topic:
        print(f"💡 Using Manual Topic: {manual_topic}")

    # PHASE 1. RESEARCH
    agent_sync(f"🔍 Запускаю исследование (Mode: {mode})...")

    # Determine style (override > mode-based > default)
    if style_override:
        style = style_override
    else:
        style = "cartoon" if mode == "cartoon" else "impact"

    print(f"🎨 Visual Style: {style.upper()}")

    try:
        content_data = run_daily_research(style=style, manual_topic=manual_topic, manual_outline=manual_outline)

        if not content_data:
            agent_sync("Исследование не дало результатов, использую Fallback")
            content_data = get_static_fallback()

        # Uniqueness check (skip if manual topic is provided)
        topic = content_data.get("selected_topic", "")
        if not manual_topic and is_already_posted(topic):
            agent_sync(f"Тема '{topic}' уже была опубликована. Пытаюсь найти другую...")
            content_data = run_daily_research()  # Retry once
            if not content_data or is_already_posted(content_data.get("selected_topic", "")):
                content_data = get_static_fallback()  # Fallback ensures variety better now
    except Exception as e:
        agent_sync(f"Ошибка исследования: {e}")
        content_data = get_static_fallback()

    agent_sync(f"Тема выбрана: {content_data.get('selected_topic')}")

    # 2. SELECTION
    if mode == "hebrew":
        content_data = generate_hebrew_content(content_data)
        script = content_data["script_he"]
        lang = "he"
        prefix = "weekly_he"
    elif mode == "english":
        content_data = generate_english_content(content_data)
        script = content_data["script_en"]
        lang = "en"
        prefix = "weekly_en"
    elif mode == "cartoon":
        script = content_data["script_ru"]
        lang = "ru"
        prefix = "cartoon_daily"
    else:
        script = content_data["script_ru"]
        lang = "ru"
        prefix = "factory_daily"

    # 3. ASSETS
    agent_sync(f"Генерирую визуалы для {len(content_data.get('scenes', []))} сцен")
    assets_dir = ROOT_DIR / "assets" / day_str
    assets_dir.mkdir(parents=True, exist_ok=True)

    final_scenes = []
    assets = generate_vision_assets(content_data.get("scenes", []), assets_dir, style=style)
    for a in assets:
        if a.get("resolved_path"):
            final_scenes.append({"image": a["resolved_path"], "keyword": a["keyword"]})

    agent_sync(f"Ассеты готовы: {len(final_scenes)} сцен успешно скачано")

    if not final_scenes:
        print("❌ No assets. Aborting.")
        return

    # 4. PRODUCTION
    out_name = f"{prefix}_{day_str.replace('-', '')}"
    try:
        video_path = run_no_face_pipeline(
            text=script, lang=lang, output_name=out_name, scenes=final_scenes, style=style
        )

        # 5. UPLOAD (Instagram + YouTube)
        if REELS_AUTO_UPLOAD and video_path and video_path.exists():
            # 5.1 Instagram (Multi-account)
            acc_manager = AccountManager()
            insta_accounts = acc_manager.get_accounts("instagram")

            # Define caption common for all platforms
            caption = content_data.get("description", f"New AI vision: {content_data.get('selected_topic', '')}")

            if INSTA_ENABLED:
                for acc in insta_accounts:
                    agent_sync(f"Загружаю {prefix} в Instagram ({acc.get('username') or 'Account'})...")

                    try:
                        # Respect action delay
                        time.sleep(INSTA_ACTION_DELAY)
                        insta_success = upload_reel(str(video_path), caption, session_id=acc.get("session_id"))
                        if insta_success:
                            agent_sync(f"🚀 Instagram ({acc.get('username')}): Успешно!")
                        else:
                            agent_sync(f"❌ Instagram ({acc.get('username')}): Ошибка")
                    except Exception as e:
                        agent_sync(f"❌ Instagram Exception: {e}")
            else:
                agent_sync("⚠️ Пропуск Instagram (модуль отключен)")

            # 5.2 YouTube (Multi-channel)
            yt_accounts = acc_manager.get_accounts("youtube")
            for acc in yt_accounts:
                agent_sync(f"Загружаю {prefix} в YouTube ({acc.get('name') or 'Channel'})...")
                title = content_data.get("selected_topic", f"New AI Video {day_str}")
                desc_yt = f"{caption}\n\n#AI #Tech #Future #Geopolitics"
                tags = ["AI", "Future", "Tech", "News", "Geopolitics", "Megaforma"]

                try:
                    from youtube_uploader import upload_video

                    token_file = acc.get("token_file")
                    # If relative path, prefix with CREDENTIALS_DIR from uploader or use absolute
                    yt_success = upload_video(
                        video_path,
                        title=title,
                        description=desc_yt,
                        tags=tags,
                        privacy_status="public",
                        token_file=token_file,
                    )
                    if yt_success:
                        agent_sync(f"🚀 YouTube ({acc.get('name')}): Успешно!")
                    else:
                        agent_sync(f"❌ YouTube ({acc.get('name')}): Ошибка")
                except Exception as e:
                    agent_sync(f"❌ YouTube Exception: {e}")

            # 5.3 Threads (Browser Automation)
            threads_success = False
            try:
                agent_sync(f"Загружаю {prefix} в Threads (Automated)...")
                threads_bot = ThreadsBrowser(headless=True)

                # Check for saved session, otherwise skip
                # State file relative to ThreadsBrowser file
                ROOT_DIR / "Projects/Content_Factory/src/uploaders/.threads_state.json"

                # We simply run the post method. It handles login state internally if configured.
                # Since we are in sync function, we need to run async code
                threads_text = f"{content_data.get('selected_topic', '')}\n\n{content_data.get('description', '')[:450]}...\n\n#AI #Future"

                # Use asyncio.run for calling async code from sync
                threads_success = asyncio.run(threads_bot.post(threads_text, str(video_path)))

                if threads_success:
                    agent_sync("🚀 Threads: Успешно опубликован!")
                else:
                    agent_sync("⚠️ Threads: Не удалось опубликовать (Check session)")

                asyncio.run(threads_bot.close())

            except Exception as e:
                # Often async loop issues in mixed context, catch silently-ish
                print(f"Threads Error: {e}")

            if yt_success or insta_success or threads_success:
                mark_as_posted(content_data.get("selected_topic"), prefix, lang)

    except Exception as e:
        print(f"❌ Factory Crash: {e}")
        agent_sync(f"Критическая ошибка фабрики: {e}")


def start_scheduler():
    """Бесконечный цикл планировщика (OPTIMIZED - Время по Израилю UTC+2)"""
    agent_sync("⏰ Планировщик фабрики запущен (OPTIMIZED MODE - 3 видео/день)")

    # === ОПТИМИЗИРОВАННОЕ РАСПИСАНИЕ (3 видео/день) ===

    # Утро 09:00 по Израилю -> 07:00 UTC - Daily Russian (пик активности)
    schedule.every().day.at("07:00").do(run_factory_production, mode="daily")

    # День 14:00 по Израилю -> 12:00 UTC - Daily English (обеденный контент)
    schedule.every().day.at("12:00").do(run_factory_production, mode="english")

    # Вечер 20:00 по Израилю -> 18:00 UTC - Cartoon/Creative (вечерний прайм-тайм)
    schedule.every().day.at("18:00").do(run_factory_production, mode="cartoon")

    # === ЕЖЕНЕДЕЛЬНЫЕ СПЕЦИАЛЬНЫЕ ВЫПУСКИ ===

    # По воскресеньям в 10:00 по Израилю -> 08:00 UTC - Hebrew Special
    schedule.every().sunday.at("08:00").do(run_factory_production, mode="hebrew")

    # По субботам в 18:00 по Израилю -> 16:00 UTC - 30-MIN DOCUMENTARY
    if LONGFORM_ENABLED:
        schedule.every().saturday.at("16:00").do(run_longform_production)
        print("🎬 Long-form Documentary: Saturday 18:00 Israel Time")

    print("🚀 OPTIMIZED Scheduler running (3 videos/day + Weekly Documentary). Waiting...")
    print("📅 Daily: 09:00 RU | 14:00 EN | 20:00 Cartoon")
    # Priority: Brand > Context > News
    modes = ["brand"] * 3 + ["context"] * 2 + ["auto"]
    
    while True:
        mode = random.choice(modes)
        print(f"🚀 Starting cycle: {mode}")
        
        try:
            if mode == "brand":
                run_brand_pipeline()
            elif mode == "context":
                run_context_pipeline()
            else:
                run_daily_cycle()
        except Exception as e:
            print(f"❌ Cycle failed: {e}")
            
        time.sleep(300) # 5 min pause


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Content Farm Scheduler")
    parser.add_argument("--hebrew", action="store_true", help="Force Hebrew weekly special")
    parser.add_argument("--english", action="store_true", help="Force English weekly special")
    parser.add_argument("--cartoon", action="store_true", help="Force Cartoon/Animation daily mode")
    parser.add_argument("--auto", action="store_true", help="Detect mode based on day")
    parser.add_argument("--scheduler", action="store_true", help="Run in infinity loop mode")
    parser.add_argument("--longform", action="store_true", help="Force 30-min Documentary mode")
    parser.add_argument("--longform-topic", type=str, help="Topic for documentary")

    parser.add_argument("--auto-upload", action="store_true", help="Force enable auto upload")
    parser.add_argument(
        "--style", type=str, choices=["impact", "cartoon", "sketch", "painting"], help="Force visual style"
    )
    parser.add_argument("--inspiration-topic", type=str, help="Manually provided topic from YouTube Inspiration Tab")
    parser.add_argument(
        "--inspiration-outline", type=str, help="Manually provided outline from YouTube Inspiration Tab"
    )

    args = parser.parse_args()

    # Allow CLI override for upload
    if args.auto_upload:
        REELS_AUTO_UPLOAD = True

    if args.scheduler:
        start_scheduler()
    elif args.longform:
        if LONGFORM_ENABLED:
            run_longform_production(args.longform_topic)
        else:
            print("❌ Long-form producer not available")
    else:
        mode = "daily"
        if args.hebrew:
            mode = "hebrew"
        elif args.english:
            mode = "english"
        elif args.cartoon:
            mode = "cartoon"
        elif args.auto:
            mode = "auto"

        run_factory_production(
            mode=mode,
            manual_topic=args.inspiration_topic,
            manual_outline=args.inspiration_outline,
            style_override=args.style,
        )
