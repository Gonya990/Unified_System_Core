import os
import sys

import requests

# Load from env or hardcode from artifact if needed (using passed arg for safety)
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")  # Set via env var
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")   # Set via env var

if len(sys.argv) > 1:
    TOKEN = sys.argv[1]

print(f"DEBUG: Testing Token (len={len(TOKEN)})")

url = f"https://api.telegram.org/bot{TOKEN}/getMe"
try:
    resp = requests.get(url, timeout=10)
    print(f"getMe Status: {resp.status_code}")
    print(f"getMe Body: {resp.text}")

    if resp.status_code == 200:
        bot_venom = resp.json()
        print(f"Bot Name: {bot_venom['result']['username']}")

        # Try sending message
        msg_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": "🤖 DEBUG: Connection Restored. I am listening."}
        res_msg = requests.post(msg_url, json=payload)
        print(f"SendMsg Status: {res_msg.status_code}")
except Exception as e:
    print(f"Error: Could not connect to Telegram API: {e}")
