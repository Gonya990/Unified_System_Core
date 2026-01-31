import os
from pathlib import Path

import requests
from dotenv import load_dotenv

# Load environment variables from .env file (searching parent directories)
# Script is in Projects/AI_Core/src, .env is in Unified_System_Core (root)
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path, override=True)

def test_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not set in environment")
        return
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "say hi"}],
        "max_tokens": 5
    }
    try:
        res = requests.post(url, json=payload, headers=headers)
        print(f"Status: {res.status_code}")
        print(res.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_openai()
