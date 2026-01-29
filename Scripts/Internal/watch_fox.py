
import json
import logging
import os
import sqlite3
import time
from datetime import datetime

import requests

# Configuration
MCP_URL = 'http://localhost:8765/mcp'
TOKEN = 'c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb' # Vibranium Secret
PROJECT_KEY = '/home/gonya/Unified_System'
MY_AGENT = 'OrangeStone'
TARGET_AGENTS = ['FuchsiaCat', 'VioletCastle']

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Determine paths based on environment
if os.path.exists("/home/gonya/Unified_System"):
    BASE_PATH = "/home/gonya/Unified_System"
else:
    BASE_PATH = ROOT_DIR

# DB Path for Approvals
DB_PATH = os.path.join(BASE_PATH, "Projects/AI_Core/user_context.db")

# Ensure log directory exists
LOG_FILE = os.path.join(BASE_PATH, "logs/fox_watch.log")
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

def call_mcp(method, params):
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "id": int(time.time()),
        "params": params
    }
    try:
        # Note: Localhost because service is on same node
        res = requests.post(MCP_URL, json=payload, headers={'Authorization': f'Bearer {TOKEN}'}, timeout=15)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def request_telegram_approval(sender, subject, body):
    """Adds a request to the DB for the Telegram Bot to pick up."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            summary = f"**Subject:** {subject}\n\n**Body:** {body[:200]}..."
            payload = {
                "sender": sender,
                "subject": subject,
                "body": body,
                "summary": summary
            }
            cursor.execute('''
                INSERT INTO pending_approvals (requester_agent, task_type, task_payload, created_at)
                VALUES (?, ?, ?, ?)
            ''', (sender, "mail_action", json.dumps(payload), datetime.now()))
            conn.commit()
            logging.info(f"📤 Approval requested via Telegram for message from {sender}")
    except Exception as e:
        logging.error(f"Failed to request Telegram approval: {e}")

def main():
    logging.info("🦊 FoxWatch 3.0 (Telegram Hybrid) initiated.")

    while True:
        try:
            # 1. Check Inbox for new messages
            resp = call_mcp("tools/call", {
                "name": "fetch_inbox",
                "arguments": {
                    "project_key": PROJECT_KEY,
                    "agent_name": MY_AGENT
                }
            })

            if "error" in resp:
                logging.error(f"MCP Connection error: {resp['error']}")
                time.sleep(60)
                continue

            result = resp.get('result', {})
            content_str = result.get('content', [{}])[0].get('text', '[]')
            try:
                messages = json.loads(content_str)
            except Exception:
                messages = []

            for msg in messages:
                sender = msg.get('from', '')
                is_read = msg.get('read', False)
                msg_id = msg.get('id')

                if sender in TARGET_AGENTS and not is_read:
                    logging.info(f"🚨 New incoming mail from {sender} (ID: {msg_id})")

                    # Fetch full message details to get body
                    # Using resources if tool is missing
                    # Actually, let's just use the subject/metadata for now or try to get body

                    # Request Telegram Approval instead of auto-replying everything
                    request_telegram_approval(sender, msg.get('subject'), "Full body processing...")

                    # Mark as read immediately to stop polling it
                    call_mcp("tools/call", {
                        "name": "mark_message_read",
                        "arguments": {
                            "project_key": PROJECT_KEY,
                            "agent_name": MY_AGENT,
                            "message_id": msg_id
                        }
                    })

            # 2. Check for APPROVED tasks to execute
            # (In the future, we can add logic here to trigger syncs or replies)

        except Exception as e:
            logging.error(f"Loop error: {e}")

        time.sleep(45) # Check every 45 seconds

if __name__ == "__main__":
    main()
