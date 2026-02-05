import sys
import os
from pathlib import Path
from instagrapi import Client
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

def finish_login():
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    code = '741909'

    cl = Client()
    try:
        print(f"🔐 Logging in as {username} with 2FA...")
        cl.login(username, password, verification_code=code)
        print("LOGIN_SUCCESS")
        
        session_path = Path('/home/gonya/Unified_System_Core/Projects/Content_Factory/insta_session.json')
        cl.dump_settings(session_path)
        print(f"SESSION_SAVED: {session_path}")
        
    except Exception as e:
        print(f"❌ Login failed: {e}")

if __name__ == '__main__':
    finish_login()
