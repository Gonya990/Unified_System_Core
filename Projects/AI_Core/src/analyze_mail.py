import json
import logging
import sqlite3
import sys
from collections import Counter

# Add src to path
sys.path.append("/app/src")
sys.path.append("/app")

from gmail_client import GmailClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_mail(user_id=708531393, count=300):
    db_path = "/app/user_context.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT google_creds FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()

    if not row or not row["google_creds"]:
        print("No credentials found")
        return

    creds_dict = json.loads(row["google_creds"])
    client = GmailClient(credentials_dict=creds_dict)

    print(f"Searching last {count} emails...")

    # Search specific vacancy keywords + general recent
    query = "newer_than:60d (vacancy OR job OR position OR hiring OR recruiter OR HR OR work OR career OR 'דרושים' OR 'משרה')"
    # query = "newer_than:60d" # Just recent

    messages = client.search_emails(query, max_results=count)

    print(f"Found {len(messages)} messages.")

    subjects = []
    senders = []
    snippets = []

    for msg in messages:
        subjects.append(msg["subject"])
        senders.append(msg["from"])
        snippets.append(msg["snippet"])

    # Analyze keywords
    text = " ".join(subjects + snippets).lower()

    # Basic keyword extraction (very simple)
    ignore = {
        "re:",
        "fwd:",
        "the",
        "and",
        "to",
        "for",
        "in",
        "of",
        "a",
        "is",
        "on",
        "with",
        "your",
        "new",
        "job",
        "vacancy",
        "alert",
        "application",
        "opportunity",
        "hiring",
        "position",
    }
    words = [w.strip(".,!-") for w in text.split() if w.strip(".,!-") not in ignore and len(w) > 3]

    common = Counter(words).most_common(50)

    print("\nTOP KEYWORDS IN EMAILS:")
    for w, c in common:
        print(f"{w}: {c}")

    print("\nSAMPLE SUBJECTS:")
    for s in subjects[:10]:
        print(f"- {s}")


if __name__ == "__main__":
    analyze_mail()
