from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]
# Paths relative to this file
current_file = Path(__file__).resolve()
CREDENTIALS_DIR = current_file.parent / ".credentials"
CLIENT_SECRETS_FILE = CREDENTIALS_DIR / "client_secrets.json"
TOKEN_FILE = CREDENTIALS_DIR / "youtube_token.json"

CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)


def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    with open(TOKEN_FILE, "w") as token:
        token.write(creds.to_json())
    print(f"Token saved to {TOKEN_FILE}")


if __name__ == "__main__":
    authenticate()
