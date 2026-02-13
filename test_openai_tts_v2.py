from pathlib import Path

from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / "Projects/AI_Core/.env"
# Temporarily hardcode the other key to test
api_key = "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"

client = OpenAI(api_key=api_key)
try:
    response = client.audio.speech.create(
        model="tts-1", voice="alloy", input="This is a test of the emergency broadcast system."
    )
    response.stream_to_file("test_audio.mp3")
    print("✅ Success! test_audio.mp3 created.")
except Exception as e:
    print(f"❌ Error: {e}")
