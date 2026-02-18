import os
import sys

from openai import OpenAI

# Add paths for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
from token_broker import TokenBroker


def test_voice():
    broker = TokenBroker()
    key = broker.get_key("openai")
    client = OpenAI(api_key=key)

    text = "Unified System Core. The architecture of autonomous sovereignty. A new era begins in 2026."

    print("🚀 Generating voice sample...")
    response = client.audio.speech.create(
        model="tts-1-hd",
        voice="onyx",
        input=text
    )

    path = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/voice_sample.mp3"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    response.stream_to_file(path)
    print(f"✅ Voice sample saved to {path}")

if __name__ == "__main__":
    test_voice()
