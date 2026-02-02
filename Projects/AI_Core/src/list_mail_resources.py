import requests


def main():
    server = "http://100.126.23.67:8765"
    token = "antigravity_secret"

    payload = {
        "jsonrpc": "2.0",
        "method": "resources/list",
        "params": {},
        "id": 1
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        res = requests.post(f"{server}/mcp", json=payload, headers=headers)
        print(f"Resources: {res.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
