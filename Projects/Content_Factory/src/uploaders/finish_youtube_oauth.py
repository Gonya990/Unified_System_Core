import os
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SECRETS_FILE = ROOT_DIR / 'Projects/Content_Factory/client_secrets.json'
TOKEN_FILE = ROOT_DIR / 'Projects/Content_Factory/youtube_token.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

def finish_oauth():
    code = '4/1ASc3gC0UokASVNorgsqaI9TzwtFEzx9TAU3cKiRCiMWITft5vzZTr2NXdtk'
    
    flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS_FILE), SCOPES)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
    
    # We need to set the state that was used generates the URL, but since we are just 
    # fetching the token with the code, strictly speaking, fetch_token doesn't always check state 
    # if we don't pass it back. Let's try fetching directly.
    
    try:
        flow.fetch_token(code=code)
        creds = flow.credentials
        
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        
        print(f"✅ Token saved to {TOKEN_FILE}")
    except Exception as e:
        print(f"❌ Error fetching token: {e}")

if __name__ == '__main__':
    finish_oauth()
