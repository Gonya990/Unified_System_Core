import os
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client

# Load environment variables
load_dotenv(override=True)

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
INSTAGRAM_SESSION_ID = os.getenv("INSTAGRAM_SESSION_ID")  # For 2FA/Meta login
SESSION_FILE = "insta_session.json"


def upload_reel(video_path: str, caption: str, session_id: str = None):
    """
    Uploads a video as an Instagram Reel using instagrapi.
    Supports Login via Username/Password or SessionID (bypasses 2FA).
    """
    cl = Client()

    # Use provided session_id or fallback to env
    active_session_id = session_id or INSTAGRAM_SESSION_ID

    # 1. Try Session ID (Most robust for 2FA/Facebook login)
    if active_session_id and active_session_id != "your_session_id":
        try:
            print("🔑 Attempting login via Session ID...")
            cl.login_by_sessionid(active_session_id)
            print("✅ Login via Session ID successful!")
        except Exception as e:
            print(f"⚠️ Session ID login failed: {e}")

    # 2. Try saved session file
    if not cl.user_id and Path(SESSION_FILE).exists():
        try:
            cl.load_settings(SESSION_FILE)
            print("✅ Loaded existing Instagram session from file.")
        except Exception:
            print("⚠️ Session file invalid.")

    # 3. Last resort: Username/Password
    if not cl.user_id:
        if (
            not INSTAGRAM_USERNAME
            or not INSTAGRAM_PASSWORD
            or INSTAGRAM_USERNAME == "your_username"
        ):
            print("❌ Error: No valid session and no credentials in .env")
            print(
                "💡 TIP: Copy your 'sessionid' cookie from the browser and put it in .env as INSTAGRAM_SESSION_ID"
            )
            return False

        try:
            print(f"🔐 Logging in to Instagram as {INSTAGRAM_USERNAME}...")
            cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            cl.dump_settings(SESSION_FILE)
            print("✅ Login successful and session saved.")
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False

    # Compliance: Add "Made with AI" disclosure to caption
    ai_tag = "✨ Made with AI / Сгенерировано ИИ\n\n"
    final_caption = ai_tag + caption

    # Upload the Reel
    print(f"🚀 Uploading Reel: {video_path}...")
    try:
        # We attempt to use is_ai_generated if the library version supports it
        # Otherwise, the text disclosure in the caption is the secondary safety net.
        params = {"video_path": video_path, "caption": final_caption[:2000]}

        # Check if version supports is_ai_generated (Safe call)
        try:
            media = cl.clip_upload(**params, is_ai_generated=True)
        except TypeError:
            media = cl.clip_upload(**params)

        print(f"✨ Successfully uploaded Reel! Media ID: {media.id}")
        return True
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return False


if __name__ == "__main__":
    # Test path
    test_video = Path(__file__).parent.parent.parent / "outputs/latest_video.mp4"
    test_caption = (
        "Будущее 2026: Эволюция Разума. #AI #Future #Technology #ImpactVision"
    )

    if Path(test_video).exists():
        upload_reel(test_video, test_caption)
    else:
        print(f"⚠️ Test video not found at {test_video}")
