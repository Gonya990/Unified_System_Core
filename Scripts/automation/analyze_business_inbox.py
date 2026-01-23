
import os
import sys
import json
import base64
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

import openai
from dotenv import load_dotenv

# Gmail imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Configuration ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# Load .env from AI_Core where key is working
ENV_PATH = BASE_DIR / "Projects" / "AI_Core" / ".env"
load_dotenv(ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4o"

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

def analyze_and_draft_responses(emails: List[Dict]):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    
    analyzed_data = []

    print(f"🧠 Analyzing {len(emails)} emails with {OPENAI_MODEL}...")

    for i, email in enumerate(emails):
        print(f"[{i+1}/{len(emails)}] Processing: {email['subject'][:40]}...")
        
        prompt = f"""
        You are a strategic business development consultant. Analyze this email.
        
        SENDER: {email['sender']}
        SUBJECT: {email['subject']}
        BODY_SNIPPET: {email['body'][:4000]}
        
        Task:
        Identify if this email contains a **LEAD** (a company or person we can pitch to).
        
        Treat the following as RELEVANT LEADS:
        1. **Direct Business Emails**: Investors, partners, clients.
        2. **High-Level Job Alerts**: Roles like "Director", "Executive", "Manager", "Supervisor", "Operations". 
           -> STRATEGY: Instead of applying as an employee, pitch a B2B consulting arrangement or "Fractional Executive" service.
        3. **Application Acknowledgements**: "Thanks for applying to Google/Cust2Mate".
           -> STRATEGY: Follow up with a "Value-Add Proposal" (Startup Plan) to stand out.
           
        Ignore:
        - Social media notifications (Instagram, Reddit).
        - purely automated system alerts (GitHub incidents, security codes).
        - Span/Promotions.
        
        If RELEVANT, output JSON:
        {{
            "is_relevant": true,
            "company_name": "Name of company found",
            "reason": "e.g. High-level role at Cust2Mate",
            "reply_draft": "Professional email pitching a B2B/Consulting arrangement instead of just a job application. Focus on delivering immediate ROI.",
            "strategy": {{
                "plan": "Brief startup/rollout plan for this specific role/company",
                "roi": "Estimated ROI keypoints (e.g. 'Reduce operational costs by 20% via AI automation')",
                "action": "Find decision maker on LinkedIn and send this pitch"
            }}
        }}
        
        If NOT relevant, output: {{"is_relevant": false}}
        """

        try:
            response = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            analysis = json.loads(content)
            
            if analysis.get("is_relevant"):
                analyzed_data.append({
                    "original": email,
                    "analysis": analysis
                })
        except Exception as e:
            print(f"⚠️ Analysis error: {e}")

    return analyzed_data

# --- Main Flow ---

def main():
    print("🚀 Starting Business Email Analysis...")
    
    # 1. Fetch Emails
    service = get_gmail_service()
    
    # Last 30 days
    date_query = (datetime.now() - timedelta(days=30)).strftime("%Y/%m/%d")
    query = f"after:{date_query}"
    # Filter out common bulk senders to save AI tokens roughly (can refine later)
    query += " -category:promotions -category:social"
    
    print(f"📥 Fetching emails since {date_query}...")
    
    messages = []
    next_page_token = None
    target_count = 300
    
    while len(messages) < target_count:
        results = service.users().messages().list(
            userId="me", 
            q=query, 
            maxResults=min(100, target_count - len(messages)), 
            pageToken=next_page_token
        ).execute()
        
        batch = results.get("messages", [])
        messages.extend(batch)
        next_page_token = results.get("nextPageToken")
        
        print(f"   Fetched {len(messages)} messages...")
        if not next_page_token or not batch:
            break
            
    print(f"Found {len(messages)} recent emails.")
    
    email_list = []
    
    # Process mostly the newest ones first
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
                email_list.append({
                    "id": msg["id"],
                    "subject": subject,
                    "sender": sender,
                    "date": date,
                    "body": body
                })
        except Exception as e:
            print(f"Error fetching msg {msg['id']}: {e}")

    # 2. Analyze
    if not email_list:
        print("No emails found.")
        return

    results = analyze_and_draft_responses(email_list)
    
    # 3. Report
    print(f"📝 Generating Report for {len(results)} relevant threads...")
    
    with open(REPORT_FILE, "w") as f:
        f.write(f"# Business Response Plan\n")
        f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        for item in results:
            orig = item["original"]
            anl = item["analysis"]
            strat = anl.get("strategy", {})
            
            f.write(f"## 📧 {orig['sender']}\n")
            f.write(f"**Subject:** {orig['subject']}\n\n")
            f.write(f"**Relevance:** {anl.get('reason')}\n\n")
            
            f.write(f"### 🎯 Strategy\n")
            f.write(f"- **Plan:** {strat.get('plan')}\n")
            f.write(f"- **ROI/Benefit:** {strat.get('roi')}\n")
            f.write(f"- **Action:** {strat.get('action')}\n\n")
            
            f.write(f"### ✍️ Draft Reply\n")
            f.write(f"```text\n{anl.get('reply_draft')}\n```\n")
            f.write(f"---\n\n")
            
    print(f"✅ Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()
