import sys
from pathlib import Path

# Add current dir to path to import gmail_agent
sys.path.append(str(Path.cwd() / "Scripts/automation"))
import gmail_agent


def search_social_takeouts():
    print("🔍 Authenticating...")
    service = gmail_agent.get_gmail_service()

    queries = [
        "from:facebook.com subject:download",
        "from:meta.com subject:download",
        "from:instagram.com subject:download",
        "from:yandex.ru subject:архив",
        "from:mail.ru subject:архив"
    ]

    for query in queries:
        print(f"\n🔍 Searching for: {query}")
        emails = gmail_agent.get_recent_emails(service, hours=24*365, max_results=5, query=query)

        for email in emails:
            print(f"📧 Found: {email['subject']} ({email['date']})")
            # We skip full fetching for now to avoid overhead, just listing titles.

if __name__ == "__main__":
    search_social_takeouts()
