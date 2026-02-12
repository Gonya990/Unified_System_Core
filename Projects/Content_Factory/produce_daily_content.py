import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Setup dynamic paths
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent
SRC_DIR = CURRENT_DIR / "src"

# Inject paths for imports
paths_to_add = [
    SRC_DIR,
    SRC_DIR / "researcher",
    SRC_DIR / "pipeline",
    SRC_DIR / "uploaders",
]
for p in paths_to_add:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Load project components AFTER path injection
import scheduler  # noqa: E402

# from daily_researcher import generate_vision_assets
# import orchestrator_v3_no_face as orchestrator

# Import Uploaders
try:
    from account_manager import AccountManager  # noqa: E402
    from insta_uploader import upload_reel as insta_upload
    from telegram_uploader import send_video as tg_upload
    from youtube_uploader import upload_video as yt_upload
except ImportError as e:
    print(f"⚠️ Warning: Some uploaders could not be imported: {e}")

load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

logger = logging.getLogger("ContentFactory")


def run_production_cycle():
    print("🏭 CONTENT FACTORY: STARTING PRODUCTION CYCLE...")

    # Initialize account manager
    acc_manager = AccountManager()

    # 1. Get Plan
    plan = scheduler.get_daily_production_plan()
    print(f"📅 Today's Plan: {len(plan)} slots")

    for task in plan:
        lang = task["lang"].value
        slot = task["slot"]
        print(f"\n🚀 Processing: {lang.upper()} ({slot}) ...")

        # 2. Topic Mining (Simplified for base version)
        topic = "Future of Business 2026"
        output_name = f"content_{slot}_{lang}"

        # 3. Content Generation (Assuming orchestrator handles it)
        # video_path = orchestrator.generate_full_video(topic=topic, lang=lang)
        # For now, we simulate success with a placeholder path
        video_path = ROOT_DIR / f"outputs/daily/{output_name}.mp4"

        print(f"✅ {output_name} production simulation complete.")

        # 4. Automate Uploads
        if os.getenv("AUTOMATION_MODE", "False") == "True":
            print(f"📤 Uploading {output_name} to platforms...")

            # Telegram
            chat_id = os.getenv("TELEGRAM_ADMIN_ID")
            if chat_id:
                try:
                    tg_upload(str(video_path), f"Daily Content: {topic}", chat_id)
                except Exception as e:
                    print(f"❌ TG Upload failed: {e}")

            # YouTube
            yt_accounts = acc_manager.get_accounts("youtube")
            for acc in yt_accounts:
                try:
                    yt_upload(
                        video_path,
                        title=f"AI Future: {topic}",
                        token_file=acc.get("token_file"),
                    )
                except Exception as e:
                    print(f"❌ YT Upload failed for {acc.get('name')}: {e}")

            # Instagram
            insta_accounts = acc_manager.get_accounts("instagram")
            for acc in insta_accounts:
                try:
                    insta_upload(
                        str(video_path),
                        "AI Daily Brief #AI #Future",
                        session_id=acc.get("session_id"),
                    )
                except Exception as e:
                    print(f"❌ Insta Upload failed for {acc.get('username')}: {e}")

    print("\n💤 Cycle Complete. Sleeping until next trigger.")


if __name__ == "__main__":
    run_production_cycle()
