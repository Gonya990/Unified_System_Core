import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

TOKEN_PATH = "Scripts/automation/.credentials/gmail_token.json"

def main():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH)
    service = build("gmail", "v1", credentials=creds)

    # 19bb6cf890f576eb is the ID from the tail output earlier?
    # Let me search by subject instead
    query = "subject:\"Run failed: Build and Push Container\""
    results = service.users().messages().list(userId="me", q=query, maxResults=1).execute()
    messages = results.get("messages", [])

    if messages:
        mid = messages[0]["id"]
        data = service.users().messages().get(userId="me", id=mid).execute()
        payload = data["payload"]

        def get_text(p):
            if "body" in p and "data" in p["body"]:
                return base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8", errors="ignore")
            if "parts" in p:
                for part in p["parts"]:
                    t = get_text(part)
                    if t: return t
            return ""

        body = get_text(payload)
        print(body)

if __name__ == "__main__":
    main()
