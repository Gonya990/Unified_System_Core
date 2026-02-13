import json
import os
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path("/home/gonya/Unified_System_Core")
SRC_DIR = Path("/home/gonya/Unified_System_Core/Projects/Content_Factory/src")

# Load ENV to get Pexels Key
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

sys.path.insert(0, str(SRC_DIR / "researcher"))
sys.path.insert(0, str(SRC_DIR / "pipeline"))
sys.path.insert(0, str(SRC_DIR / "video"))

from daily_researcher import generate_vision_assets


def generate_script():
    script_ru = """
Почему девяносто процентов предпринимателей провалятся в две тысячи двадцать шестом году? 🛑

Потому что они застряли в модели 'работа за деньги'. Трамп всегда говорил: 'Думай масштабно'. Кийосаки учил: 'Заставляй деньги работать на себя'. 📉

Сегодня Масштаб - это не сотрудники. Это Эй-Ай Оркестрация. 🤖

Ваш бизнес в две тысячи двадцать шестом - это не офис. Это сеть автономных агентов. Один пишет код, второй ведет продажи, третий - анализирует рынки. Пока вы спите. 😴

Это не будущее. Это то, что мы строим в Unified System Core прямо сейчас. 🏗️

Хочешь узнать стратегию 'Основателя две тысячи двадцать шестого'? Как объединить жесткость Трампа и логику активов Кийосаки с мощью ИИ?

Подписывайся. Время одиночек прошло. Пришло время дирижеров цифровых империй. 👑
"""
    return script_ru


def run():
    print("🚀 Starting HIGH-QUALITY Production with Pexels + AI Assets...")
    script = generate_script()
    # Adding more descriptive keywords for Pexels to pick up real footage
    scenes = [
        {"image": "scene_1_hook", "keyword": "stressed businessman looking at laptop city office handheld cinematic"},
        {"image": "scene_2_trump_kiyosaki", "keyword": "golden luxury interior wealth success assets"},
        {"image": "scene_3_ai_core", "keyword": "data server room glowing led technology abstract"},
        {"image": "scene_4_orchestrator", "keyword": "orchestra conductor silhouette epic lighting"},
        {"image": "scene_5_sovereign_living", "keyword": "modern luxury house architecture pool sunset sky"},
        {"image": "scene_6_cta", "keyword": "epic mountain peak sunrise clouds achievement"},
    ]

    day_str = datetime.now().strftime("%Y-%m-%d")
    assets_dir = ROOT_DIR / "Local_Dev" / "Media" / "legacy_wealth_v3" / day_str
    assets_dir.mkdir(parents=True, exist_ok=True)

    print(f"🎨 Using PEXELS API Key: {os.getenv('PEXELS_API_KEY')[:5]}...")

    try:
        # Style 'impact' will trigger Pexels fallback if Gemini/SDXL fails
        assets = generate_vision_assets(scenes, assets_dir, style="cinematic_impact")

        production_config = {
            "title": "The 2026 Founder Strategy V3",
            "script_ru": script,
            "assets_dir": str(assets_dir),
            "assets": assets,
            "timestamp": datetime.now().isoformat(),
        }

        with open(assets_dir / "production_config.json", "w", encoding="utf-8") as f:
            json.dump(production_config, f, indent=2, ensure_ascii=False)

        print("✅ V3 Assets ready (Hybrid IA + Real Footage).")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    run()
