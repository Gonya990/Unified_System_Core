import os
import json
import sys
from Projects.Content_Factory.src.pipeline.vibranium_creativity import generate_dynamic_content

def test_production():
    print("Testing Content Factory LLM Fallback...")
    # Force Gemini key from the code if it's there, or use environment
    os.environ["GEMINI_API_KEY"] = "AIzaSyCZd986TK8vI-lk7ygpwMV0XgquWIHX7ZU"
    # Nullify OpenAI to force fallback
    os.environ["OPENAI_API_KEY"] = "invalid"
    os.environ["GITHUB_TOKEN"] = "invalid"
    
    try:
        content = generate_dynamic_content()
        print("✅ SUCCESS! LLM Response:")
        print(json.dumps(content, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_production()
