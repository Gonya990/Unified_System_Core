#!/usr/bin/env python3
"""
Gmail Automation Agent
Агент автоматизации Gmail

Automatically monitors and processes emails from gonya90.gg@gmail.com
"""

import argparse
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("❌ Gmail API libraries not installed!")
    msg = "Install with: pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    print(msg)
    sys.exit(1)

# Scopes for Gmail API
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")

CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
CREDS_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_PATH = CREDS_DIR / "gmail_token.json"
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
# EMAIL_DB_PATH = BASE_DIR / "logs" / "automation" / "email_database.json"

# Email categories
CATEGORIES = {
    "urgent": {
        "keywords": ["urgent", "asap", "important", "срочно", "важно", "דחוף"],
        "icon": "🔴",
    },
    "work": {
        "keywords": ["interview", "job", "vacancy", "работа", "вакансия", "משרה"],
        "icon": "💼",
        "senders": ["@schindler"],
    },
    "shopping": {
        "keywords": ["order", "shipped", "tracking", "заказ", "доставка"],
        "icon": "🛒",
        "senders": ["@amazon", "@ebay", "@aliexpress"],
    },
    "bank": {
        "keywords": ["transaction", "bank", "בנק", "כרטיס אשראи"],
        "icon": "🏦",
        "senders": ["@bankhapoalim", "@leumi", "@isracard"],
    },
    "github": {
        "keywords": ["github", "pull request", "commit", "merge"],
        "icon": "🐙",
        "senders": ["@github.com"],
    },
}


def get_gmail_service():
    """Authenticate and return Gmail API service"""
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def categorize_email(subject, body, sender):
    """Categorize email based on sender and content"""
    sender_lower = sender.lower()
    for cat, data in CATEGORIES.items():
        for pattern in data.get("senders", []):
            if pattern in sender_lower:
                return cat
    content = f"{subject} {body}".lower()
    for cat, data in CATEGORIES.items():
        for kw in data["keywords"]:
            if kw in content:
                return cat
    return "info"


def send_telegram_alert(category, subject, sender, preview):
    """Send a notification to Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    priority_map = {
        "urgent": "🚨 URGENT",
        "work": "💼 WORK",
        "github": "🐙 GIT",
    }
    if category not in priority_map:
        return
    import html

    msg = (
        f"{priority_map[category]}\n\n"
        f"<b>From:</b> {html.escape(sender)}\n"
        f"<b>Subject:</b> {html.escape(subject)}\n"
        f"<i>{html.escape(preview[:100])}...</i>"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception:
        pass


def get_emails(service, hours=24, unread_only=False):
    """Get emails from last N hours or unread only"""
    if unread_only:
        q = "is:unread"
    else:
        since = datetime.now() - timedelta(hours=hours)
        q = f"after:{int(since.timestamp())}"

    results = service.users().messages().list(userId="me", q=q).execute()
    messages = results.get("messages", [])
    emails = []
    for msg in messages:
        try:
            m = service.users().messages().get(userId="me", id=msg["id"]).execute()
            headers = m["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "")
            body = ""
            cat = categorize_email(subject, body, sender)
            emails.append({"id": msg["id"], "subject": subject, "sender": sender, "cat": cat})
            send_telegram_alert(cat, subject, sender, "")
        except Exception:
            continue
    return emails


def main():
    parser = argparse.ArgumentParser(description="Gmail Automation Agent")
    parser.add_argument("--unread", action="store_true")
    args = parser.parse_args()

    service = get_gmail_service()
    emails = get_emails(service, hours=24, unread_only=args.unread)
    print(f"Processed {len(emails)} emails")


if __name__ == "__main__":
    main()
