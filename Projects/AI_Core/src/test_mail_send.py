import json

import requests


def main():
    server = "http://100.126.23.67:8765"
    token = "antigravity_secret"
    project_key = "/home/gonya/Unified_System"

    # We use OrangeStone as the sender
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "send_message",
            "arguments": {
                "project_key": project_key,
                "sender_name": "OrangeStone",
                "to": ["OrangeStone"],
                "subject": "Self-Test",
                "body_md": "Testing Agent Mail delivery on Windows server."
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
