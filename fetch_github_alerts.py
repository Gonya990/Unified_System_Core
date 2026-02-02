import base64
import re
import sys
from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

try:
    BASE_DIR = Path(__file__).resolve().parent
    TOKEN_PATH = BASE_DIR / "Scripts" / "automation" / ".credentials" / "gmail_token.json"

    if not TOKEN_PATH.exists():
        print(f"Token not found at {TOKEN_PATH}")
        sys.exit(1)

    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    service = build("gmail", "v1", credentials=creds)

    query = "Gonya990"
    print(f"Searching for query: {query}")
    results = service.users().messages().list(userId="me", q=query, maxResults=5).execute()
    messages = results.get("messages", [])

    print(f"Found {len(messages)} messages")

    for msg in messages:
        mid = msg["id"]
        data = service.users().messages().get(userId="me", id=mid, format="full").execute()
        headers = data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject")
        print(f"\nID: {mid}")
        print(f"Subject: {subject}")

        # Simple body extraction
        parts = [data["payload"]]
        while parts:
            p = parts.pop()
            if "parts" in p:
                parts.extend(p["parts"])
            if "body" in p and "data" in p["body"]:
                text = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8", errors="ignore")
                # Look for URLs
                links = re.findall(r'https://[^\s<>"]+', text)
                for l in links:
                    if "gitguardian" in l or "github.com" in l:
                        print(f"  Link: {l}")
except Exception as e:
    print(f"Error: {e}")
