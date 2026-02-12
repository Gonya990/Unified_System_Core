from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

# Setup paths
ROOT_DIR = Path('/home/gonya/Unified_System_Core')
SECRETS_FILE = ROOT_DIR / 'Projects/Content_Factory/client_secrets.json'
TOKEN_FILE = ROOT_DIR / 'Projects/Content_Factory/youtube_token.json'

SCOPES = ['https://www.googleapis.com/auth/youtube.upload', 'https://www.googleapis.com/auth/youtube.readonly']

def setup_oauth():
    if not SECRETS_FILE.exists():
        print(f"❌ Secrets file not found: {SECRETS_FILE}")
        return

    print(f"🔑 Starting OAuth flow using {SECRETS_FILE}...")
    flow = InstalledAppFlow.from_client_secrets_file(str(SECRETS_FILE), SCOPES)

    # Manual Console Flow
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

    auth_url, _ = flow.authorization_url(prompt='consent')

    print(f'Please go to this URL: {auth_url}')

    code = input('Enter the authorization code: ')

    flow.fetch_token(code=code)
    creds = flow.credentials

    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

    print(f"✅ Token saved to {TOKEN_FILE}")

if __name__ == '__main__':
    setup_oauth()
