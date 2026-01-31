import sys
from pathlib import Path

# Add current dir to path to import gmail_agent
sys.path.append(str(Path.cwd() / "Scripts/automation"))
import gmail_agent


def search_takeout():
    print("🔍 Authenticating...")
    service = gmail_agent.get_gmail_service()

    print("🔍 Searching for 'Google Takeout' emails...")
    # Search specifically for takeout emails
    emails = gmail_agent.get_recent_emails(service, hours=24*30, max_results=10, query="from:google.com subject:Takeout")

    found_links = []

    for email in emails:
        print(f"\n📧 Found Email: {email['subject']} ({email['date']})")
        # Need to fetch full body again or rely on preview? Agent fetches full body.
        # But categorization truncates. Let's fetch full message content here just to be sure
        try:
             # Re-fetch full for link extraction if needed, but 'body_preview' might be too short.
             # We will use the service directly to get full text
             msg = service.users().messages().get(userId="me", id=email['id'], format="full").execute()
             snippet = msg.get('snippet', '')
             print(f"   Snippet: {snippet}")

             # Simple checking in snippet or body preview from previous call is risky.
             # Let's simple check if we can find a drive folder link or takeout download link
        except Exception as e:
            print(f"Error fetching detail: {e}")

    if not emails:
        print("❌ No recent Takeout emails found.")

if __name__ == "__main__":
    search_takeout()
