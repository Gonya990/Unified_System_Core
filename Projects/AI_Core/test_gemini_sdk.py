import os
import sys

from pathlib import Path
SRC_DIR = Path('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src')
if sys.path[0] != str(SRC_DIR):
    sys.path.insert(0, str(SRC_DIR))

from dotenv import load_dotenv
load_dotenv('/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/.env')

from google import genai
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

for model in ['gemini-2.5-flash', 'gemini-2.0-flash-exp', 'gemini-1.5-flash']:
    try:
        resp = client.models.generate_content(
            model=f"models/{model}",
            contents="Hello"
        )
        print(f"{model}: SUCCESS - {resp.text[:20]}")
    except Exception as e:
        print(f"{model}: FAILED - {e}")
