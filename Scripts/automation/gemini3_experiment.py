from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool

GEMINI_API_KEY = "AIzaSyCZd986TK8vI-lk7ygpwMV0XgquWIHX7ZU"

def test_gemini_3():
    print("🚀 Experimenting with Gemini 3 (The Future)...")

    client = genai.Client(api_key=GEMINI_API_KEY)

    # We'll try gemini-3-flash-preview as it's likely more stable for initial tests
    model_id = "models/gemini-3-flash-preview"

    print(f"📡 Using model: {model_id}")

    query = "Describe the potential capabilities of Gemini 3 architecture compared to Gemini 2. Focus on agentic workflows and multi-step reasoning."

    try:
        response = client.models.generate_content(
            model=model_id,
            contents=query,
            config=GenerateContentConfig(
                tools=[Tool(google_search=GoogleSearch())]
            )
        )

        print("\n✅ Gemini 3 Response:")
        print(response.text)

        if response.candidates[0].grounding_metadata:
            print("\n📚 Grounding Metadata found (Powered by Google Search)")

    except Exception as e:
        print(f"❌ Error with Gemini 3: {e}")
        print("💡 Suggestion: The model might be restricted to specific regions or require internal whitelisting despite appearing in the list.")

if __name__ == "__main__":
    test_gemini_3()
