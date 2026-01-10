#!/usr/bin/env python3
"""
Fetch Emails from Last 4 Months for Analysis
"""

import os
import sys
import json

# SECURITY: Using JSON instead of pickle for OAuth tokens (US-psm.1)
import base64
import time
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
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_email_body(payload):
    body = ""
    if "body" in payload and payload["body"].get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode(
            "utf-8", errors="ignore"
        )

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                if part["body"].get("data"):
                    return base64.urlsafe_b64decode(part["body"]["data"]).decode(
                        "utf-8", errors="ignore"
                    )
            elif part["mimeType"] == "text/html":
                # We might want HTML for parsing links/emails better, but keep simple for now
                pass
            elif part["mimeType"].startswith("multipart/"):
                found_body = get_email_body(part)
                if found_body:
                    return found_body
    return body


def main():
    print("Authenticating...")
    service = get_gmail_service()

    # Calculate date 4 months ago
    four_months_ago = datetime.now() - timedelta(days=120)
    query_date = four_months_ago.strftime("%Y/%m/%d")
    query = f"after:{query_date}"

    print(f"Fetching emails since {query_date}...")

    messages = []
    next_page_token = None

    # Pagination loop
    while True:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, pageToken=next_page_token, maxResults=500)
            .execute()
        )
        new_messages = results.get("messages", [])
        messages.extend(new_messages)
        next_page_token = results.get("nextPageToken")
        print(f"Fetched {len(messages)} message IDs so far...")
        if not next_page_token:
            break

    print(f"Total messages to process: {len(messages)}")

    email_data = []

    # Process messages in batches to show progress
    for i, msg in enumerate(messages):
        try:
            full_msg = (
                service.users()
                .messages()
                .get(userId="me", id=msg["id"], format="full")
                .execute()
            )
            payload = full_msg.get("payload", {})
            headers = payload.get("headers", [])

            subject = next(
                (h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)"
            )
            sender = next(
                (h["value"] for h in headers if h["name"] == "From"), "(Unknown)"
            )
            date = next((h["value"] for h in headers if h["name"] == "Date"), "")

            body = get_email_body(payload)
            snippet = full_msg.get("snippet", "")
            content = body if body else snippet

            # Filter optimization: Only save if it looks like a job email to save space/time?
            # User wants DEEP scan. Let's filter slightly for keywords to keep JSON manageable
            # OR just save everything relevant.
            # Given the request, let's look for keywords NOW to avoid massive files.

            combined_text = (subject + " " + sender + " " + content).lower()
            keywords = [
                "job",
                "vacancy",
                "hiring",
                "opportunity",
                "career",
                "resume",
                "apply",
                "משרה",
                "דרוש",
                "גיוס",
                "קורות חיים",
                "עבודה",
                "linkedin",
                "alljobs",
                "glassdoor",
                "indeed",
                "manager",
                "operation",
                "supervisor",
                "technical",
                "site manager",
            ]

            if any(k in combined_text for k in keywords):
                email_data.append(
                    {
                        "id": msg["id"],
                        "subject": subject,
                        "sender": sender,
                        "date": date,
                        "content": content[
                            :2000
                        ],  # Increased limit for better context extraction
                    }
                )

            if (i + 1) % 50 == 0:
                print(f"Processed {i + 1}/{len(messages)}...")

        except Exception as e:
            print(f"Error reading message {msg['id']}: {e}")

    print(f"Saving {len(email_data)} relevant emails to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(email_data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
