import json
import os
import sys

import requests

# Add SDK
sdk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../External_Tools/Stack/agent_mail_sdk/src"))
sys.path.append(sdk_path)


def main():
    server = "http://100.126.23.67:8765"
    token = "antigravity_secret"

    payload = {"jsonrpc": "2.0", "method": "tools/list", "params": {}, "id": 1}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        res = requests.post(f"{server}/mcp", json=payload, headers=headers)
        tools = res.json()["result"]["tools"]
        for tool in tools:
            if tool["name"] in ["create_agent_identity", "register_agent", "whois"]:
                print(json.dumps(tool, indent=2))
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
