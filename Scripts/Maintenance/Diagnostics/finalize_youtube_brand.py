import sys
import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import Flow

# Configuration
CLIENT_SECRETS_FILE = "/home/gonya/Unified_System/Projects/AI_Core/client_secret.json"

# SCOPES must match what was requested in the URL
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'openid'
]
REDIRECT_URI = 'http://localhost'

def generate_url():
    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"❌ ОШИБКА: Файл {CLIENT_SECRETS_FILE} не найден.")
        return

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    
    print(f"\n🔗 НОВАЯ ССЫЛКА АВТОРИЗАЦИИ (Только YouTube):\n{auth_url}\n")
    print("👉 Нажмите на ссылку, выберите ВАШ НОВЫЙ БРЕНД-АККАУНТ (Unified System) и скопируйте код.")

def exchange_code(code):
    try:
        print(f"🔄 Exchanging code: {code[:10]}...")
        
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        print("✅ Code exchanged successfully!")
        
        creds_json = creds.to_json()
        
        # Save to Content Factory path
        target_path = Path("/home/gonya/Unified_System/Projects/Content_Factory/src/uploaders/.credentials/youtube_token.json")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        # Backup existing if any
        if target_path.exists():
            backup_path = target_path.with_suffix('.bak')
            target_path.rename(backup_path)
            print(f"📦 Backed up old token to {backup_path}")
            
        with open(target_path, "w") as f:
            f.write(creds_json)
        print(f"✅ YouTube BRAND token updated at {target_path}")
        
        # Verify
        creds_dict = json.loads(creds_json)
        # Access token usually doesn't show scopes directly in to_json sometimes, but let's check
        scopes_got = creds_dict.get("scopes", [])
        if "https://www.googleapis.com/auth/youtube.upload" in scopes_got:
            print("🚀 YOUTUBE UPLOAD SCOPE ACQUIRED for BRAND ACCOUNT!")
        else:
             print("ℹ️ Token saved. Ready for upload.")

    except Exception as e:
        print(f"❌ Error exchanging code: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "url":
            generate_url()
        else:
            code = sys.argv[1]
            exchange_code(code)
    else:
        print("Usage: python3 finalize_youtube_brand.py [url|<code>]")
