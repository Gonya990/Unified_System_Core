#!/usr/bin/env python3
"""
Gmail Automation Agent
Агент автоматизации Gmail

Automatically monitors and processes emails from gonya90.gg@gmail.com
Автоматически мониторит и обрабатывает письма с gonya90.gg@gmail.com
"""

# SECURITY: Using JSON instead of pickle for OAuth tokens (US-psm.1)
import base64
import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from pathlib import Path

import requests
from dotenv import load_dotenv

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Gmail API libraries not installed!")
    print(
        "Install with: pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
    )
    sys.exit(1)

# Scopes for Gmail API
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]

# Paths
# Determine BASE_DIR relative to this script location
# Script is in: Unified_System/Scripts/automation/gmail_agent.py
# Base should be: Unified_System/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID")
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
CREDS_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_PATH = CREDS_DIR / "gmail_token.json"  # Migrated from pickle for security
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
EMAIL_DB_PATH = BASE_DIR / "logs" / "automation" / "email_database.json"

# Email categories with sender patterns for better matching
CATEGORIES = {
    # Priority categories
    "urgent": {
        "keywords": ["urgent", "asap", "important", "срочно", "важно", "דחוף", "מיידי"],
        "icon": "🔴",
        "senders": [],
    },
    "work": {
        "keywords": [
            "interview",
            "job",
            "position",
            "vacancy",
            "работа",
            "вакансия",
            "משרה",
            "schindler",
        ],
        "icon": "💼",
        "senders": ["@schindler"],
    },
    # Shopping
    "shopping": {
        "keywords": [
            "order",
            "shipped",
            "delivered",
            "tracking",
            "заказ",
            "доставка",
            "משלוח",
            "הזמנה",
        ],
        "icon": "🛒",
        "senders": [
            "@amazon",
            "@ebay",
            "@aliexpress",
            "@rozetka",
            "@shein",
            "@asos",
            "@zara",
            "@hm.com",
            "@ikea",
        ],
    },
    # Banks IL
    "bank": {
        "keywords": [
            "transaction",
            "העברה",
            "יתרה",
            "חיוב",
            "זיכוי",
            "כרטיס אשראי",
            "bank",
            "בנק",
            "פעולה",
        ],
        "icon": "🏦",
        "senders": [
            "@bankhapoalim",
            "@poalim",
            "@leumi",
            "@discountbank",
            "@mizrahi-tefahot",
            "@fibi",
            "@isracard",
            "@max.co.il",
            "@cal-online",
            "@visa",
            "@mastercard",
        ],
    },
    # Government IL
    "gov": {
        "keywords": [
            "gov.il",
            "ביטוח לאומי",
            "משרד הפנים",
            "מס הכנסה",
            "עירייה",
            "מינהל",
            "רשות",
            "משרד",
        ],
        "icon": "🏛️",
        "senders": [
            "@gov.il",
            "@btl.gov.il",
            "@taxes.gov.il",
            "@justice.gov.il",
            "@health.gov.il",
            "@moin.gov.il",
        ],
    },
    "family": {
        "keywords": ["family", "invite", "приглашение", "семейная группа", "gorode"],
        "icon": "🏠",
        "senders": ["families-noreply@google.com"],
    },
    # Payments IL
    "payment": {
        "keywords": ["bit", "paybox", "pepper", "העברה", "קיבלת", "שילמת", "תשלום"],
        "icon": "💳",
        "senders": ["@bit.co.il", "@paybox", "@pepper.co.il", "@paypal", "@wise.com"],
    },
    # Tech/Dev
    "github": {
        "keywords": [
            "github",
            "pull request",
            "commit",
            "repository",
            "issue",
            "merge",
        ],
        "icon": "🐙",
        "senders": ["@github.com", "@gitlab", "gitguardian"],
    },
    "security": {
        "keywords": ["security alert", "incident detected", "breach", "vulnerability", "утечка", "секрет", "обнаружен"],
        "icon": "👮",
        "senders": ["gitguardian", "@auth", "security"],
    },
    "linkedin": {
        "keywords": ["linkedin", "connection", "invitation", "network", "job alert"],
        "icon": "💼",
        "senders": ["@linkedin.com"],
    },
    # Low priority
    "spam": {
        "keywords": [
            "unsubscribe",
            "lottery",
            "winner",
            "prize",
            "click here",
            "спам",
            "הסר מרשימה",
        ],
        "icon": "⚪",
        "senders": [],
    },
}


def get_gmail_service():
    """
    Authenticate and return Gmail API service
    Аутентификация и возврат сервиса Gmail API
    """
    creds = None

    # Load existing token (JSON format - migrated from pickle for security)
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print("❌ Gmail credentials not found!")
                print("Please download OAuth2 credentials from Google Cloud Console")
                print(f"And save to: {CREDENTIALS_PATH}")
                print("\nSteps:")
                print("1. Go to: https://console.cloud.google.com/apis/credentials")
                print("2. Create OAuth 2.0 Client ID (Desktop app)")
                print("3. Download JSON")
                print(f"4. Save as: {CREDENTIALS_PATH}")
                sys.exit(1)

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials as JSON (secure format)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def categorize_email(subject, body, sender):
    """
    Categorize email based on sender and content
    Категоризация письма на основе отправителя и содержимого

    Priority: sender patterns > keywords
    """
    sender_lower = sender.lower()

    # Check sender patterns first (more reliable)
    for category, data in CATEGORIES.items():
        senders = data.get("senders", [])
        for sender_pattern in senders:
            if sender_pattern in sender_lower:
                return category

    # Then check keywords in content
    content = f"{subject} {body}".lower()
    for category, data in CATEGORIES.items():
        for keyword in data["keywords"]:
            if keyword in content:
                return category

    return "info"


def send_telegram_alert(category, subject, sender, body_preview):
    """
    Send a notification to Telegram based on category priority
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("⚠️ Telegram credentials not found, skipping alert")
        return

    # Define icons and alerts
    priority_map = {
        "urgent": "🚨 URGENT",
        "work": "💼 WORK",
        "family": "🏠 FAMILY",
        "security": "👮 SECURITY", # New category for gitguardian etc
        "github": "🐙 GIT",
        "payment": "💰 MONEY"
    }

    # Only alert for specific categories
    if category not in priority_map:
        return

    header = priority_map[category]

    import html

    # Construct message
    safe_sender = html.escape(sender)
    safe_subject = html.escape(subject)
    safe_preview = html.escape(body_preview[:100])

    message = (
        f"{header}\n\n"
        f"<b>From:</b> {safe_sender}\n"
        f"<b>Subject:</b> {safe_subject}\n"
        f"<i>{safe_preview}...</i>"
    )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print(f"✈️ Telegram alert sent for: {subject[:30]}...")
        else:
            print(f"⚠️ Failed to send Telegram alert: {response.text}")
    except Exception as e:
        print(f"⚠️ Error sending Telegram alert: {e}")



def send_email(service, to, subject, body):
    """
    Send an email
    Отправить письмо
    """
    try:
        message = MIMEText(body)
        message["to"] = to
        message["from"] = "me"
        message["subject"] = subject

        raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        body = {"raw": raw}

        message = service.users().messages().send(userId="me", body=body).execute()
        print(f"✅ Email sent to {to} (ID: {message['id']})")
        return message
    except HttpError as error:
        print(f"❌ Error sending email: {error}")
        return None


def get_unread_emails(service, max_results=50):
    """
    Get all unread emails
    Получить все непрочитанные письма
    """
    return get_recent_emails(
        service, hours=24 * 7, max_results=max_results, query="is:unread"
    )


def get_recent_emails(service, hours=24, max_results=50, query=None):
    """
    Get emails from last N hours or custom query
    Получить письма за последние N часов или по запросу
    """
    try:
        if not query:
            # Calculate timestamp
            since = datetime.now() - timedelta(hours=hours)
            query = f"after:{int(since.timestamp())}"

        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=max_results)
            .execute()
        )

        messages = results.get("messages", [])

        emails = []
        for msg in messages:
            try:
                email_data = (
                    service.users()
                    .messages()
                    .get(userId="me", id=msg["id"], format="full")
                    .execute()
                )

                headers = email_data["payload"]["headers"]
                subject = next(
                    (h["value"] for h in headers if h["name"] == "Subject"),
                    "No Subject",
                )
                sender = next(
                    (h["value"] for h in headers if h["name"] == "From"), "Unknown"
                )
                date = next((h["value"] for h in headers if h["name"] == "Date"), "")

                # Get body
                body = ""
                if "parts" in email_data["payload"]:
                    for part in email_data["payload"]["parts"]:
                        if part["mimeType"] == "text/plain":
                            if "data" in part["body"]:
                                body = base64.urlsafe_b64decode(
                                    part["body"]["data"]
                                ).decode("utf-8")
                                break
                elif (
                    "body" in email_data["payload"]
                    and "data" in email_data["payload"]["body"]
                ):
                    body = base64.urlsafe_b64decode(
                        email_data["payload"]["body"]["data"]
                    ).decode("utf-8")

                # Categorize
                body_preview = body[:200] if body else ""
                category = categorize_email(subject, body[:500], sender)

                emails.append(
                    {
                        "id": msg["id"],
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "category": category,
                        "body_preview": body_preview,
                    }
                )

                # Send Alert immediately for fresh emails
                send_telegram_alert(category, subject, sender, body_preview)

            except Exception as e:
                print(f"⚠️ Error processing message {msg['id']}: {e}")
                continue

        return emails

    except HttpError as error:
        print(f"❌ Error fetching emails: {error}")
        return []


def save_email_database(emails):
    """
    Save emails to database
    Сохранить письма в базу данных
    """
    EMAIL_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Load existing
    if EMAIL_DB_PATH.exists():
        with open(EMAIL_DB_PATH) as f:
            db = json.load(f)
    else:
        db = {"emails": [], "last_check": None}

    # Add new emails (avoid duplicates)
    existing_ids = {e["id"] for e in db["emails"]}
    new_emails = [e for e in emails if e["id"] not in existing_ids]

    db["emails"].extend(new_emails)
    db["last_check"] = datetime.now().isoformat()

    with open(EMAIL_DB_PATH, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)

    return len(new_emails)


def print_email_summary(emails):
    """
    Print summary of emails by category
    Вывести сводку писем по категориям
    """
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║   Gmail Automation Agent - Email Summary                    ║")
    print("║   Агент автоматизации Gmail - Сводка писем                  ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Count by category
    stats = {}
    for email in emails:
        cat = email["category"]
        stats[cat] = stats.get(cat, 0) + 1

    print("📊 Email Statistics | Статистика писем:")
    print()
    for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        icon = CATEGORIES.get(category, {}).get("icon", "📧")
        print(f"  {icon} {category.title()}: {count}")

    print()
    print(f"Total: {len(emails)} emails")
    print()

    # Show urgent emails
    urgent = [e for e in emails if e["category"] == "urgent"]
    if urgent:
        print("🔴 URGENT EMAILS:")
        print()
        for email in urgent[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print(f"  Date: {email['date']}")
            print()

    # Show work-related
    work = [e for e in emails if e["category"] == "work"]
    if work:
        print("💼 WORK-RELATED:")
        print()
        for email in work[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print()

    # Show shopping
    shopping = [e for e in emails if e["category"] == "shopping"]
    if shopping:
        print("🛒 SHOPPING / ORDERS:")
        print()
        for email in shopping[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print()

    # Show bank notifications
    bank = [e for e in emails if e["category"] == "bank"]
    if bank:
        print("🏦 BANK NOTIFICATIONS:")
        print()
        for email in bank[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print()

    # Show government notifications
    gov = [e for e in emails if e["category"] == "gov"]
    if gov:
        print("🏛️ GOVERNMENT / GOV.IL:")
        print()
        for email in gov[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print()

    # Show payment notifications
    payment = [e for e in emails if e["category"] == "payment"]
    if payment:
        print("💳 PAYMENTS (Bit/PayBox/etc):")
        print()
        for email in payment[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print()


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Gmail Automation Agent")
    parser.add_argument("--unread", action="store_true", help="Fetch all unread emails")
    parser.add_argument("--send-to", help="Send email to address")
    parser.add_argument("--subject", help="Subject for email sending")
    parser.add_argument("--body", help="Body for email sending")

    args = parser.parse_args()

    print("Starting Gmail Automation Agent...")
    print("Запуск агента автоматизации Gmail...")
    print()

    # Get Gmail service
    print("🔐 Authenticating with Gmail...")
    service = get_gmail_service()
    print("✅ Authentication successful!")
    print()

    if args.send_to:
        if not args.subject or not args.body:
            print("❌ --subject and --body required for sending email")
            sys.exit(1)

        print(f"📤 Sending email to {args.send_to}...")
        send_email(service, args.send_to, args.subject, args.body)
        print("✅ Done")
        return

    # Fetch emails
    if args.unread:
        print("📧 Fetching UNREAD emails...")
        emails = get_unread_emails(service)
    else:
        print("📧 Fetching recent emails (last 24 hours)...")
        emails = get_recent_emails(service, hours=24)

    print(f"✅ Found {len(emails)} emails")
    print()

    if emails:
        # Save to database
        new_count = save_email_database(emails)
        print(f"💾 Saved {new_count} new emails to database")
        print()

        # Print summary
        print_email_summary(emails)

        # Save log
        log_file = BASE_DIR / "logs" / "automation" / "gmail_agent.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(log_file, "a") as f:
            f.write(
                f"{datetime.now().isoformat()} - Processed {len(emails)} emails ({new_count} new) [Mode: {'Unread' if args.unread else 'Recent'}]\n"
            )
    else:
        print("ℹ️  No new emails found")

    print()
    print("═══════════════════════════════════════════════════════════════")
    print("✅ Gmail Automation Agent completed successfully")
    print("✅ Агент автоматизации Gmail завершен успешно")
    print("═══════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
