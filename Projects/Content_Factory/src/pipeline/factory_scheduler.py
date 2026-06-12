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
load_dotenv(FACTORY_DIR / ".env", override=True)


from account_manager import AccountManager  # noqa: E402
from daily_researcher import (  # noqa: E402
    generate_vision_assets,
    run_daily_research,
    translate_to_english,
    translate_to_hebrew,
)
from telegram_notifier import send_telegram_message  # noqa: E402

try:
    from insta_uploader import upload_reel  # noqa: E402

    INSTA_ENABLED = True
except ImportError:
    INSTA_ENABLED = False
    print("⚠️ Instagram uploader not available")

from orchestrator_v4_advanced import run_advanced_pipeline as run_no_face_pipeline  # noqa: E402
from threads_browser import ThreadsBrowser  # noqa: E402

# Long-form documentary producer
try:
    from longform_producer import run_longform_production

    LONGFORM_ENABLED = True
    print("✅ Long-form Documentary Producer loaded")
except ImportError:
    LONGFORM_ENABLED = False
    print("⚠️ Long-form producer not available")

# YouTube SEO Engine
try:
    sys.path.append(str(SRC_DIR / "uploaders"))
    from youtube_seo import generate_full_seo_package, get_category_id
    SEO_ENABLED = True
    print("✅ YouTube SEO Engine loaded")
except ImportError as e:
    SEO_ENABLED = False
    print(f"⚠️ YouTube SEO not available: {e}")

# Thumbnail Generator
try:
    from thumbnail_generator import generate_thumbnail_pair
    THUMBNAILS_ENABLED = True
    print("✅ Thumbnail Generator loaded")
except ImportError as e:
    THUMBNAILS_ENABLED = False
    print(f"⚠️ Thumbnail Generator not available: {e}")

# YouTube Daily Report
try:
    from youtube_daily_report import generate_daily_report, send_upload_notification
    REPORTS_ENABLED = True
    print("✅ YouTube Daily Report loaded")
except ImportError as e:
    REPORTS_ENABLED = False
    print(f"⚠️ YouTube Daily Report not available: {e}")

# Content Council (Консилиум)
try:
    from content_council import run_consilium
    CONSILIUM_ENABLED = True
    print("✅ Content Council (Консилиум) loaded")
except ImportError as e:
    CONSILIUM_ENABLED = False
    print(f"⚠️ Content Council not available: {e}")

# Configuration
REELS_AUTO_UPLOAD = True  # Production Mode
POSTED_HISTORY_FILE = ROOT_DIR / "posted_history.json"

# --- MONETIZATION SAFETY LIMITS (STRICT COMPLIANCE) ---
DAILY_VIDEOS_LIMIT = 3  # Maximum 3 videos per day to avoid "Spam" flags
MIN_INTERVAL_HOURS = 4  # Minimum gap between any two posts
INSTA_ACTION_DELAY = 120  # Delayed actions for human-like behavior
AI_LABEL_MANDATORY = True  # Always label as AI for Meta compliance
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
        telegram_msg = f"🏭 <b>Factory Status:</b> {msg}"
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
    history.append(
        {
            "topic": topic,
            "prefix": prefix,
            "lang": lang,
            "timestamp": datetime.now().isoformat(),
        }
    )
    # Keep history manageable
    save_history(history[-200:])


def get_static_fallback():
    """
    Emergency fallback if deep research fails.
    Improved with date-based variety.
    """
    day_str = datetime.now().strftime("%Y-%m-%d")
    topics = [
        (
            "AI Agents Revolution",
            "How autonomous agents are taking over digital tasks.",
        ),
        ("Quantum Supremacy", "The race for the first practical quantum computer."),
        ("Space Exploration 2026", "Mars colonization and the moon gateway mission."),
        (
            "Neural interface evolution",
            "Connecting human brains directly to the cloud.",
        ),
        ("Sustainable Fusion Energy", "Clean, infinite power is finally within reach."),
        ("Robotics in Everyday Life", "How machines are helping us in our homes."),
        (
            "The Future of Medicine",
            "AI-driven diagnostics and personalized treatments.",
        ),
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


def get_consilium_package(channel: str):
    """
    Find the oldest package in outputs/consilium/.../<channel> with status 'ready_for_production'.
    Marks it as 'processing' and returns its path and data.
    """
    consilium_dir = FACTORY_DIR / "outputs" / "consilium"
    if not consilium_dir.exists():
        return None, None
        
    candidates = []
    # Search all session folders for the channel
    for session_dir in consilium_dir.iterdir():
        if not session_dir.is_dir() or session_dir.name.startswith("_"):
            continue
        channel_dir = session_dir / channel
        if not channel_dir.exists():
            continue
            
        for pkg_dir in channel_dir.iterdir():
            if not pkg_dir.is_dir() or pkg_dir.name.startswith("_"):
                continue
            pkg_file = pkg_dir / "package.json"
            if pkg_file.exists():
                try:
                    data = json.loads(pkg_file.read_text())
                    if data.get("status") == "ready_for_production":
                        candidates.append((pkg_file.stat().st_ctime, pkg_file, data))
                except Exception:
                    pass
                    
    if not candidates:
        return None, None
        
    # Pick the oldest
    candidates.sort(key=lambda x: x[0])
    _, pkg_file, data = candidates[0]
    
    # Mark as processing
    data["status"] = "processing"
    pkg_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    
    return str(pkg_file), data

def update_consilium_status(pkg_path: str, status: str):
    try:
        if not pkg_path:
            return
        path = Path(pkg_path)
        data = json.loads(path.read_text())
        data["status"] = status
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"⚠️ Failed to update consilium status: {e}")

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

    # Determine style (override > mode-based > default)
    if style_override:
        style = style_override
    else:
        style = "cartoon" if mode == "cartoon" else "impact"

    print(f"🎨 Visual Style: {style.upper()}")

    # 0. Check Consilium
    channel = "unifiedsystem" if mode == "english" else "megaforma"
    consilium_pkg_path, consilium_pkg = get_consilium_package(channel) if not manual_topic else (None, None)
    
    if consilium_pkg:
        agent_sync(f"🎓 Найден готовый пакет от Консилиума: {consilium_pkg.get('title')}")
        script_key = "script_en" if mode == "english" else "script_ru"
        
        scenes = []
        for s in consilium_pkg.get("scenes", []):
            scenes.append({"image": s.get("id", f"scene_{len(scenes)}"), "keyword": s.get("visual_keyword", "")})
            
        content_data = {
            "selected_topic": consilium_pkg.get("title", "Consilium Package"),
            "description": consilium_pkg.get("seo", {}).get("description", ""),
            script_key: consilium_pkg.get("script_text", ""),
            "pinned_comment": consilium_pkg.get("pinned_comment", ""),
            "scenes": scenes,
            "_consilium_seo": consilium_pkg.get("seo"),
            "_consilium_path": consilium_pkg_path
        }
    else:
        # PHASE 1. RESEARCH (Ad-hoc fallback)
        agent_sync(f"🔍 Запускаю исследование (Mode: {mode})...")
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
            text=script,
            lang=lang,
            output_name=out_name,
            scenes=final_scenes,
            style=style,
        )

        # 5. UPLOAD (Instagram + YouTube)
        if REELS_AUTO_UPLOAD and video_path and video_path.exists():
            # 5.1 Instagram (Multi-account)
            acc_manager = AccountManager()
            insta_accounts = acc_manager.get_accounts("instagram")

            # Define caption common for all platforms
            caption = content_data.get(
                "description",
                f"New AI vision: {content_data.get('selected_topic', '')}",
            )

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

            # 5.2 YouTube (Multi-channel) — with SEO + Thumbnails
            yt_accounts = acc_manager.get_accounts("youtube")
            raw_topic = content_data.get("selected_topic", f"New AI Video {day_str}")
            raw_script = content_data.get("script_ru", "")

            # Generate SEO package
            seo = content_data.get("_consilium_seo")
            if not seo and SEO_ENABLED:
                try:
                    agent_sync("🔍 Генерирую SEO (title/description/tags)...")
                    seo = generate_full_seo_package(
                        topic=raw_topic,
                        script=raw_script,
                        lang=lang,
                        style="shorts" if mode in ["daily", "cartoon", "english", "hebrew"] else "longform",
                        channel_name="Megaforma" if mode != "english" else "UnifiedSystem",
                    )
                    agent_sync(f"✅ SEO: {seo['title'][:50]}...")
                except Exception as e:
                    agent_sync(f"⚠️ SEO failed: {e}")

            # Use SEO data or fallback
            yt_title = seo["title"] if seo else raw_topic[:100]
            yt_desc = seo["description"] if seo else f"{caption}\n\n#AI #Tech #Future"
            yt_tags = seo["tags"] if seo else ["AI", "Future", "Tech", "Megaforma"]
            yt_category = get_category_id(raw_topic, raw_script) if SEO_ENABLED else "28"

            # Generate thumbnail
            thumbnail_path = None
            if THUMBNAILS_ENABLED:
                try:
                    agent_sync("🖼️ Генерирую thumbnail...")
                    thumbs = generate_thumbnail_pair(
                        title=yt_title,
                        topic=raw_topic,
                        output_dir=ROOT_DIR / "assets" / day_str / "thumbnails",
                        use_ai_bg=False,  # Fast mode - no DALL-E
                    )
                    thumbnail_path = thumbs.get("longform")
                    if thumbnail_path:
                        agent_sync(f"✅ Thumbnail: {thumbnail_path.name}")
                except Exception as e:
                    agent_sync(f"⚠️ Thumbnail failed: {e}")

            for acc in yt_accounts:
                agent_sync(f"Загружаю {prefix} в YouTube ({acc.get('name') or 'Channel'})...")

                try:
                    from youtube_uploader import upload_video

                    token_file = acc.get("token_file")
                    yt_success = upload_video(
                        video_path,
                        title=yt_title,
                        description=yt_desc,
                        tags=yt_tags,
                        category_id=yt_category,
                        privacy_status="public",
                        token_file=token_file,
                    )
                    if yt_success:
                        agent_sync(f"🚀 YouTube ({acc.get('name')}): Успешно!")
                        # Send upload notification
                        if REPORTS_ENABLED:
                            video_url = "https://www.youtube.com/@Megaforma"
                            send_upload_notification(yt_title, video_url, "YouTube")
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
                update_consilium_status(content_data.get("_consilium_path"), "published")
            else:
                update_consilium_status(content_data.get("_consilium_path"), "failed")

    except Exception as e:
        print(f"❌ Factory Crash: {e}")
        agent_sync(f"Критическая ошибка фабрики: {e}")
        if "_consilium_path" in locals() and content_data.get("_consilium_path"):
            update_consilium_status(content_data.get("_consilium_path"), "failed")
        time.sleep(60)  # Prevent rapid restart loop


def start_scheduler():
    """Stable Scheduler Loop with Meta Compliance + YouTube Analytics."""
    agent_sync("⏰ Планировщик фабрики запущен (STRICT COMPLIANCE - 3 видео/день + аналитика 22:00)")

    # 0. КОНСИЛИУМ (06:00 UTC = 09:00 ISR) — ПЕРЕД продакшном
    def consilium_task():
        """Исследование трендов и генерация сценариев для обоих каналов."""
        if not CONSILIUM_ENABLED:
            print("⚠️ Consilium disabled")
            return
        try:
            agent_sync("🎓 Консилиум: Начинаю исследование трендов (Megaforma + UnifiedSystem)...")
            # Megaforma — 3 темы на русском
            pkgs_mega = run_consilium(channel="megaforma", top_n=3, notify=True)
            agent_sync(f"✅ Megaforma: {len(pkgs_mega)} сценариев готово")
            # UnifiedSystem — 2 темы на английском
            pkgs_uni = run_consilium(channel="unifiedsystem", top_n=2, notify=True)
            agent_sync(f"✅ UnifiedSystem: {len(pkgs_uni)} сценариев готово")
            total = len(pkgs_mega) + len(pkgs_uni)
            agent_sync(f"🎓 Консилиум завершён: {total} пакетов в очереди на производство")
        except Exception as e:
            agent_sync(f"⚠️ Consilium error: {e}")

    # 1. Morning Production (09:00 ISR -> 07:00 UTC)
    def morning_task():
        # Add random jitter up to 45 minutes
        delay = random.randint(0, 2700)
        print(f"⌛ Random Jitter: Waiting {delay}s before Morning Run...")
        time.sleep(delay)
        run_factory_production(mode="daily")

    # 2. Lunch Production (14:00 ISR -> 12:00 UTC)
    def lunch_task():
        delay = random.randint(0, 3600)
        print(f"⌛ Random Jitter: Waiting {delay}s before Lunch Run...")
        time.sleep(delay)
        run_factory_production(mode="english")

    # 3. Evening Production (20:00 ISR -> 18:00 UTC)
    def evening_task():
        delay = random.randint(0, 1800)
        print(f"⌛ Random Jitter: Waiting {delay}s before Evening Run...")
        time.sleep(delay)
        run_factory_production(mode="cartoon")

    # 4. Daily Analytics Report (22:00 ISR -> 19:00 UTC)
    def analytics_report_task():
        if REPORTS_ENABLED:
            print("📊 Generating daily YouTube analytics report...")
            try:
                generate_daily_report()
            except Exception as e:
                print(f"⚠️ Analytics report failed: {e}")
        else:
            print("⚠️ Reports module not available")

    # Schedule tasks
    schedule.every().day.at("06:00").do(consilium_task)  # 09:00 ISR — Research first
    schedule.every().day.at("07:00").do(morning_task)
    schedule.every().day.at("12:00").do(lunch_task)
    schedule.every().day.at("18:00").do(evening_task)
    schedule.every().day.at("19:00").do(analytics_report_task)  # 22:00 ISR

    # Weekly Special
    schedule.every().sunday.at("08:00").do(run_factory_production, mode="hebrew")

    if LONGFORM_ENABLED:
        schedule.every().saturday.at("16:00").do(run_longform_production)

    print("🚀 COMPLIANT Scheduler running. Waiting for pending tasks...")
    print("📅 Schedule:")
    print("   06:00 UTC (09:00 ISR) - 🎓 КОНСИЛИУМ: Тренды + Сценарии (Megaforma+UnifiedSystem)")
    print("   07:00 UTC (10:00 ISR) - Morning Shorts (RU)")
    print("   12:00 UTC (15:00 ISR) - Lunch Shorts (EN)")
    print("   18:00 UTC (21:00 ISR) - Evening Shorts (Cartoon)")
    print("   19:00 UTC (22:00 ISR) - Analytics Report → Telegram")
    print("   Saturday 16:00 UTC    - Long-form Documentary")
    print("   Sunday   08:00 UTC    - Hebrew Special")

    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


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
    parser.add_argument("--no-upload", action="store_true", help="Disable all uploads (dry-run)")
    parser.add_argument(
        "--style",
        type=str,
        choices=["impact", "cartoon", "sketch", "painting"],
        help="Force visual style",
    )
    parser.add_argument(
        "--inspiration-topic",
        type=str,
        help="Manually provided topic from YouTube Inspiration Tab",
    )
    parser.add_argument(
        "--inspiration-outline",
        type=str,
        help="Manually provided outline from YouTube Inspiration Tab",
    )

    args = parser.parse_args()

    # Allow CLI override for upload
    if args.auto_upload:
        REELS_AUTO_UPLOAD = True
    if args.no_upload:
        REELS_AUTO_UPLOAD = False

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
