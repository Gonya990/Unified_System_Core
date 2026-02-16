import os

import openai
from dotenv import load_dotenv
from google import genai

load_dotenv(os.path.join(os.path.dirname(__file__), "../.env"))


def test_openai():
    print("Testing OpenAI...")
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        print("❌ OpenAI API key not found in environment!")
        return
    print(f"Using key: {key[:8]}...{key[-4:]}")
    client = openai.OpenAI(api_key=key)
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": "ping"}], max_tokens=5
        )
        print(f"✅ OpenAI works: {res.choices[0].message.content}")
    except Exception as e:
        print(f"❌ OpenAI failed: {e}")


def test_gemini():
    print("\nTesting Gemini...")
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        print("❌ Gemini API key not found in environment!")
        return
    print(f"Using key: {key[:8]}...{key[-4:]}")
    client = genai.Client(api_key=key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    print(f"Using model: {model_name}")
    try:
        res = client.models.generate_content(model=model_name, contents="ping")
        print(f"✅ Gemini works: {res.text}")
    except Exception as e:
        print(f"❌ Gemini failed: {e}")


if __name__ == "__main__":
    test_openai()
    test_gemini()
