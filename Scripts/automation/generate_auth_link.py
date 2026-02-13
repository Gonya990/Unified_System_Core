from pathlib import Path

from google_auth_oauthlib.flow import Flow

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
TOKEN_PATH = CREDS_DIR / "gmail_token.json"

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly https://www.googleapis.com/auth/gmail.compose"]

try:
    flow = Flow.from_client_secrets_file(str(CREDENTIALS_PATH), scopes=SCOPES, redirect_uri="urn:ietf:wg:oauth:2.0:oob")

    auth_url, _ = flow.authorization_url(prompt="consent")

    print("\n" + "=" * 80)
    print("ACTION REQUIRED: GMAIL RE-AUTHENTICATION")
    print("=" * 80)
    print("The previous access token has expired. Please authorize the app manually.")
    print("\n1. Click this link to authorize:")
    print(f"\n{auth_url}\n")
    print("2. Copy the authorization code.")
    print("3. Run this command in your terminal to complete setup:")
    print("\npython3 Scripts/automation/complete_auth.py --code YOUR_CODE_HERE\n")
    print("=" * 80 + "\n")

except Exception as e:
    print(f"Error generating auth link: {e}")
