import base64
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

import openai
from dotenv import load_dotenv

# Gmail imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Load .env from AI_Core where key is working
ENV_PATH = BASE_DIR / "Projects" / "AI_Core" / ".env"
load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o-mini"

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
TOKEN_PATH = CREDS_DIR / "gmail_token.json"
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
REPORT_FILE = BASE_DIR / "Reports" / "BUSINESS_EMAIL_RESPONSE_PLAN.md"

# --- Gmail Helpers ---


def get_gmail_service():
    creds = None
    if TOKEN_PATH.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
        except Exception:
            print("⚠️ Token file corrupt or invalid.")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"❌ Token refresh failed: {e}")
                print("PLEASE RUN RE-AUTH.")
                sys.exit(1)
        else:
            print("❌ No valid token found.")
            print("Please run: python3 Scripts/automation/generate_auth_link.py")
            sys.exit(1)

        # Save refreshed token
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def get_email_content(payload) -> str:
    body = ""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                if "data" in part["body"]:
                    body += base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="ignore")
    elif "body" in payload and "data" in payload["body"]:
        body = base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="ignore")
    return body


# --- AI Analysis ---


def analyze_and_draft_responses(emails: list[dict]):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)

    analyzed_data = []

    print(f"🧠 Analyzing {len(emails)} emails with {OPENAI_MODEL}...")

    for i, email in enumerate(emails):
        print(f"[{i + 1}/{len(emails)}] Processing: {email['subject'][:40]}...")

        prompt = f"""
        You are a strategic business development AI.

        SENDER: {email["sender"]}
        SUBJECT: {email["subject"]}
        BODY_SNIPPET: {email["body"][:4000]}

        Task:
        1. Identify if this is a **LEAD** (job alert, direct email, inquiry).
        2. **CLASSIFY** the response type:
           - "AUTO_SEND": Standard pitch, job application follow-up, cold outreach to a job alert. Safe to send automatically if we have an address.
           - "MANUAL_REVIEW": Complex negotiation, sensitive topic, high-stakes investor reply. User must see it first.
           - "IGNORE": Not a business lead.

        3. **EXTRACT RECIPIENT**:
           - Look for a real email address in the body (e.g., "send CV to hr@company.com").
           - If the SENDER is a "noreply" or "notifications" address, you MUST find an email in the body. If none, output null.
           - If the SENDER is a real person/recruiting alias, use that.

        Output JSON:
        {{
            "is_relevant": true,
            "action_type": "AUTO_SEND" or "MANUAL_REVIEW",
            "recipient_email": "extracted_email@domain.com" or null,
            "subject": "optimized subject line",
            "reply_body": "Full professional email body...",
            "reason": "Why this action?",
            "strategy": {{
                "plan": "Step-by-step approach",
                "roi": "Expected benefit"
            }}
        }}

        If NOT relevant: {{"is_relevant": false}}
        """

        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content
            analysis = json.loads(content)

            if analysis.get("is_relevant"):
                analyzed_data.append({"original": email, "analysis": analysis})
        except Exception as e:
            print(f"⚠️ Analysis error: {e}")

    # Save structured data for the auto-responder script
    ACTIONS_FILE = BASE_DIR / "Reports" / "email_actions.json"
    os.makedirs(ACTIONS_FILE.parent, exist_ok=True)
    with open(ACTIONS_FILE, "w") as f:
        json.dump(analyzed_data, f, indent=2)
    print(f"💾 Structured actions saved to {ACTIONS_FILE}")

    return analyzed_data


# --- Main Flow ---


def main():
    print("🚀 Starting Business Email Analysis...")

    # 1. Fetch Emails
    service = get_gmail_service()

    # Last 30 days
    date_query = (datetime.now() - timedelta(days=30)).strftime("%Y/%m/%d")
    query = f"after:{date_query}"
    # Filter out common bulk senders
    query += " -category:promotions -category:social"

    print(f"📥 Fetching emails since {date_query}...")

    messages = []
    next_page_token = None
    target_count = 450

    while len(messages) < target_count:
        results = (
            service.users()
            .messages()
            .list(userId="me", q=query, maxResults=min(100, target_count - len(messages)), pageToken=next_page_token)
            .execute()
        )

        batch = results.get("messages", [])
        messages.extend(batch)
        next_page_token = results.get("nextPageToken")

        print(f"   Fetched {len(messages)} messages...")
        if not next_page_token or not batch:
            break

    print(f"Found {len(messages)} recent emails.")

    email_list = []

    # Process newest ones
    for msg in messages[:target_count]:
        try:
            full = service.users().messages().get(userId="me", id=msg["id"], format="full").execute()
            payload = full.get("payload", {})
            headers = payload.get("headers", [])

            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "(No Subject)")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "(Unknown)")
            date = next((h["value"] for h in headers if h["name"] == "Date"), "")

            body = get_email_content(payload)

            if body:
                email_list.append({"id": msg["id"], "subject": subject, "sender": sender, "date": date, "body": body})
        except Exception as e:
            print(f"Error fetching msg {msg['id']}: {e}")

    # 2. Analyze
    if not email_list:
        print("No emails found.")
        return

    results = analyze_and_draft_responses(email_list)

    # 3. Report
    print(f"📝 Generating Report for {len(results)} relevant threads...")

    os.makedirs(REPORT_FILE.parent, exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        f.write("# Business Response Plan\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")

        for item in results:
            orig = item["original"]
            anl = item["analysis"]
            strat = anl.get("strategy", {})

            f.write(f"## 📧 {orig['sender']}\n")
            f.write(f"**Subject:** {orig['subject']}\n\n")
            f.write(f"**Status:** {anl.get('action_type')}\n")
            f.write(f"**Reason:** {anl.get('reason')}\n\n")

            f.write("### 🎯 Strategy\n")
            f.write(f"- **Plan:** {strat.get('plan')}\n")
            f.write(f"- **ROI/Benefit:** {strat.get('roi')}\n\n")

            f.write("### ✍️ Draft Reply\n")
            f.write(f"```text\n{anl.get('reply_body')}\n```\n")
            f.write("---\n\n")

    print(f"✅ Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
