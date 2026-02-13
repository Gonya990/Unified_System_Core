import os

import requests
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
load_dotenv(dotenv_path)

AGENT_MAIL_SERVER = os.getenv("AGENT_MAIL_SERVER", "http://igor-gaming-1:8765")
AGENT_MAIL_TOKEN = os.getenv("AGENT_MAIL_TOKEN")


def check_inbox(server_url):
    print(f"🔍 Checking inbox at {server_url}...")
    url = f"{server_url.rstrip('/')}/messages/inbox"
    headers = {"Authorization": f"Bearer {AGENT_MAIL_TOKEN}"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        messages = response.json()

        print(f"📬 Found {len(messages)} messages in inbox.")
        for msg in messages:
            print(f"\n--- Message ID: {msg.get('id')} ---")
            print(f"From: {msg.get('from_agent_id')}")
            print(f"Subject: {msg.get('subject')}")
            print(f"Body: {msg.get('body')}")
        return True
    except Exception as e:
        print(f"❌ Error at {server_url}: {e}")
        return False


if __name__ == "__main__":
    if not check_inbox(AGENT_MAIL_SERVER):
        # Fallback to the working Windows Tailscale IP
        IP_SERVER = "http://100.126.23.67:8765"
        print(f"🔄 Retrying with IP fallback: {IP_SERVER}")
        check_inbox(IP_SERVER)
