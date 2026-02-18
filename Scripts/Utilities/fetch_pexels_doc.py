import os
import sys
from pathlib import Path

# Add factory src to path
sys.path.insert(0, "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory/src")
from video.ai_video_generator import VideoGenerator

def fetch_doc_assets():
    vgen = VideoGenerator(provider="pexels")
    output_dir = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Reports/media/scenes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pexels_scenes = {
        "1": "Deep space zoom earth",
        "3": "motherboard microchip glowing",
        "4": "server room data center lights",
        "8": "fiber optic cable network",
        "9": "human brain nervous system animation",
        "15": "hacker in hood dark room",
        "18": "gold coins falling pile",
        "19": "stock market green candle chart",
        "20": "people using laptops globally"
    }
    
    print(f"🎬 Fetching {len(pexels_scenes)} Pexels videos...")
    
    for sid, prompt in pexels_scenes.items():
        out_path = output_dir / f"scene_{sid}.mp4"
        if out_path.exists():
            print(f"  → Scene {sid} already exists, skipping.")
            continue
        print(f"  → Fetching Scene {sid}: {prompt}")
        try:
            vgen.generate_video(prompt=prompt, output_path=out_path)
            print(f"    ✅ Downloaded.")
        except Exception as e:
            print(f"    ❌ Failed: {e}")

if __name__ == "__main__":
    fetch_doc_assets()
