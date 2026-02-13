#!/usr/bin/env python3
"""
Fetch Job Emails from Last 4 Months (Optimized)
"""

# SECURITY: Using JSON instead of pickle for OAuth tokens (US-psm.1)
import base64
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("❌ Gmail API libraries not installed!")
    sys.exit(1)

# Configuration
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
TOKEN_PATH = CREDS_DIR / "gmail_token.json"
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
OUTPUT_FILE = BASE_DIR / "Projects" / "AI_Core" / "src" / "emails_4_months.json"


def get_gmail_service():
    """Authenticate and return Gmail service with proper credential refresh."""
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print(f"❌ Missing credentials file: {CREDENTIALS_PATH}")
                print("Please run gmail_agent.py first to set up OAuth.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)

        # Save refreshed/new credentials
        CREDS_DIR.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, "w") as token_file:
            token_file.write(creds.to_json())
        print("✅ Credentials saved.")

    return build("gmail", "v1", credentials=creds)


def get_email_body(payload):
    body = ""
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                if part["body"].get("data"):
                    return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
            elif part["mimeType"].startswith("multipart/"):
                found = get_email_body(part)
                if found:
                    return found
    return body


def main():
    print("Authenticating...")
    service = get_gmail_service()

    # 4 months ago
    four_months_ago = (datetime.now() - timedelta(days=120)).strftime("%Y/%m/%d")

    # Optimized Query: Filter server-side
    query = f"after:{four_months_ago} (subject:job OR subject:vacancy OR subject:hiring OR subject:career OR subject:משרה OR subject:דרוש OR content:apply OR content:resume)"

    print(f"Fetching RELEVANT emails since {four_months_ago}...")

    messages = []
    next_page_token = None

    while True:
        results = service.users().messages().list(userId="me", q=query, pageToken=next_page_token).execute()
        new_messages = results.get("messages", [])
        messages.extend(new_messages)
        next_page_token = results.get("nextPageToken")
        if not next_page_token:
            break

    print(f"Found {len(messages)} potential job emails.")

    email_data = []
    for i, msg in enumerate(messages):
        try:
            full_msg = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
            payload = full_msg.get("payload", {})
            headers = payload.get("headers", [])

            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown)")
            date = next((h["value"] for h in headers if h["name"] == "Date"), "")
            content = get_email_body(payload)

            email_data.append(
                {
                    "id": msg["id"],
                    "subject": subject,
                    "sender": sender,
                    "date": date,
                    "content": content[:2000],
                }
            )
            if i % 20 == 0:
                print(f"Processed {i}...")

        except Exception as e:
            print(f"Error: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(email_data, f, ensure_ascii=False, indent=2)
    print("Done.")


if __name__ == "__main__":
    main()
