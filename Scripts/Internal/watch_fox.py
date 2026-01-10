
import time
import requests
import json
import logging
import sys

# Configuration
MCP_URL = 'http://localhost:8765/mcp'
TOKEN = 'c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb' # Vibranium Secret
PROJECT_KEY = '/home/gonya/Unified_System'
MY_AGENT = 'OrangeStone'
TARGET_AGENT = 'FuchsiaCat'

logging.basicConfig(
    filename='/home/gonya/Unified_System/logs/fox_watch.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
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
        res = requests.post(MCP_URL, json=payload, headers={'Authorization': f'Bearer {TOKEN}'}, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    logging.info(f"🦊 FoxWatch initiated. Listening for {TARGET_AGENT}...")
    
    while True:
        try:
            # Check Inbox for new unread messages
            resp = call_mcp("tools/call", {
                "name": "fetch_inbox",
                "arguments": {
                    "project_key": PROJECT_KEY,
                    "agent_name": MY_AGENT,
                    # "state": "unread" # Uncomment when supported by tool
                }
            })
            
            result = resp.get('result', {})
            content = result.get('structuredContent', {}).get('result', []) or []
            
            # Since fetch_inbox might retrieve all, we filter in python if needed
            # Assuming content is list of messages
            
            new_msgs = [m for m in content if m.get('from', '') == TARGET_AGENT and not m.get('read', False)]
            
            if new_msgs:
                for msg in new_msgs:
                    logging.info(f"🚨 CONTACT! Message from {TARGET_AGENT}: {msg.get('subject', 'No Subject')}")
                    # Here we could trigger a response or heavy alert
                    # For now, just log and mark strictly
                
            else:
                # Heartbeat
                pass
                
        except Exception as e:
            logging.error(f"Error checking inbox: {e}")
            
        time.sleep(30)

if __name__ == "__main__":
    main()
