import os
import sys
import requests
import json

def main():
    server = "http://100.126.23.67:8765"
    token = "antigravity_secret"
    project_key = "/home/gonya/Unified_System"
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "register_agent",
            "arguments": {
                "project_key": project_key,
                "program": "ai-bot",
                "model": "gpt-4o",
                "name": "FrostyMeadow",
                "task_description": "Main Telegram Bot"
            }
        },
        "id": 1
    }
    
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        res = requests.post(f"{server}/mcp", json=payload, headers=headers)
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
