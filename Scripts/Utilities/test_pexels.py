import os
import sys

import requests

# Put parent dir in path
sys.path.append(os.getcwd())
try:
    from Scripts.Utilities.token_broker import TokenBroker
except ImportError:
    print("❌ Could not import TokenBroker")
    sys.exit(1)


def test_pexels():
    print("🔍 Testing Pexels Key via TokenBroker...")
    broker = TokenBroker()
    key = broker.get_key("pexels")

    if not key:
        print("❌ No Pexels key found in broker.")
        return

    print(f"🔑 Using Key: {key[:5]}...{key[-3:]}")

    headers = {"Authorization": key}
    url = "https://api.pexels.com/videos/search?query=nature&per_page=1"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("videos"):
                print(f"✅ Success! Found video: {data['videos'][0]['url']}")
            else:
                print("✅ Auth success, but no videos found (strange).")
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    test_pexels()
