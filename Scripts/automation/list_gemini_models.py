
from google import genai

GEMINI_API_KEY = "AIzaSyCZd986TK8vI-lk7ygpwMV0XgquWIHX7ZU"

def list_models():
    client = genai.Client(api_key=GEMINI_API_KEY)
    print("Listing available models:")
    for model in client.models.list():
        if "gemini-2.0-flash" in model.name:
            print(f"- {model.name}: {model.supported_actions}")

if __name__ == "__main__":
    list_models()
