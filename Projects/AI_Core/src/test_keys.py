import os
import openai
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv("../.env")

def test_openai():
    print("Testing OpenAI...")
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
        )
        print(f"✅ OpenAI works: {res.choices[0].message.content}")
    except Exception as e:
        print(f"❌ OpenAI failed: {e}")

def test_gemini():
    print("\nTesting Gemini...")
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        res = model.generate_content("ping")
        print(f"✅ Gemini works: {res.text}")
    except Exception as e:
        print(f"❌ Gemini failed: {e}")

if __name__ == "__main__":
    test_openai()
    test_gemini()
