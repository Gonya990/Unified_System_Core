import os
import requests

def test_openai():
    api_key = "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"
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
