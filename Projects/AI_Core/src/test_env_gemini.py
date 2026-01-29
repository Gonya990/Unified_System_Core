import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file (searching parent directories)
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(dotenv_path=env_path, override=True)

def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not set in environment")
        return
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": "say hi"}]}]}
    try:
        res = requests.post(url, json=payload, headers=headers)
        print(f"Status: {res.status_code}")
        print(res.json())
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gemini()
