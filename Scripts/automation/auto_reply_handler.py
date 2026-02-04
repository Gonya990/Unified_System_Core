
import base64
import json
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
REPORT_PATH = BASE_DIR / "Reports" / "BUSINESS_EMAIL_RESPONSE_PLAN.md"
CREDS_DIR = BASE_DIR / "Scripts" / "automation" / ".credentials"
TOKEN_PATH = CREDS_DIR / "gmail_token.json"
CREDENTIALS_PATH = CREDS_DIR / "gmail_credentials.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

# Load Env
load_dotenv(BASE_DIR / "Projects" / "AI_Core" / ".env")

def get_gmail_service():
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # If scopes changed or token missing, might need re-auth
            # But we try to rely on existing token first
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)

def create_draft(service, subject, body, placeholder_to):
    try:
        message = MIMEText(body)
        # message["to"] = placeholder_to # Gmail API rejects invalid content in To header
        # Intentionally leaving 'to' empty so it saves as draft without destination
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        body = {"message": {"raw": raw_message}}

        draft = service.users().drafts().create(userId="me", body=body).execute()
        print(f"✅ Draft created: '{subject}' (ID: {draft['id']})")
        return draft
    except Exception as e:
        print(f"❌ Error creating draft: {e}")
        return None

ACTIONS_FILE = BASE_DIR / "Reports" / "email_actions.json"

def send_email(service, to_email, subject, body_content):
    try:
        message = MIMEText(body_content)
        message["to"] = to_email
        message["subject"] = subject

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

        sent = service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        print(f"🚀 SENT email to {to_email} (ID: {sent['id']})")
        return sent
    except Exception as e:
        print(f"❌ Error sending to {to_email}: {e}")
        return None

def process_actions_and_send():
    if not ACTIONS_FILE.exists():
        print(f"Actions file not found at {ACTIONS_FILE}")
        return

    with open(ACTIONS_FILE) as f:
        actions = json.load(f)

    print(f"Found {len(actions)} actions to process.")

    service = get_gmail_service()

    sent_count = 0
    draft_count = 0

    for item in actions:
        analysis = item.get("analysis", {})
        original = item.get("original", {})

        action_type = analysis.get("action_type", "MANUAL_REVIEW")
        recipient = analysis.get("recipient_email")
        subject = analysis.get("subject", f"Re: {original.get('subject')}")
        body = analysis.get("reply_body", "")

        # Determine if we can auto-send
        can_auto_send = False
        if action_type == "AUTO_SEND" and recipient and "@" in recipient and "noreply" not in recipient:
            can_auto_send = True

        if can_auto_send:
            print(f"📧 Auto-Sending to: {recipient}")
            send_email(service, recipient, subject, body)
            sent_count += 1
        else:
            # Fallback to draft
            reason = "Manual Review Required" if action_type == "MANUAL_REVIEW" else "No valid recipient found"
            print(f"📝 Creating Draft ({reason}) for subject: {subject[:30]}...")

            # Add context to top of draft body for user
            context_header = f"""[AUTO-GENERATED DRAFT]
Reason: {reason}
Suggested Action: {action_type}
Original Sender: {original.get('sender')}
--------------------------------------------------
"""
            create_draft(service, subject, context_header + body, "")
            draft_count += 1

    print("\n🎉 Processing Complete.")
    print(f"   🚀 Sent: {sent_count}")
    print(f"   📝 Drafts: {draft_count}")

if __name__ == "__main__":
    process_actions_and_send()
