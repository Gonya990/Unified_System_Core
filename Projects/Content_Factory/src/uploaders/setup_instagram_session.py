import os
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client

# Setup paths
ROOT_DIR = Path("/home/gonya/Unified_System_Core")
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)


def setup_session():
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if not username or not password:
        print("❌ INSTAGRAM_USERNAME or INSTAGRAM_PASSWORD not set in .env")
        return

    cl = Client()
    try:
        print(f"🔐 Logging in as {username}...")
        cl.login(username, password)
        print("LOGIN_SUCCESS")

        session_path = Path(
            "/home/gonya/Unified_System_Core/Projects/Content_Factory/insta_session.json"
        )
        cl.dump_settings(session_path)
        print(f"SESSION_SAVED: {session_path}")

    except Exception as e:
        print(f"❌ Login failed: {e}")
        # Handle 2FA if needed?
        if "Two-factor authentication required" in str(e):
            print("2FA_REQUIRED")
            code = input("Enter 2FA Code: ")
            cl.login(username, password, verification_code=code)
            cl.dump_settings(session_path)
            print("2FA_SUCCESS")


if __name__ == "__main__":
    setup_session()
