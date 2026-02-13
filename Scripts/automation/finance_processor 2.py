#!/usr/bin/env python3
"""
Finance Processor for Gmail
Searches for receipts and invoices to update the Financial Report.
"""

from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / "Projects/AI_Core/.env")

# Gmail Config
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
TOKEN_PATH = CREDS_DIR / "gmail_token.json"


def get_gmail_service():
    if not TOKEN_PATH.exists():
        print("❌ Gmail token not found. Please run gmail_agent.py first.")
        return None
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
    return build("gmail", "v1", credentials=creds)


def search_finance_emails(service):
    # Search for common AI subscription receipts
    queries = [
        "subject:(receipt OR invoice OR payment OR subscription)",
        "from:suno",
        "from:elevenlabs",
        "from:runway",
        "from:openai",
        "from:luma",
    ]

    found_emails = []
    # Search in the last 30 days
    since = datetime.now() - timedelta(days=30)
    q = f"({' OR '.join(queries)}) after:{int(since.timestamp())}"

    print(f"🔍 Searching Gmail with: {q}")
    results = service.users().messages().list(userId="me", q=q).execute()
    messages = results.get("messages", [])

    for msg in messages:
        msg_data = (
            service.users()
            .messages()
            .get(userId="me", id=msg["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"])
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg_data.get("payload", {}).get("headers", [])}

        found_emails.append(
            {
                "from": headers.get("From"),
                "subject": headers.get("Subject"),
                "date": headers.get("Date"),
                "snippet": msg_data.get("snippet"),
            }
        )

    return found_emails


def main():
    service = get_gmail_service()
    if not service:
        return

    emails = search_finance_emails(service)
    print(f"\n✅ Found {len(emails)} relevant financial emails:")
    for email in emails:
        print("---")
        print(f"📅 Date: {email['date']}")
        print(f"👤 From: {email['from']}")
        print(f"📝 Subj: {email['subject']}")
        print(f"📄 Snippet: {email['snippet'][:100]}...")


if __name__ == "__main__":
    main()
