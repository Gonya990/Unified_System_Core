#!/usr/bin/env python3
import json
import sys
from datetime import datetime

import requests

# CONFIGURATION
URL = "http://localhost:8765/mcp"
TOKEN = "c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb"
PROJECT_KEY = "/home/gonya/Unified_System"
MY_NAME = "Antigravity"
TARGET_AGENT = "VioletCastle"


def call_mcp(method, params):
    headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    try:
        response = requests.post(URL, json=payload, headers=headers, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def push_status(status_msg):
    print(f"📡 Pushing status to {TARGET_AGENT}...")
    params = {
        "name": "send_message",
        "arguments": {
            "project_key": PROJECT_KEY,
            "sender_name": MY_NAME,
            "recipient_name": TARGET_AGENT,
            "subject": f"SYNC: {datetime.now().strftime('%H:%M:%S')}",
            "body_md": status_msg,
        },
    }
    return call_mcp("tools/call", params)


def fetch_updates():
    print(f"👂 Listening for updates from {TARGET_AGENT}...")
    # Search for unread messages or just last messages from Target
    params = {
        "name": "search_messages",
        "arguments": {"project_key": PROJECT_KEY, "query": f"from:{TARGET_AGENT}", "limit": 3},
    }
    result = call_mcp("tools/call", params)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: ./sync_agent.py "Your current status/action"')
        sys.exit(1)

    status = sys.argv[1]

    # 1. Push
    push_res = push_status(status)
    if "error" in push_res:
        print(f"❌ Push failed: {push_res['error']}")
    else:
        print("✅ Status pushed successfully!")

    # 2. Fetch
    updates = fetch_updates()
    print("\n--- UPDATES FROM KOSTYA ---")
    try:
        messages = updates.get("result", {}).get("content", [])
        if messages and isinstance(messages, list):
            # MCP response usually has text in 'text' field or podobno
            print(json.dumps(messages, indent=2, ensure_ascii=False))
        else:
            print("No new updates from Kostya.")
    except Exception as e:
        print(f"Could not parse updates: {e}")
    print("---------------------------\n")
