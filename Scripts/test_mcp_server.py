import requests
import json

url = "https://web-to-mcp.com/mcp/6fb78109-5edd-4124-8df7-b6d168ef99da/"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream"
}
payload = {
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1,
    "params": {}
}

try:
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
