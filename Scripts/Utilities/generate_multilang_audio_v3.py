import os
import sys
import re
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

    with open(script_path, "r") as f:
        content = f.read()
    
    # Flexible marker for Narrator
    # EN: [NARRATOR SPEAKS] or [NARRATOR SPEAKS]:
    # RU: [ГОВОРИТ НАРРАТОР] or [ГОВОРИТ НАРРАТОР]:
    marker_pattern = r'\[(?:NARRATOR SPEAKS|ГОВОРИТ НАРРАТОР)\]:?\s*'
    
    parts = re.split(marker_pattern, content)
    
    # Filter intro text (before the first marker)
    # The first element of split result is usually the text before the first [NARRATOR SPEAKS]
    if len(parts) > 1:
        speech_blocks = parts[1:]
    else:
        print("❌ No markers found!")
        return
        
    speech_blocks = [p.strip() for p in speech_blocks if len(p.strip()) > 10]
    
    print(f"🚀 Found {len(speech_blocks)} speech blocks for {lang}")
    
    media_dir = f"/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/audio/{lang}"
    os.makedirs(media_dir, exist_ok=True)
    
    # Map for verification
    mapping_file = os.path.join(media_dir, "mapping.txt")
    with open(mapping_file, "w") as m:
        for i, block in enumerate(speech_blocks):
            # Clean block from scene markers and markdown
            text = re.sub(r'\[.*?\]', '', block)
            text = re.sub(r'\*\*.*?\*\*', '', text)
            text = text.replace('"', '').strip()
            
            # Shorten for log
            log_text = (text[:60] + '...') if len(text) > 60 else text
            print(f"  → Encoding block {i+1}/{len(speech_blocks)}: {log_text}")
            
            filename = f"block_{i}.mp3"
            out_path = os.path.join(media_dir, filename)
            
            m.write(f"{filename}|{text}\n")
            
            try:
                # Use onyx for deep male narrator
                response = client.audio.speech.create(
                    model="tts-1-hd",
                    voice="onyx",
                    input=text
                )
                response.write_to_file(out_path)
                print(f"    ✅ Saved.")
            except Exception as e:
                print(f"    ❌ Error: {e}")
                time.sleep(1)

if __name__ == "__main__":
    generate_scene_audio("EN")
    generate_scene_audio("RU")
    print("🏁 Multi-lang audio generation complete.")
