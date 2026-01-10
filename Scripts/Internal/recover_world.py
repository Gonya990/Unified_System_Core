
import requests
import sys

URL = 'http://localhost:8765/mcp'
TOKEN = 'c2bb2cf043ec2ae56a0dec69024e6129eb5cde36a22bddb93afcfa2e71e72afb'
PROJECT = '/home/gonya/Unified_System'

def call(name, args):
    payload = {
        "jsonrpc": "2.0", "method": "tools/call", "id": 1,
        "params": {"name": name, "arguments": args}
    }
    try:
        r = requests.post(URL, json=payload, headers={'Authorization': f'Bearer {TOKEN}'}, timeout=5)
        print(f"{name}: {r.status_code} - {r.text[:200]}...")
    except Exception as e:
        print(f"{name}: Error {e}")

# 1. Ensure Project
call("ensure_project", {"human_key": PROJECT})

# 2. Register Agents
agents = [
    {"name": "OrangeStone", "program": "antigravity-core", "model": "gemini-2.0-flash-exp"},
    {"name": "PinkLake", "program": "llm-council", "model": "gemini-2.0-flash-exp"},
    {"name": "FuchsiaCat", "program": "llm-council", "model": "gemini-2.0-flash-exp"}
]

for a in agents:
    args = {"project_key": PROJECT, **a}
    call("register_agent", args)

print("World Recovery Complete.")
