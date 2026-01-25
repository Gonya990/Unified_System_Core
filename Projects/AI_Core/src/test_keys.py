import os
import openai
import google.generativeai as genai
from dotenv import load_dotenv

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
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=5
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
    genai.configure(api_key=key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    print(f"Using model: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        res = model.generate_content("ping")
        print(f"✅ Gemini works: {res.text}")
    except Exception as e:
        print(f"❌ Gemini failed: {e}")

if __name__ == "__main__":
    test_openai()
    test_gemini()
