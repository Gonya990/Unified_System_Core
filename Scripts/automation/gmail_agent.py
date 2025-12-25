#!/usr/bin/env python3
"""
Gmail Automation Agent
Агент автоматизации Gmail

Automatically monitors and processes emails from gonya90.gg@gmail.com
Автоматически мониторит и обрабатывает письма с gonya90.gg@gmail.com
"""

import os
import sys
import json
import pickle
import base64
from datetime import datetime, timedelta
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail API imports
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Gmail API libraries not installed!")
    print("Install with: pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)

# Scopes for Gmail API
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify'
]

# Paths
BASE_DIR = Path("/Users/macbook/Documents/Unified_System")
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
CREDS_DIR.mkdir(parents=True, exist_ok=True)

TOKEN_PATH = CREDS_DIR / "gmail_token.pickle"
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
EMAIL_DB_PATH = BASE_DIR / "logs" / "automation" / "email_database.json"

# Email categories
CATEGORIES = {
    "urgent": {"keywords": ["urgent", "asap", "important", "срочно", "важно", "דחוף"], "icon": "🔴"},
    "work": {"keywords": ["interview", "job", "position", "vacancy", "работа", "вакансия", "משרה"], "icon": "💼"},
    "github": {"keywords": ["github", "pull request", "commit", "repository"], "icon": "🐙"},
    "linkedin": {"keywords": ["linkedin", "connection", "invitation", "network"], "icon": "💼"},
    "spam": {"keywords": ["unsubscribe", "lottery", "winner", "prize", "click here", "спам"], "icon": "⚪"}
}


def get_gmail_service():
    """
    Authenticate and return Gmail API service
    Аутентификация и возврат сервиса Gmail API
    """
    creds = None
    
    # Load existing token
    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    
    # Refresh or create new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print("❌ Gmail credentials not found!")
                print(f"Please download OAuth2 credentials from Google Cloud Console")
                print(f"And save to: {CREDENTIALS_PATH}")
                print("\nSteps:")
                print("1. Go to: https://console.cloud.google.com/apis/credentials")
                print("2. Create OAuth 2.0 Client ID (Desktop app)")
                print("3. Download JSON")
                print(f"4. Save as: {CREDENTIALS_PATH}")
                sys.exit(1)
            
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_PATH), SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('gmail', 'v1', credentials=creds)


def categorize_email(subject, body, sender):
    """
    Categorize email based on content
    Категоризация письма на основе содержимого
    """
    content = f"{subject} {body} {sender}".lower()
    
    for category, data in CATEGORIES.items():
        for keyword in data["keywords"]:
            if keyword in content:
                return category
    
    return "info"


def get_recent_emails(service, hours=24, max_results=50):
    """
    Get emails from last N hours
    Получить письма за последние N часов
    """
    try:
        # Calculate timestamp
        since = datetime.now() - timedelta(hours=hours)
        query = f"after:{int(since.timestamp())}"
        
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=max_results
        ).execute()
        
        messages = results.get('messages', [])
        
        emails = []
        for msg in messages:
            email_data = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='full'
            ).execute()
            
            headers = email_data['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            date = next((h['value'] for h in headers if h['name'] == 'Date'), '')
            
            # Get body
            body = ''
            if 'parts' in email_data['payload']:
                for part in email_data['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        if 'data' in part['body']:
                            body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                            break
            elif 'body' in email_data['payload'] and 'data' in email_data['payload']['body']:
                body = base64.urlsafe_b64decode(email_data['payload']['body']['data']).decode('utf-8')
            
            # Categorize
            category = categorize_email(subject, body[:500], sender)
            
            emails.append({
                'id': msg['id'],
                'subject': subject,
                'sender': sender,
                'date': date,
                'category': category,
                'body_preview': body[:200] if body else ''
            })
        
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
        with open(EMAIL_DB_PATH, 'r') as f:
            db = json.load(f)
    else:
        db = {"emails": [], "last_check": None}
    
    # Add new emails (avoid duplicates)
    existing_ids = {e['id'] for e in db['emails']}
    new_emails = [e for e in emails if e['id'] not in existing_ids]
    
    db['emails'].extend(new_emails)
    db['last_check'] = datetime.now().isoformat()
    
    with open(EMAIL_DB_PATH, 'w') as f:
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
        cat = email['category']
        stats[cat] = stats.get(cat, 0) + 1
    
    print("📊 Email Statistics | Статистика писем:")
    print()
    for category, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        icon = CATEGORIES.get(category, {}).get('icon', '📧')
        print(f"  {icon} {category.title()}: {count}")
    
    print()
    print(f"Total: {len(emails)} emails")
    print()
    
    # Show urgent emails
    urgent = [e for e in emails if e['category'] == 'urgent']
    if urgent:
        print("🔴 URGENT EMAILS:")
        print()
        for email in urgent[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print(f"  Date: {email['date']}")
            print()
    
    # Show work-related
    work = [e for e in emails if e['category'] == 'work']
    if work:
        print("💼 WORK-RELATED:")
        print()
        for email in work[:5]:
            print(f"  From: {email['sender']}")
            print(f"  Subject: {email['subject']}")
            print()


def main():
    """Main execution"""
    print("Starting Gmail Automation Agent...")
    print("Запуск агента автоматизации Gmail...")
    print()
    
    # Get Gmail service
    print("🔐 Authenticating with Gmail...")
    service = get_gmail_service()
    print("✅ Authentication successful!")
    print()
    
    # Fetch recent emails
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
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now().isoformat()} - Processed {len(emails)} emails ({new_count} new)\n")
    else:
        print("ℹ️  No new emails found")
    
    print()
    print("═══════════════════════════════════════════════════════════════")
    print("✅ Gmail Automation Agent completed successfully")
    print("✅ Агент автоматизации Gmail завершен успешно")
    print("═══════════════════════════════════════════════════════════════")


if __name__ == "__main__":
    main()
