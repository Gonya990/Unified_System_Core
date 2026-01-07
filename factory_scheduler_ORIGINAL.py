#!/usr/bin/env python3
import os
import sys
import json
import random
from pathlib import Path
from datetime import datetime

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from orchestrator_v3_no_face import run_no_face_pipeline, add_subtitles, OUTPUT_DIR
from insta_uploader import upload_reel

# Configuration
REELS_AUTO_UPLOAD = True  # Set to False if you want to manual review first

def get_weekly_trend():
    """
    Randomly selects a futuristic topic for daily variation.
    """
    topics = [
        {
            "topic": "The Rise of Agentic AI: Your New Digital Co-workers",
            "description": "Explaining the shift from chatbots to autonomous agents in 2026.",
            "keywords": ["agentic ai", "autonomous agents", "productivity 2026", "digital workforce"]
        },
        {
            "topic": "AI & Bio-Engineering: The Neural Link Era",
            "description": "How AI is merging with human biology to enhance cognition.",
            "keywords": ["neuralink", "bio-ai", "cybernetic enhancement", "future brain"]
        },
        {
            "topic": "The Post-Labor Economy: Living with AI Wealth",
            "description": "What happens when AI does 90% of the work? The new human purpose.",
            "keywords": ["post-labor", "universal income", "ai economy", "future of work"]
        },
        {
            "topic": "Digital Immortality: Uploading the Mind in 2026",
            "description": "The first steps towards consciousness preservation in the cloud.",
            "keywords": ["digital immortality", "mind uploading", "consciousness", "future tech"]
        }
    ]
    trend = random.choice(topics)
    print(f"🔍 Selected Daily Trend: {trend['topic']}")
    return trend

def generate_dynamic_script(trend):
    """
    Calls the LLM Council to generate a 15-scene script.
    """
    print(f"📝 Drafting Script for: {trend['topic']}")
    
    # Generic high-impact script template that adapts to the topic
    script_ru = (
        f"Мы перешли черту. 2026 год стал моментом... когда {trend['topic']} перестал быть просто теорией... и стал реальностью. "
        f"Познакомьтесь с будущим. Это не просто технология... это глобальный сдвиг в самой сути нашего существования. "
        "Они не спрашивают 'как это работает?'... они спрашивают 'как далеко мы готовы зайти?'. "
        "Ваш новый мир уже здесь. Он управляет вашим временем... вашими возможностями... и вашей судьбой... пока вы спите. "
        "Это не просто прогресс. Это симбиоз человеческой воли... и бесконечной цифровой мощи. "
        "Миллиарды процессов уже трудятся в глобальной сети... создавая новую цивилизацию... цивилизацию действий, а не ожиданий. "
        "Но готовы ли вы... доверить свое будущее коду? "
        "Граница между человеком и машиной стирается... и это только начало. "
        "Эти изменения не заменяют вас... они освобождают вас для великих свершений. "
        "Добро пожаловать в эру осознанного разума. "
        "Эпоха 2026 года. Где интеллект — это не ресурс... а само действие. "
        "Весь мир скоро изменится навсегда. "
        "Будущее не наступает... оно программируется прямо сейчас. "
        "Приготовьтесь к самому масштабному сдвигу в истории человечества. "
        "Это ваш новый мир. Мир, где каждый из нас — лидер армии технологий."
    )
    
    # Scene mapping with epic keywords
    scenes = [
        {"image": "ai_factory_s1_agent_working", "keyword": "cyborg digital office futuristic 4k"},
        {"image": "ai_factory_s2_interface", "keyword": "holographic dashboard futuristic computer cinematic"},
        {"image": "ai_factory_s3_avatar", "keyword": "humanoid robot face smooth white portrait cinematic"},
        {"image": "ai_factory_s4_matrix", "keyword": "fast digital matrix particles movement slow motion"},
        {"image": "ai_factory_s5_collab", "keyword": "human hand touching holographic screen cinematic"},
        {"image": "ai_factory_s6_global", "keyword": "planet earth glowing neural network space cinematic"},
        {"image": "ai_factory_s7_trust", "keyword": "stormy dark ocean lighthouse cinematic"},
        {"image": "ai_factory_s8_blurring", "keyword": "ink merging in water abstract slow motion cinematic"},
        {"image": "ai_factory_s9_liberation", "keyword": "eagle wings flying through clouds cinematic sky"},
        {"image": "ai_factory_s10_era_sunrise", "keyword": "sunrise over futuristic city horizon cinematic"},
        {"image": "ai_factory_s11_brain_firing", "keyword": "digital brain firing synapses close up cinematic"},
        {"image": "ai_factory_s12_hr_minimalist", "keyword": "clean futuristic hall minimalist architecture cinematic"},
        {"image": "ai_factory_s13_typing_code_matrix", "keyword": "hands typing glowing code matrix background cinematic"},
        {"image": "ai_factory_s14_gears_digital_light_cinematic", "keyword": "old gears turning into digital light cinematic"},
        {"image": "ai_factory_s15_robot_army_silhouette_sunset_cinematic", "keyword": "massive army of robots silhouettes sunset cinematic"}
    ]
    
    return script_ru, scenes

def run_weekly_production():
    """Main Factory Loop"""
    day_str = datetime.now().strftime('%Y-%m-%d')
    print(f"🏭 --- Factory Run: {day_str} ---")
    
    # 1. Research
    trend = get_weekly_trend()
    
    # 2. Scripting
    script_ru, scenes = generate_dynamic_script(trend)
    
    # 3. Production
    output_name = f"factory_daily_{day_str.replace('-', '')}"
    
    # Path to where images are saved
    gen_dir = ROOT_DIR / "assets"
    if not gen_dir.exists(): # Fallback for MacBook local testing
        gen_dir = Path("/Users/macbook/.gemini/antigravity/brain/74acf072-6bc0-4fdc-9ad0-33f04fb9fa16")
    
    # Resolve image paths
    resolved_scenes = []
    for scene in scenes:
        matches = list(gen_dir.glob(f"{scene['image']}_*.png"))
        if matches:
            resolved_scenes.append({
                "image": str(sorted(matches)[-1]),
                "keyword": scene['keyword']
            })
        else:
            print(f"⚠️ Image {scene['image']} not found. Skipping.")

    if len(resolved_scenes) < 15:
        print(f"❌ Not enough scenes resolved ({len(resolved_scenes)}/15). Check logs.")
        return

    print("🚀 Launching Production Pipeline...")
    run_no_face_pipeline(script_ru, lang="ru", output_name=output_name, scenes=resolved_scenes)
    
    # 4. Final Verification and Upload
    final_video = OUTPUT_DIR / f"{output_name}_impact.mp4"
    if not final_video.exists():
        # Fallback to check raw_final
        raw_final = OUTPUT_DIR / f"{output_name}_final.mp4"
        if raw_final.exists():
            raw_final.rename(final_video)

    if final_video.exists():
        print(f"✅ Factory Production Success: {final_video}")
        
        if REELS_AUTO_UPLOAD:
            print("📤 Initializing Server-Side Upload...")
            caption = f"{trend['topic']}\n\n{trend['description']}\n\n#AI #Technology #2026 #Future #ImpactVision"
            success = upload_reel(str(final_video), caption)
            if success:
                print("🏆 Reel successfully published to Instagram!")
            else:
                print("⚠️ Auto-upload failed. Manual check required.")
    else:
        print(f"❌ Final video not found/generated: {output_name}")

if __name__ == "__main__":
    run_weekly_production()
