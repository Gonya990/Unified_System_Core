import os

from google import genai


def list_models():
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        raise RuntimeError("Set GEMINI_API_KEY in env before running this script")

    client = genai.Client(api_key=gemini_key)
    print("Listing available models:")
    for model in client.models.list():
        if "gemini-2.0-flash" in model.name:
            print(f"- {model.name}: {model.supported_actions}")


if __name__ == "__main__":
    list_models()
