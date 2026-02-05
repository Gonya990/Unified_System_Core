import os
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SECRETS_FILE = ROOT_DIR / 'Projects/Content_Factory/client_secrets.json'
TOKEN_FILE = ROOT_DIR / 'Projects/Content_Factory/youtube_token.json'
CODE_FILE = ROOT_DIR / 'Projects/Content_Factory/youtube_code.txt'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

def setup_oauth():
    if CODE_FILE.exists():
        CODE_FILE.unlink()

    print(f"🔑 Starting OAuth flow (V3 with Valid Secrets)...")
    flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS_FILE), SCOPES)
    flow.redirect_uri = 'http://localhost'
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    print('--------------------------------------------------')
    print('1. CLICK THIS URL: {}'.format(auth_url))
    print('2. Authorize the app.')
    print('3. You will be redirected to http://localhost/?code=... (Site can not be reached)')
    print('4. COPY the code value from the address bar (between code= and &scope).')
    print('--------------------------------------------------')
    print('Waiting for code in youtube_code.txt...')
    
    while not CODE_FILE.exists():
        time.sleep(2)
        
    with open(CODE_FILE, 'r') as f:
        code = f.read().strip()
    
    # Clean code just in case
    if '&' in code:
        code = code.split('&')[0]
        
    print(f"📥 Received code: {code[:10]}...")
    
    try:
        flow.fetch_token(code=code)
        creds = flow.credentials
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print(f"✅ Token saved to {TOKEN_FILE}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    setup_oauth()
