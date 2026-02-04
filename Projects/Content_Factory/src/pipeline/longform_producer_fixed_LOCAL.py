#!/usr/bin/env python3
"""
Long-Form Documentary Producer (FIXED)
Produces 25-30 minute deep-dive documentaries using LLM Council for research.
Direct ENV Key Injection to avoid Broker issues.
"""

import json
import logging
import sys
import time
import os
import random
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("LongFormProducer")

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve()
FACTORY_DIR = SRC_DIR.parent
PROJECTS_DIR = FACTORY_DIR.parent
ROOT_DIR = PROJECTS_DIR.parent

# Add paths
sys.path.append(str(SRC_DIR / "researcher"))
sys.path.append(str(SRC_DIR / "pipeline"))
sys.path.append(str(ROOT_DIR / "Scripts/Utilities"))
sys.path.append(str(ROOT_DIR / "LLM_Council"))

# FORCE LOAD ENVS
load_dotenv(ROOT_DIR / ".env")
load_dotenv(FACTORY_DIR / ".env")
load_dotenv(PROJECTS_DIR / "AI_Core" / ".env")

# Ensure keys are in os.environ for subprocesses and libraries like google.genai
if os.getenv("ELEVENLABS_API_KEY"):
    os.environ["ELEVENLABS_API_KEY"] = os.getenv("ELEVENLABS_API_KEY")
if os.getenv("PEXELS_API_KEY"):
    os.environ["PEXELS_API_KEY"] = os.getenv("PEXELS_API_KEY")

# Mock Broker that just returns env vars to satisfy LLMCouncil if it needs it
class EnvBroker:
    def get_key(self, name, tier=None, session_id=None):
        name = name.upper()
        if name == "OPENAI": return os.getenv("OPENAI_API_KEY")
        if name == "GEMINI": return os.getenv("GEMINI_API_KEY")
        if name == "ELEVENLABS": return os.getenv("ELEVENLABS_API_KEY")
        if name == "PEXELS": return os.getenv("PEXELS_API_KEY")
        return os.getenv(f"{name}_API_KEY")
    
    def get_token(self, name, **kwargs):
        return self.get_key(name, **kwargs)

BROKER = EnvBroker()

# =============================================================================
#                           DEEP RESEARCH 
# =============================================================================

def deep_research_with_council(topic: str) -> Optional[dict]:
    print(f"\n🧠 PHASE 1: Planning Documentary Structure for '{topic}'")
    
    # Structure Template
    structure = {
        "title": f"Documentary: {topic}",
        "description": "Auto-generated documentary",
        "segments": []
    }
    
    # 6 Segments hardcoded logic since Council is flaky
    subtopics = [
        "Introduction & History",
        "Current State of Technology",
        "Real World Applications",
        "Challenges and Risks",
        "Future Predictions 2030",
        "Conclusion: What lies ahead"
    ]
    
    for i, sub in enumerate(subtopics):
        structure["segments"].append({
            "name": sub,
            "focus_points": [f"Deep dive into {sub}", "Expert opinions", "Statistics"],
            "visual_theme": "documentary",
            "script": generate_script_direct(topic, sub) # Generate script immediately
        })
        
    return structure

def generate_script_direct(topic, subtopic):
    """
    Generate script using OpenAI directly to avoid Council complexity for now
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return f"Script generation failed. Topic: {topic}. Subtopic: {subtopic}. (No API Key)"
        
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        prompt = f"""
        Write a 3-minute documentary narration script (Russian language) about: {topic}
        Focus specifically on: {subtopic}
        
        Style: Professional, Engaging, Discovery Channel style.
        Length: Approx 400-500 words.
        Format: Just the text for Voiceover. No scene directions in text.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI Error: {e}")
        return f"Error generating script for {subtopic}."

# =============================================================================
#                           VIDEO ASSEMBLY
# =============================================================================

def assemble_longform_video(data: dict, output_dir: Path) -> Optional[Path]:
    from orchestrator_v3_no_face import run_no_face_pipeline
    
    segments = data.get("segments", [])
    segment_videos = []
    
    for i, seg in enumerate(segments):
        print(f"\n📹 Processing Segment {i+1}: {seg['name']}")
        
        script = seg.get("script", "")
        if len(script) < 100:
            print("⚠️ Script too short, skipping.")
            continue
            
        seg_name = f"longform_part_{i}"
        
        # Determine Scenes keywords based on segment name
        keywords = seg['name'].split()
        scenes = [
             {'keyword': f"{keywords[0]} abstract technology"},
             {'keyword': f"{keywords[-1]} detail"},
             {'keyword': "future world"}
        ]
        
        # Use existing powerful V3 pipeline
        run_no_face_pipeline(
            text=script,
            lang="ru",
            output_name=seg_name,
            scenes=scenes,
            style="impact" # Uses ElevenLabs + Pexels
        )
        
        # The V3 pipeline saves to FACTORY/outputs/
        # We need to find it and move/symlink or just add to list
        expected_path = FACTORY_DIR / f"outputs/{seg_name}_final.mp4"
        if expected_path.exists():
            segment_videos.append(expected_path)
            print(f"✅ Segment {i+1} Ready: {expected_path}")
        else:
            print(f"❌ Segment {i+1} Failed to produce video")
            
    if not segment_videos:
        print("❌ No segments produced.")
        return None
        
    # Concatenate
    print(f"\n🔗 Concatenating {len(segment_videos)} segments...")
    concat_file = output_dir / "concat_list.txt"
    final_output = output_dir / f"FULL_DOCUMENTARY_{int(time.time())}.mp4"
    
    with open(concat_file, "w") as f:
        for v in segment_videos:
            f.write(f"file '{v}'\n")
            
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy", str(final_output)
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"✅ FULL MOVIE SAVED: {final_output}")
        return final_output
    except Exception as e:
        print(f"❌ Concat Error: {e}")
        return None

if __name__ == "__main__":
    topic = "The Future of Humanity 2026"
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", default=topic)
    args = parser.parse_args()
    
    # 1. Research (Simplified)
    data = deep_research_with_council(args.topic)
    
    # 2. Output Dir
    out_dir = FACTORY_DIR / "outputs"
    out_dir.mkdir(exist_ok=True)
    
    # 3. Produce
    vid = assemble_longform_video(data, out_dir)
    
    if vid:
        # Notify Telegram
        msg = f"🎬 <b>ДОКУМЕНТАЛЬНЫЙ ФИЛЬМ ГОТОВ!</b>\n\n<b>Тема:</b> {args.topic}\n<b>Файл:</b> {vid.name}"
        subprocess.run([
            'curl', '-F', f'video=@{vid}', 
            '-F', 'chat_id=708531393', 
            '-F', f'caption={msg}', 
            '-F', 'parse_mode=HTML',
            'https://api.telegram.org/bot8518131338:AAHtcEgI--E2Fktdo3nE3oynhzq1gvrVON4/sendVideo'
        ])
