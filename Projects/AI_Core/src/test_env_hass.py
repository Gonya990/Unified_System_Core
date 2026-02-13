import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables from .env file (searching parent directories)
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path, override=True)


def test_hass():
    token = os.getenv("HASS_TOKEN")
    url = os.getenv("HASS_URL")

    if not token or not url:
        print("❌ HASS_TOKEN or HASS_URL not set in environment")
        return

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        res = requests.get(f"{url}/api/config", headers=headers, timeout=10)
        print(f"Status: {res.status_code}")
        if res.status_code == 200:
            print("✅ Successfully connected to Home Assistant!")
            data = res.json()
            print(f"Version: {data.get('version')}")
            print(f"Location: {data.get('location_name')}")
        else:
            print(f"Error: {res.text}")
    except Exception as e:
        print(f"Connection Error: {e}")


if __name__ == "__main__":
    test_hass()
