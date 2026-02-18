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

    with open(script_path, "r", encoding='utf-8') as f:
        content = f.read()
    
    # Very broad marker pattern to catch anything between brackets that looks like narration
    marker_pattern = r'\[(?:NARRATOR SPEAKS|ГОВОРИТ НАРРАТОР).*?\]:?\s*'
    
    parts = re.split(marker_pattern, content, flags=re.IGNORECASE)
    
    if len(parts) > 1:
        speech_blocks = parts[1:]
    else:
        print(f"❌ No markers found for {lang}!")
        # Fallback split by double newline if markers are missing
        if lang == "RU":
            print("Trying fallback split for RU...")
            speech_blocks = [p for p in content.split('\n\n') if '"' in p or len(p) > 100]
        else:
            return
            
    speech_blocks = [p.strip() for p in speech_blocks if len(p.strip()) > 10]
    
    print(f"🚀 Found {len(speech_blocks)} speech blocks for {lang}")
    
    media_dir = f"/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/audio/{lang}"
    os.makedirs(media_dir, exist_ok=True)
    
    mapping_file = os.path.join(media_dir, "mapping.txt")
    with open(mapping_file, "w", encoding='utf-8') as m:
        for i, block in enumerate(speech_blocks):
            text = re.sub(r'\[.*?\]', '', block)
            text = re.sub(r'\*\*.*?\*\*', '', text)
            text = text.replace('"', '').strip()
            
            if not text: continue
            
            log_text = (text[:60] + '...') if len(text) > 60 else text
            print(f"  → Encoding block {i+1}/{len(speech_blocks)}: {log_text}")
            
            filename = f"block_{i}.mp3"
            out_path = os.path.join(media_dir, filename)
            
            m.write(f"{filename}|{text}\n")
            
            try:
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
