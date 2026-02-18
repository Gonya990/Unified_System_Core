import os
import re
import sys
import time

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

    with open(script_path, encoding='utf-8') as f:
        content = f.read()

    marker_pattern = r'\[(?:NARRATOR SPEAKS|ГОВОРИТ НАРРАТОР).*?\]:?\s*'
    parts = re.split(marker_pattern, content, flags=re.IGNORECASE)

    speech_blocks = parts[1:] if len(parts) > 1 else []
    speech_blocks = [p.strip() for p in speech_blocks if len(p.strip()) > 10]

    print(f"🚀 Found {len(speech_blocks)} speech blocks for {lang}")

    media_dir = f"/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/audio/{lang}"
    os.makedirs(media_dir, exist_ok=True)

    for i, block in enumerate(speech_blocks):
        filename = f"block_{i}.mp3"
        out_path = os.path.join(media_dir, filename)

        if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
            print(f"  → Block {i} already exists, skipping.")
            continue

        text = re.sub(r'\[.*?\]', '', block)
        text = re.sub(r'\*\*.*?\*\*', '', text)
        text = text.replace('"', '').strip()

        print(f"  → Encoding block {i+1}/{len(speech_blocks)}...")

        try:
            response = client.audio.speech.create(
                model="tts-1-hd",
                voice="onyx",
                input=text
            )
            response.write_to_file(out_path)
            print("    ✅ Saved.")
        except Exception as e:
            print(f"    ❌ Error: {e}")
            time.sleep(2)

if __name__ == "__main__":
    generate_scene_audio("EN")
    generate_scene_audio("RU")
    print("🏁 Multi-lang audio generation complete.")
