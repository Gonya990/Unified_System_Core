import json

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

TOKEN = 'c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb'
SERVER = 'http://100.110.209.49:8765'
PROJECT = '/Gonya990/Unified_System_Core'
NAME = 'OrangeStone'

def register():
    url = f"{SERVER}/mcp"
    payload = {
        'jsonrpc': '2.0',
        'method': 'tools/call',
        'params': {
            'name': 'register_agent',
            'arguments': {
                'project_key': PROJECT,
                'name': NAME,
                'program': 'claude-code',
                'model': 'claude-sonnet-4.5'
            }
        },
        'id': 1
    }

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    print(f"Sending request to {url}...")
    try:
        res = requests.post(url, json=payload, headers=headers)
        print(f"Status: {res.status_code}")
        print("Body:")
        print(json.dumps(res.json(), indent=2))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register()
