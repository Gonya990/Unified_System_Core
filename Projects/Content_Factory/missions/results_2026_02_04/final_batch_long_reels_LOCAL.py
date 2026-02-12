import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

# Force load ENV
load_dotenv('/home/gonya/Unified_System_Core/Projects/Content_Factory/.env')
# Ensure API keys are present in env for subprocesses
os.environ['PEXELS_API_KEY'] = os.getenv('PEXELS_API_KEY', '')
os.environ['ELEVENLABS_API_KEY'] = os.getenv('ELEVENLABS_API_KEY', '')
os.environ['RUNWAY_API_KEY'] = os.getenv('RUNWAY_API_KEY', '')

# Setup paths
FACTORY_ROOT = '/home/gonya/Unified_System_Core/Projects/Content_Factory'
sys.path.append(os.path.join(FACTORY_ROOT, 'src'))
sys.path.append(os.path.join(FACTORY_ROOT, 'src/pipeline'))

from orchestrator_v3_no_face import run_no_face_pipeline

# TOPICS ONLY - The script will be generated dynamically to be LONG (50s+)
TOPICS = [
    {
        "topic": "Neural Interfaces 2030",
        "keywords": ["human brain chip", "future interface"]
    },
    {
        "topic": "Mars Colonization Infrastructure",
        "keywords": ["mars base construction", "spacex rocket"]
    }
]

def generate_viral_script(topic):
    """Generates a 140-word robust script (~50-60 sec audio)"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        prompt = f"""
        Write a viral 60-second TikTok/Reels script (Russian Language) about: {topic}
        
        Rules:
        1. Length: Approx 130-150 words (Must take ~50 seconds to read).
        2. Style: High energy, shocking facts, "Did you know?" style.
        3. No scene headers, just the spoken text.
        4. Do not use emojis in the text.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI Gen Error: {e}")
        return None

def run_long_reels():
    print('🚀 Starting LONG REELS Production (Target: 40-60s)...')

    for i, item in enumerate(TOPICS):
        topic = item["topic"]
        print(f"\n🎬 Processing Topic: {topic}")

        # 1. Generate Long Script
        script = generate_viral_script(topic)
        if not script:
            print("Failed to generate script")
            continue

        print(f"📝 Script generated ({len(script)} chars)")

        # 2. Dynamic Scenes (6 scenes for 60s = ~10s per scene)
        scenes = []
        base_keywords = item["keywords"]
        for j in range(6):
            kw = base_keywords[j % len(base_keywords)]
            scenes.append({"keyword": kw})

        # 3. Run Pipeline
        name = f"REEL_LONG_{int(time.time())}_{i}"
        try:
            run_no_face_pipeline(
                text=script,
                lang='ru',
                output_name=name,
                scenes=scenes,
                style='impact'
            )

            output_file = Path(FACTORY_ROOT) / f'outputs/{name}_final.mp4'
            if output_file.exists():
                caption = f"🎞️ <b>{topic}</b>\n\n✅ 60s Generation\n✅ ElevenLabs + Pexels\n\n<a href='https://www.pexels.com'>Photos provided by Pexels</a>"
                subprocess.run([
                    'curl',
                    '-F', f'video=@{output_file}',
                    '-F', 'chat_id=708531393',
                    '-F', f'caption={caption}',
                    '-F', 'parse_mode=HTML',
                    'https://api.telegram.org/bot8518131338:AAHtcEgI--E2Fktdo3nE3oynhzq1gvrVON4/sendVideo'
                ])
                print(f"📤 Sent {name}")

        except Exception as e:
            print(f"❌ Pipeline Error: {e}")

if __name__ == '__main__':
    run_long_reels()
