
import argparse
import sys
from pathlib import Path

from google_auth_oauthlib.flow import Flow

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
TOKEN_PATH = CREDS_DIR / "gmail_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose"
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", required=True, help="Authorization code from Google")
    args = parser.parse_args()

    try:
        flow = Flow.from_client_secrets_file(
            str(CREDENTIALS_PATH),
            scopes=SCOPES,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        )

        # Exchange code for token
        flow.fetch_token(code=args.code)
        creds = flow.credentials

        # Save token
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

        print("\n✅ Authentication successful! Token saved.")
        print("You can now ask the agent to scan your emails.")

    except Exception as e:
        print(f"❌ Error completing auth: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
