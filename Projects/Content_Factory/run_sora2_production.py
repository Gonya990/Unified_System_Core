#!/usr/bin/env python3
"""
Quick production run using multi-source research
Based on Sora 2 script idea (Viral Potential: 9/10)
"""
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Setup paths
ROOT_DIR = Path(__file__).parent.parent.parent
SRC_DIR = Path(__file__).parent / "src"

sys.path.insert(0, str(SRC_DIR / "researcher"))
sys.path.insert(0, str(SRC_DIR / "pipeline"))
sys.path.insert(0, str(SRC_DIR / "video"))

from daily_researcher import generate_vision_assets

# Load latest multi-source research
reports_dir = ROOT_DIR / "Reports"
report_files = sorted(reports_dir.glob('multi_source_research_*.json'))
if not report_files:
    print("❌ No research reports found")
    sys.exit(1)

latest_report = report_files[-1]
print(f"📊 Loading research: {latest_report.name}")

with open(latest_report) as f:
    research_data = json.load(f)

# Get Sora 2 script idea (index 1, Viral Potential: 9/10)
script_idea = research_data['script_ideas'][1]

print("\n🎬 SELECTED SCRIPT IDEA:")
print(f"Title: {script_idea['Title']}")
print(f"Viral Potential: {script_idea['Viral Potential']}/10")
print()

# Prepare content for production
content_data = {
    'selected_topic': script_idea['Title'],
    'description': script_idea['Hook'],
    'script_ru': '''
Стоп! Собираешься платить 200 долларов за Sora 2?

Есть способ получить безлимитный доступ... абсолютно бесплатно.

Без кучи почт. Без подписок.

Sora 2 от OpenAI - революция в генерации видео. Качество космическое.

Но цена? 200 долларов в месяц.

Я нашел метод... который проверили уже больше 1700 человек.

Он работает прямо сейчас... но нет гарантии что завтра не закроют.

Записывай и используй пока можно.

Первый шаг - Temp Mail. Временная почта... бесплатно.

Второй шаг - DIGEN AI. Регистрация за минуту.

Третий шаг - повторяй для безлимита.

Улучшай качество через Topaz AI... создавай невероятное.

Но помни... с большими возможностями приходит большая ответственность.

Не создавай фейки... не распространяй дезинформацию.

Используй для обучения... для созидания.

Будь адекватен. Это момент истины... для всего сообщества.

Творцы новой реальности... это мы.
''',
    'scenes': [
        {'image': 'sora2_scene1', 'keyword': 'futuristic ai video generation sora 2 interface glowing'},
        {'image': 'sora2_scene2', 'keyword': 'expensive subscription money cash dollars price tag'},
        {'image': 'sora2_scene3', 'keyword': 'free unlimited access digital freedom liberation light'},
        {'image': 'sora2_scene4', 'keyword': 'temporary email service web browser interface'},
        {'image': 'sora2_scene5', 'keyword': 'ai neural network video creation technology'},
        {'image': 'sora2_scene6', 'keyword': 'youtube shorts viral content success engagement'},
        {'image': 'sora2_scene7', 'keyword': 'quality enhancement upscale 4k crystal clear'},
        {'image': 'sora2_scene8', 'keyword': 'responsibility ethics digital citizenship'},
        {'image': 'sora2_scene9', 'keyword': 'creative innovation future technology vision'}
    ]
}

print(f"📝 Script: {len(content_data['script_ru'].split())} words")
print(f"🎨 Scenes: {len(content_data['scenes'])} visuals")
print()

# Generate visual assets
day_str = datetime.now().strftime('%Y-%m-%d')
assets_dir = ROOT_DIR / "Local_Dev" / "Media" / "sora2_production" / day_str
assets_dir.mkdir(parents=True, exist_ok=True)

print(f"🎨 Generating visual assets in {assets_dir}...")
print()

try:
    assets = generate_vision_assets(content_data['scenes'], assets_dir, style="impact")

    final_scenes = []
    for a in assets:
        if a.get('resolved_path'):
            final_scenes.append({"image": a['resolved_path'], "keyword": a['keyword']})

    print(f"\n✅ Assets ready: {len(final_scenes)}/{len(content_data['scenes'])} scenes downloaded")

    if not final_scenes:
        print("❌ No assets generated. Aborting.")
        sys.exit(1)

    # Save production config
    production_config = {
        'timestamp': datetime.now().isoformat(),
        'research_source': latest_report.name,
        'script_idea': script_idea,
        'content': content_data,
        'assets': final_scenes,
        'status': 'assets_ready'
    }

    config_path = assets_dir / "production_config.json"
    with open(config_path, 'w') as f:
        json.dump(production_config, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Production config saved: {config_path}")
    print()
    print("🎬 NEXT STEPS:")
    print(f"1. Review assets in: {assets_dir}")
    print(f"2. Run video production with orchestrator_v3_no_face.py")
    print(f"3. Script text is in production_config.json")
    print()
    print("📊 VIRAL POTENTIAL: 9/10")
    print("🎯 BASED ON: 1,730 views on Telegram @vitalycontentcreate")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
