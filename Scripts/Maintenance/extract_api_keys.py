#!/usr/bin/env python3
"""
Extract API keys from open browser tabs
"""
import json
import re

import requests
import websocket


def get_tabs():
    resp = requests.get("http://localhost:9222/json")
    return [t for t in resp.json() if t.get('type') == 'page']

def run_js(ws_url, expression):
    try:
        ws = websocket.create_connection(ws_url, timeout=10)
        ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {
                "expression": expression,
                "returnByValue": True
            }
        }))
        result = json.loads(ws.recv())
        ws.close()
        return result.get("result", {}).get("result", {}).get("value")
    except:
        return None

def main():
    tabs = get_tabs()
    keys = {}

    # Find SerpAPI dashboard
    for tab in tabs:
        url = tab.get("url", "")
        ws_url = tab.get("webSocketDebuggerUrl")
        if not ws_url:
            continue

        # SerpAPI
        if "serpapi.com/dashboard" in url:
            print("🔍 Checking SerpAPI...")
            # Try to get API key from page
            html = run_js(ws_url, "document.body.innerText")
            if html:
                # Look for API key pattern
                match = re.search(r'([a-f0-9]{64})', html)
                if match:
                    keys["SERPAPI_KEY"] = match.group(1)
                    print(f"   ✅ Found key: {match.group(1)[:20]}...")

        # OpenRouter
        if "openrouter.ai/settings/keys" in url:
            print("🔍 Checking OpenRouter...")
            html = run_js(ws_url, "document.body.innerText")
            if html:
                match = re.search(r'(sk-or-v1-[a-f0-9]{64})', html)
                if match:
                    keys["OPENROUTER_KEY"] = match.group(1)
                    print(f"   ✅ Found key: {match.group(1)[:30]}...")

        # NVIDIA
        if "build.nvidia.com" in url:
            print("🔍 Checking NVIDIA...")
            # Check localStorage
            data = run_js(ws_url, "JSON.stringify(localStorage)")
            if data:
                storage = json.loads(data)
                for k, v in storage.items():
                    if 'nvapi' in str(v).lower() or 'key' in k.lower():
                        print(f"   Found localStorage key: {k}")

    print("\n" + "="*60)
    print("🔑 EXTRACTED API KEYS")
    print("="*60)

    if keys:
        for name, key in keys.items():
            print(f"\nexport {name}=\"{key}\"")

        # Append to .env
        with open(".env", "a") as f:
            f.write("\n# Auto-extracted API keys\n")
            for name, key in keys.items():
                f.write(f"{name}={key}\n")
        print("\n✅ Keys appended to .env")
    else:
        print("\n⚠️ No API keys found in visible page content.")
        print("Keys might be hidden. Check manually:")
        print("  - SerpAPI: https://serpapi.com/dashboard")
        print("  - OpenRouter: https://openrouter.ai/settings/keys")

if __name__ == "__main__":
    main()
