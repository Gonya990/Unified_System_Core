#!/usr/bin/env python3
"""
Extract sessions and tokens from running Chrome browser
"""

import json

import requests
import websocket


def get_tabs():
    resp = requests.get("http://localhost:9222/json")
    return [t for t in resp.json() if t.get("type") == "page"]


def extract_from_tab(ws_url, tab_url):
    """Extract cookies and localStorage from a tab"""
    try:
        ws = websocket.create_connection(ws_url, timeout=5)

        # Get cookies
        ws.send(json.dumps({"id": 1, "method": "Network.enable"}))
        ws.recv()
        ws.send(json.dumps({"id": 2, "method": "Network.getCookies"}))
        cookie_result = json.loads(ws.recv())

        # Get localStorage via JS evaluation
        ws.send(
            json.dumps(
                {
                    "id": 3,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": "JSON.stringify({localStorage: {...localStorage}, sessionStorage: {...sessionStorage}})",
                        "returnByValue": True,
                    },
                }
            )
        )
        storage_result = json.loads(ws.recv())

        ws.close()

        cookies = cookie_result.get("result", {}).get("cookies", [])
        storage_str = storage_result.get("result", {}).get("result", {}).get("value", "{}")
        storage = json.loads(storage_str) if storage_str else {}

        return {
            "cookies": cookies,
            "localStorage": storage.get("localStorage", {}),
            "sessionStorage": storage.get("sessionStorage", {}),
        }
    except Exception as e:
        return {"error": str(e)}


def main():
    tabs = get_tabs()

    # Target domains for token extraction
    targets = {
        "serpapi": "serpapi.com",
        "openrouter": "openrouter.ai",
        "nvidia": "nvidia.com",
        "mashov": "mashov.info",
        "google_cloud": "console.cloud.google.com",
        "meta": "facebook.com",
    }

    results = {}

    for tab in tabs:
        url = tab.get("url", "")
        title = tab.get("title", "")
        ws_url = tab.get("webSocketDebuggerUrl")

        if not ws_url:
            continue

        for name, domain in targets.items():
            if domain in url:
                print(f"🔍 Extracting from: {title[:50]}")
                data = extract_from_tab(ws_url, url)

                if "error" not in data:
                    # Filter relevant cookies
                    relevant_cookies = [
                        c for c in data.get("cookies", []) if domain.split(".")[0] in c.get("domain", "")
                    ]

                    if relevant_cookies or data.get("localStorage"):
                        results[name] = {
                            "url": url,
                            "cookies_count": len(relevant_cookies),
                            "cookies": [
                                {"name": c["name"], "domain": c["domain"]}
                                for c in relevant_cookies[:10]  # Just names
                            ],
                            "localStorage_keys": list(data.get("localStorage", {}).keys())[:10],
                        }

    print("\n" + "=" * 60)
    print("📊 SESSION EXTRACTION RESULTS")
    print("=" * 60)

    for name, info in results.items():
        print(f"\n🔑 {name.upper()}")
        print(f"   URL: {info['url'][:60]}...")
        print(f"   Cookies: {info['cookies_count']}")
        for c in info["cookies"][:5]:
            print(f"     - {c['name']} ({c['domain']})")
        if info["localStorage_keys"]:
            print(f"   LocalStorage keys: {info['localStorage_keys'][:5]}")

    # Save full results
    with open("browser_sessions.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n✅ Saved to browser_sessions.json")


if __name__ == "__main__":
    main()
