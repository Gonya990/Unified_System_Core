import asyncio
import os
import sys

from openai import AsyncOpenAI

# Add paths for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
from token_broker import TokenBroker


async def generate_full_audio():
    broker = TokenBroker()
    key = broker.get_key("openai")
    client = AsyncOpenAI(api_key=key)

    script_path = "/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_SCRIPT_2026.md"
    with open(script_path) as f:
        full_script = f.read()

    # Remove markers like [NARRATOR SPEAKS] and PART ONE etc for cleaner audio
    import re
    clean_script = re.sub(r'\[.*?\]', '', full_script)
    clean_script = re.sub(r'\*\*.*?\*\*', '', clean_script)
    clean_script = re.sub(r'#.*', '', clean_script)
    clean_script = clean_script.strip()

    # Split into chunks of ~3500 chars (safe limit)
    chunks = []
    current_chunk = ""
    for sentence in clean_script.split(". "):
        if len(current_chunk) + len(sentence) < 3500:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "
    if current_chunk:
        chunks.append(current_chunk.strip())

    print(f"🚀 Generating {len(chunks)} audio chunks...")

    audio_files = []
    for i, chunk in enumerate(chunks):
        print(f"  → Encoding chunk {i+1}/{len(chunks)}...")
        response = await client.audio.speech.create(
            model="tts-1-hd",
            voice="onyx",
            input=chunk
        )
        chunk_path = f"/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/audio_chunk_{i}.mp3"
        os.makedirs(os.path.dirname(chunk_path), exist_ok=True)
        response.stream_to_file(chunk_path)
        audio_files.append(chunk_path)

    print(f"✅ Full audio generated in {len(chunks)} files.")
    return audio_files

if __name__ == "__main__":
    asyncio.run(generate_full_audio())
