import os
import re
import sys

from openai import OpenAI

# Add paths for TokenBroker
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src")
from token_broker import TokenBroker


def generate_scene_audio(lang="EN"):
    print(f"🎬 Starting Scene-Based Audio Generation ({lang})...")
    broker = TokenBroker()
    key = broker.get_key("openai")
    client = OpenAI(api_key=key)

    suffix = "_RU" if lang == "RU" else ""
    script_path = f"/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/DOCUMENTARY_SCRIPT_2026{suffix}.md"

    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return

    with open(script_path) as f:
        content = f.read()

    # Split by Narrator markers
    # We want to keep the scene context if possible, but the simplest is splitting by [NARRATOR SPEAKS]:
    parts = re.split(r'\[NARRATOR SPEAKS\]:', content)

    # Filter intro/outro text
    speech_blocks = [p.strip() for p in parts if len(p.strip()) > 10]

    print(f"🚀 Found {len(speech_blocks)} speech blocks for {lang}")

    media_dir = f"/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/audio/{lang}"
    os.makedirs(media_dir, exist_ok=True)

    for i, block in enumerate(speech_blocks):
        # Clean block from markdown
        text = re.sub(r'\[.*?\]', '', block)
        text = re.sub(r'\*\*.*?\*\*', '', text)
        text = text.replace('"', '').strip()

        # Add smooth pauses at the beginning and end if needed (handled by narration style)
        print(f"  → Encoding block {i+1}/{len(speech_blocks)} ({len(text)} chars)...")
        filename = f"block_{i}.mp3"
        out_path = os.path.join(media_dir, filename)

        try:
            response = client.audio.speech.create(
                model="tts-1-hd",
                voice="onyx",
                input=text
            )
            response.write_to_file(out_path)
            print(f"    ✅ Saved to {out_path}")
        except Exception as e:
            print(f"    ❌ Error: {e}")

if __name__ == "__main__":
    generate_scene_audio("EN")
    generate_scene_audio("RU")
