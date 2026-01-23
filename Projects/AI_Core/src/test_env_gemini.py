import os
import requests

def test_gemini():
    api_key = "AIzaSyAPXO54KZnH13Qspn10WFgI4DvJ3Dzs2TA"
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
