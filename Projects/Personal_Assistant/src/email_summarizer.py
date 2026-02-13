import os
import sys

# Robust path handling for local execution
sys.path.append(os.path.expanduser("~/Documents/Unified_System/Projects/AI_Core/src"))
sys.path.append(os.path.expanduser("~/Documents/Unified_System/Scripts/Bridge"))

try:
    from gmail_client import GmailClient
except ImportError:
    # Fallback to current working directory relative path if running from root
    sys.path.append(os.path.abspath("Projects/AI_Core/src"))
    try:
        from gmail_client import GmailClient
    except ImportError as e:
        print(f"❌ Failed to import GmailClient: {e}")
        sys.exit(1)

import json
import sqlite3

import apple_intelligence


def get_gmail_client():
    db_path = os.path.expanduser("~/Documents/Unified_System/Projects/AI_Core/src/user_context.db")
    if not os.path.exists(db_path):
        db_path = os.path.abspath("Projects/AI_Core/src/user_context.db")

    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return None

    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT google_creds FROM users WHERE user_id = 708531393").fetchone()
        if not row:
            return None
        creds = json.loads(row[0])
        return GmailClient(creds)
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None


def main():
    client = get_gmail_client()
    if not client:
        print("❌ No Gmail credentials found.")
        return

    print("📧 Fetching latest email...")
    emails = client.get_recent_emails(max_results=1)
    if not emails:
        print("📭 No emails found.")
        return

    email = emails[0]
    print(f"📄 Processing: {email.get('subject', 'No Subject')}")

    # Fetch full body
    body = client.get_email_body(email["id"])
    if not body:
        body = email.get("snippet", "")

    print("🤖 Sending to Apple Intelligence Bridge...")

    # Try summarize shortcut
    summary = apple_intelligence.trigger_shortcut("Unified_Summarize", body)

    if "Error" in summary or "not found" in summary:
        print("\n⚠️ Apple Intelligence Shortcut 'Unified_Summarize' not found.")
        print(
            "ACTION REQUIRED: Create a Shortcut named 'Unified_Summarize' on your Mac that accepts text input and uses the 'Summarize' action."
        )
        print(f"Debug info: {summary}")
    else:
        print("\n✨ Summary:")
        print(summary)


if __name__ == "__main__":
    main()
