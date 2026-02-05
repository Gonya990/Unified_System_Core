import sys
import os
import json
from pathlib import Path
from instagrapi import Client
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

def test_session():
    print("🕵️ Testing Instagram Session Injection...")
    
    cl = Client()
    # Load settings from file (which we just wrote with user cookies)
    session_path = Path('/home/gonya/Unified_System_Core/Projects/Content_Factory/insta_session.json')
    
    try:
        if session_path.exists():
            cl.load_settings(session_path)
            # Try to get own profile info to verify auth
            user_id = cl.user_id
            print(f"✅ Session Valid! User ID: {user_id}")
            info = cl.user_info(user_id)
            print(f"🎉 Logged in as: {info.username} ({info.full_name})")
        else:
            print("❌ Session file missing")
    except Exception as e:
        print(f"❌ Session Failed: {e}")

if __name__ == '__main__':
    test_session()
