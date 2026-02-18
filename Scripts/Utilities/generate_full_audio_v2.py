import os
import sys

from openai import OpenAI

# Add paths for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
from token_broker import TokenBroker


def generate_full_audio():
    print("🎬 Starting Audio Generation (Synchronous)...")
    broker = TokenBroker()
    key = broker.get_key("openai")
    client = OpenAI(api_key=key)

    script_path = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_SCRIPT_2026.md"
    with open(script_path) as f:
        full_script = f.read()

    import re
    clean_script = re.sub(r'\[.*?\]', '', full_script)
    clean_script = re.sub(r'\*\*.*?\*\*', '', clean_script)
    clean_script = re.sub(r'#.*', '', clean_script)
    clean_script = clean_script.strip()

    # Split by paragraphs or sentences
    chunks = [c.strip() for c in clean_script.split("\n\n") if c.strip()]

    print(f"🚀 Total chunks to process: {len(chunks)}")

    media_dir = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media"
    os.makedirs(media_dir, exist_ok=True)

    for i, chunk in enumerate(chunks):
        # Skip empty chunks
        if len(chunk) < 10: continue

        print(f"  → Processing chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...")
        chunk_path = os.path.join(media_dir, f"audio_chunk_{i}.mp3")

        try:
            response = client.audio.speech.create(
                model="tts-1-hd",
                voice="onyx",
                input=chunk
            )
            # Use the content directly
            response.write_to_file(chunk_path)
            print(f"    ✅ Saved chunk {i} to {chunk_path}")
        except Exception as e:
            print(f"    ❌ Error on chunk {i}: {e}")

    print("🏁 Audio generation finished.")

if __name__ == "__main__":
    generate_full_audio()
