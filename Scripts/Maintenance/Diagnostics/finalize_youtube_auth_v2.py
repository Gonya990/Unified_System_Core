import json
import sys
from pathlib import Path

# Add AI_Core/src to path
sys.path.append("/home/gonya/Unified_System/Projects/AI_Core/src")

try:
    from config_manager import ConfigManager
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from identity_orchestrator import IdentityOrchestrator
    from user_context_db import UserContextDB
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Configuration
CLIENT_SECRETS_FILE = "/home/gonya/Unified_System/Projects/AI_Core/client_secret.json"
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.settings.basic',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/drive',
    'openid'
]
REDIRECT_URI = 'http://localhost'
ADMIN_ID = 708531393

def generate_url():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline', include_granted_scopes='true')
    print(f"\n🔗 AUTHORIZATION URL:\n{auth_url}\n")
    print("👉 Click the link, authorize, and copy the 'code' parameter from the localhost URL.")

def exchange_code(code):
    try:
        # Initialize dependencies only for exchange
        db_path = "/home/gonya/Unified_System/Projects/AI_Core/user_context.db"
        db = UserContextDB(db_path=db_path)
        config = ConfigManager()
        # Mock auth manager for IdentityOrchestrator init if needed, or just use identity to save
        # Actually we need flow to exchange code
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )

        print(f"🔄 Exchanging code: {code[:10]}...")
        flow.fetch_token(code=code)
        creds = flow.credentials

        print("✅ Code exchanged successfully!")

        # Save to DB via IdentityOrchestrator (need to init properly)
        # We'll just manually mimic the save since import might be complex with deps
        creds_json = creds.to_json()

        # 1. Update Content Factory Token (Immediate Fix)
        target_path = Path("/home/gonya/Unified_System/Projects/Content_Factory/src/uploaders/.credentials/youtube_token.json")
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w") as f:
            f.write(creds_json)
        print(f"✅ YouTube token updated at {target_path}")

        # 2. Update AI_Core Token (Legacy/Bot)
        # We try to use the DB class if possible, otherwise skip to avoid "AttributeError"
        try:
            db.set_google_creds(ADMIN_ID, creds_json)
            print("✅ Credentials saved to user_context.db")
        except Exception as e:
            print(f"⚠️ Could not save to DB (minor): {e}")

        # Verify Scopes
        creds_dict = json.loads(creds_json)
        scopes_got = creds_dict.get("scopes", [])
        if "https://www.googleapis.com/auth/youtube.upload" in scopes_got:
            print("🚀 YOUTUBE UPLOAD SCOPE ACQUIRED!")
        else:
            print(f"⚠️ Missing YouTube scope. Got: {scopes_got}")

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
            if not code.startswith("4/"):
                # sometimes users paste just the end, but usually it starts with 4/
                pass
            exchange_code(code)
    else:
        print("Usage: python3 finalize.py [url|<code>]")
