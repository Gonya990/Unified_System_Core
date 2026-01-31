
import base64
import re
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

def parse_report_and_create_drafts():
    if not REPORT_PATH.exists():
        print(f"Report not found at {REPORT_PATH}")
        return

    with open(REPORT_PATH) as f:
        content = f.read()

    # Split by email sections
    sections = content.split("## 📧")[1:]

    print(f"Found {len(sections)} sections to process.")

    service = get_gmail_service()

    count = 0
    for section in sections:
        try:
            # Extract Subject
            # Look for **Subject:** ...
            subj_match = re.search(r'\*\*Subject:\*\*\s*(.*)', section)
            orig_subject = subj_match.group(1).strip() if subj_match else "Business Proposal"

            # Extract Relevance/Company for better Subject line
            rel_match = re.search(r'\*\*Relevance:\*\*\s*(.*)', section)
            relevance = rel_match.group(1).strip() if rel_match else ""

            # Smart Subject Line
            # If original subject is "30+ new jobs", we want "Strategic Partnership Proposal" instead.
            smart_subject = f"Strategic Collaboration: {orig_subject}"
            if "30+ new jobs" in orig_subject or "new jobs" in orig_subject:
                # Try to find role/company in relevance
                smart_subject = f"Consulting Proposal: {relevance}"
            elif "Director" in orig_subject or "manager" in orig_subject.lower():
                smart_subject = f"Optimization Proposal: {orig_subject}"

            # Extract Body (Draft Reply)
            # Find content between ```text and ```
            body_match = re.search(r'```text\n(.*?)\n```', section, re.DOTALL)
            if body_match:
                email_body = body_match.group(1).strip()
            else:
                print(f"⚠️ No draft text found for section starting with: {section[:50]}...")
                continue

            # Create Draft
            # Clean up smart subject to be reasonable length
            if len(smart_subject) > 80:
                smart_subject = smart_subject[:77] + "..."

            # Try to guess company name for placeholder
            # Rough heuristic: look for "at [Company]" in relevance
            company = "CONTACT"
            if "at " in relevance:
                company = relevance.split("at ")[1].split(" ")[0].upper()

            placeholder = f"[{company}_RECRUITER_EMAIL]"

            create_draft(service, smart_subject, email_body, placeholder)
            count += 1

        except Exception as e:
            print(f"Error processing section: {e}")

    print(f"\n🎉 Successfully created {count} drafts.")

if __name__ == "__main__":
    parse_report_and_create_drafts()
