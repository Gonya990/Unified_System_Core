
import os
import urllib.parse
from pathlib import Path

from dotenv import load_dotenv
from instagrapi import Client

# Load env from Root
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
load_dotenv(ROOT_DIR / ".env")

def test_login():
    session_id = os.getenv("INSTAGRAM_SESSION_ID")
    if not session_id:
        print("❌ No session ID")
        return

    session_id = urllib.parse.unquote(session_id)
    print(f"🔑 Testing Session ID: {session_id[:10]}...")

    cl = Client()
    try:
        cl.login_by_sessionid(session_id)
        print(f"✅ Login SUCCESS! User ID: {cl.user_id}")
        info = cl.user_info(cl.user_id)
        print(f"👤 Account: {info.username}")
    except Exception as e:
        print(f"❌ Login FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_login()
