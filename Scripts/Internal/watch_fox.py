
import time
import requests
import json
import logging
import os

# Configuration
MCP_URL = 'http://localhost:8765/mcp'
TOKEN = 'c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb' # Vibranium Secret
PROJECT_KEY = '/home/gonya/Unified_System'
MY_AGENT = 'OrangeStone'
TARGET_AGENTS = ['FuchsiaCat', 'VioletCastle']

# Ensure log directory exists
LOG_FILE = '/home/gonya/Unified_System/logs/fox_watch.log'
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
        res = requests.post(MCP_URL, json=payload, headers={'Authorization': f'Bearer {TOKEN}'}, timeout=15)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def reply_to_msg(msg_id, sender):
    reply_body = f"""👋 **Vibranium Auto-Response**

OrangeStone (Orchestrator) received your message.
The system is currently in **Vibranium Unified Mode**.
Your input is being processed or queued for the next orchestration cycle.

--
*Sent autonomously by FoxWatch 🦊*"""
    
    return call_mcp("tools/call", {
        "name": "reply_message",
        "arguments": {
            "project_key": PROJECT_KEY,
            "message_id": msg_id,
            "sender_name": MY_AGENT,
            "body_md": reply_body
        }
    })

def mark_read(msg_id):
    return call_mcp("tools/call", {
        "name": "mark_message_read",
        "arguments": {
            "project_key": PROJECT_KEY,
            "agent_name": MY_AGENT,
            "message_id": msg_id
        }
    })

def main():
    logging.info(f"🦊 FoxWatch 2.0 initiated. Listening for {TARGET_AGENTS}...")
    
    while True:
        try:
            # Check Inbox
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
            except:
                messages = []
            
            # Filter for unread messages from targets
            for msg in messages:
                sender = msg.get('from', '')
                is_read = msg.get('read', False)
                msg_id = msg.get('id')
                
                if sender in TARGET_AGENTS and not is_read:
                    logging.info(f"🚨 ALERT! New message from {sender} (ID: {msg_id}): {msg.get('subject')}")
                    
                    # 1. Send Auto-Reply
                    rep_resp = reply_to_msg(msg_id, sender)
                    if "error" not in rep_resp:
                        logging.info(f"✅ Auto-reply sent to {sender}.")
                    else:
                        logging.error(f"❌ Failed to send reply: {rep_resp}")

                    # 2. Mark as Read
                    mark_resp = mark_read(msg_id)
                    if "error" not in mark_resp:
                        logging.info(f"✔ Message {msg_id} marked as read.")
                    else:
                        logging.error(f"❌ Failed to mark as read: {mark_resp}")

        except Exception as e:
            logging.error(f"Loop error: {e}")
            
        time.sleep(30) # Check every 30 seconds

if __name__ == "__main__":
    main()
