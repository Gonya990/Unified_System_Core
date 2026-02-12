import os
import json
from Projects.Content_Factory.src.pipeline.vibranium_creativity import (
    generate_dynamic_content
)

def test_production():
    print("Testing Content Factory LLM Fallback...")
    # Respect existing env; never hardcode secrets in code.
    gemini_key = os.getenv("GEMINI_API_KEY")
    github_token = os.getenv("GITHUB_TOKEN")

    if not gemini_key:
        raise RuntimeError("GEMINI_API_KEY is required in the environment for the fallback test")

    # Nullify OpenAI to force fallback path if caller didn't already override
    os.environ.setdefault("OPENAI_API_KEY", "invalid")
    os.environ.setdefault("GITHUB_TOKEN", github_token or "invalid")
    
    try:
        content = generate_dynamic_content()
        print("✅ SUCCESS! LLM Response:")
        print(json.dumps(content, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"❌ FAILED: {e}")

if __name__ == "__main__":
    test_production()
