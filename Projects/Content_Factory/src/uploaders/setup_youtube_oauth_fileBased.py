import os
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SECRETS_FILE = ROOT_DIR / 'Projects/Content_Factory/client_secrets.json'
TOKEN_FILE = ROOT_DIR / 'Projects/Content_Factory/youtube_token.json'
CODE_FILE = ROOT_DIR / 'Projects/Content_Factory/youtube_code.txt'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

def setup_oauth():
    # Clean up old code file
    if CODE_FILE.exists():
        CODE_FILE.unlink()

    if not SECRETS_FILE.exists():
        print(f"❌ Secrets file not found: {SECRETS_FILE}")
        return

    print(f"🔑 Starting OAuth flow...")
    flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS_FILE), SCOPES)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print('--------------------------------------------------')
    print('CLICK THIS URL: {}'.format(auth_url))
    print('--------------------------------------------------')
    print('Waiting for code in youtube_code.txt...')
    
    while not CODE_FILE.exists():
        time.sleep(2)
        
    with open(CODE_FILE, 'r') as f:
        code = f.read().strip()
    
    print(f"📥 Received code: {code[:5]}...")
    
    flow.fetch_token(code=code)
    creds = flow.credentials
    
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    
    print(f"✅ Token saved to {TOKEN_FILE}")

if __name__ == '__main__':
    setup_oauth()
