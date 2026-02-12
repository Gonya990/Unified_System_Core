from pathlib import Path

from instagrapi import Client

# Paths
current_file = Path(__file__).resolve()
CREDENTIALS_DIR = current_file.parent / ".credentials"
SESSION_FILE = CREDENTIALS_DIR / "insta_session.json"

def upload_reel(video_path, caption):
    print(f"📸 Preparing to upload to Instagram: {video_path}")

    cl = Client()

    # Load session
    if SESSION_FILE.exists():
        try:
            print("📂 Loading session from: " + str(SESSION_FILE))
            cl.load_settings(SESSION_FILE)

            # Verify
            if cl.user_id:
                 print(f"✅ Authenticated as user: {cl.user_id}")
            else:
                 print("⚠️ Session loaded but user_id is empty?")
        except Exception as e:
            print(f"❌ Session load error: {e}")
    else:
        print(f"❌ Session file not found: {SESSION_FILE}")

    if not cl.user_id:
        print("❌ Not logged in. Cannot upload.")
        return False

    try:
        print("📤 Uploading Video...")
        media = cl.video_upload(str(video_path), caption)
        print(f"✅ Video Uploaded! Media ID: {media.pk}")
        print(f"🔗 Code: {media.code}")
        return True
    except Exception as e:
        print(f"❌ Upload Failed: {e}")
        if "login_required" in str(e):
            print("💡 Hint: The session might be invalid or IP locked. Try logging in again locally and extracting cookies.")
        return False
