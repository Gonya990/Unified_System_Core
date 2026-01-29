#!/usr/bin/env python3
import json
import logging

import requests
import websocket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("WebtopStealer")

def get_webtop_tab():
    resp = requests.get("http://localhost:9222/json")
    for t in resp.json():
        if "webtop.smartschool.co.il" in t.get('url', ''):
            return t
    return None

def main():
    tab = get_webtop_tab()
    if not tab:
        print("❌ Webtop tab not found!")
        return

    ws_url = tab.get('webSocketDebuggerUrl')
    try:
        ws = websocket.create_connection(ws_url)

        # JS to extract homework from Webtop internal state
        # Usually Webtop uses Vue/React, we can try to find the data in the DOM or API response
        js_code = """
        (function() {
            // Try to find homework items in the DOM
            const items = Array.from(document.querySelectorAll('.homework-item, [class*="homework"]')).map(el => el.innerText);
            
            // Also grab the auth tokens from localStorage
            const auth = localStorage.getItem('token') || localStorage.getItem('access_token');
            const user = localStorage.getItem('user');
            
            return JSON.stringify({
                url: window.location.href,
                homework_dom: items,
                tokens: {
                    auth: auth,
                    user: user
                },
                localStorage: {...localStorage}
            });
        })()
        """

        ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": js_code, "returnByValue": True}
        }))

        res = json.loads(ws.recv())
        ws.close()

        if "result" in res and "result" in res["result"] and "value" in res["result"]["result"]:
            data = json.loads(res["result"]["result"]["value"])
            print(json.dumps(data, indent=2, ensure_ascii=False))

            with open("webtop_session.json", "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print("\n✅ Saved session to webtop_session.json")
        else:
            print("❌ Failed to extract data")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
