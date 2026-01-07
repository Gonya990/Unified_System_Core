#!/usr/bin/env python3
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

from orchestrator_v3_no_face import run_no_face_pipeline, add_subtitles

def get_weekly_trend():
    """
    Simulates or performs web search for trending tech topics.
    For this 'Завод' run, we focus on 'Agentic AI / Digital Co-workers'.
    """
    print("🔍 Researching Weekly Trends...")
    # In a fully automated version, this would call search_web via an API or use a pre-scanned report.
    trend = {
        "topic": "The Rise of Agentic AI: Your New Digital Co-workers",
        "description": "Explaining the shift from chatbots to autonomous agents that perform multi-step tasks in 2026.",
        "keywords": ["agentic ai", "autonomous agents", "productivity 2026", "digital workforce"]
    }
    return trend

def generate_dynamic_script(trend):
    """
    Calls the LLM Council to generate a 15-scene script.
    For now, we provide a high-quality template specifically for the trend.
    """
    print(f"📝 Drafting Script for: {trend['topic']}")
    
    # This script is designed for the 'Motivaider' aesthetic: Strong, punchy, futuristic.
    script_ru = (
        "Мы перешли черту. 2026 год стал моментом... когда искусственный интеллект перестал быть просто инструментом... и стал сотрудником. "
        "Познакомьтесь с Агентным ИИ. Это не просто чат-бот... это цифровая личность, способная действовать автономно. "
        "Они не спрашивают 'что написать?'... они спрашивают 'какую проблему решить?'. "
        "Ваш новый цифровой коллега уже здесь. Он управляет вашим календарем... вашими проектами... и вашей стратегией... пока вы спите. "
        "Это не просто автоматизация. Это симбиоз человеческой воли... и бесконечной вычислительной мощности. "
        "Миллиарды таких агентов уже трудятся в глобальной сети... создавая новую экономику... экономику действий, а не слов. "
        "Но готовы ли вы... доверить решение машине? "
        "Граница между человеком и кодом стирается... и это только начало. "
        "Агентный ИИ не заменяет вас... он освобождает вас для великих дел. "
        "Добро пожаловать в эру автономного разума. "
        "Эпоха 2026 года. Где интеллект — это не ресурс... а действие. "
        "Ваш отдел кадров скоро изменится навсегда. "
        "Будущее не наступает... оно программируется прямо сейчас. "
        "Приготовьтесь к самому масштабному сдвигу в истории труда. "
        "Это ваш новый мир. Мир, где каждый из нас — лидер армии цифровых агентов."
    )
    
    # Scene mapping with epic keywords and PRE-GENERATED assets
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
    print(f"🏭 --- Factory Run: {datetime.now().strftime('%Y-%m-%d')} ---")
    
    # 1. Research
    trend = get_weekly_trend()
    
    # 2. Scripting
    script_ru, scenes = generate_dynamic_script(trend)
    
    # 3. Production (RU only for the 'Factory' demo, EN can be added)
    output_name = f"factory_weekly_{datetime.now().strftime('%Y%V')}"
    
    # We need to ensure images exist for the keywords or use Pexels effectively
    # For the factory, we rely on Pexels B-roll and AI images we've already generated or mock if missing
    
    # Path to where images are saved
    gen_dir = Path("/Users/macbook/.gemini/antigravity/brain/74acf072-6bc0-4fdc-9ad0-33f04fb9fa16")
    
    # Resolve image paths
    resolved_scenes = []
    for scene in scenes:
        matches = list(gen_dir.glob(f"{scene['image']}_*.png"))
        if matches:
            resolved_scenes.append({
                "image": sorted(matches)[-1],
                "keyword": scene['keyword']
            })
        else:
            print(f"⚠️ Image {scene['image']} not found. Skipping.")

    if len(resolved_scenes) < 15:
        print(f"❌ Not enough scenes resolved ({len(resolved_scenes)}/15). Check logs.")
        return

    print("🚀 Launching Production Pipeline...")
    run_no_face_pipeline(script_ru, lang="ru", output_name=output_name, scenes=resolved_scenes)
    
    # 4. Final Pass: Subtitles (Motivaider Style)
    final_video = ROOT_DIR / "outputs" / f"{output_name}_final.mp4"
    if (ROOT_DIR / "outputs" / f"{output_name}_raw.mp4").exists(): # Pipeline produces _final after subtitles
        print(f"✅ Factory Success: {final_video}")

if __name__ == "__main__":
    run_weekly_production()
