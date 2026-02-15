import os
from pathlib import Path

from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / "Projects/AI_Core/.env"

try:
    from dotenv import load_dotenv

    load_dotenv(env_path)
except Exception:
    pass

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise SystemExit("OPENAI_API_KEY is not set.")

client = OpenAI(api_key=api_key)
try:
    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input="This is a test of the emergency broadcast system."
    )
    response.stream_to_file("test_audio.mp3")
    print("✅ Success! test_audio.mp3 created.")
except Exception as e:
    print(f"❌ Error: {e}")
