import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path("/home/gonya/Unified_System_Core")
SRC_DIR = Path("/home/gonya/Unified_System_Core/Projects/Content_Factory/src")

load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

sys.path.append(str(SRC_DIR / "pipeline"))
sys.path.append(str(SRC_DIR / "video"))
sys.path.append(str(SRC_DIR / "researcher"))
sys.path.append(str(ROOT_DIR / "Scripts/Utilities"))

import orchestrator_v3_no_face as orchestrator


def run_assembly():
    print("🎬 V3 ASSEMBLY: PEXELS + AI (Fast & Kinetic)...")

    # RE-VALIDATE PEXELS KEY
    pexels_key = os.getenv("PEXELS_API_KEY")
    print(f"🔑 PEXELS KEY IN ENV: {pexels_key[:5] if pexels_key else 'MISSING'}...")

    orchestrator.broker = None
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["PEXELS_API_KEY"] = pexels_key

    day_str = datetime.now().strftime("%Y-%m-%d")
    assets_dir = ROOT_DIR / "Local_Dev" / "Media" / "legacy_wealth_v3" / day_str

    script_ru = """
Почему девяносто процентов предпринимателей провалятся в две тысячи двадцать шестом году? 🛑
Потому что они застряли в модели 'работа за деньги'. Трамп всегда говорил: 'Думай масштабно'. Кийосаки учил: 'Заставляй деньги работать на себя'. 📉
Сегодня Масштаб - это не сотрудники. Это Эй-Ай Оркестрация. 🤖
Ваш бизнес в две тысячи двадцать шестом - это не офис. Это сеть автономных агентов. Один пишет код, второй ведет продажи, третий - анализирует рынки. Пока вы спите. 😴
Это не будущее. Это то, что мы строим в Unified System Core прямо сейчас. 🏗️
Хочешь узнать стратегию 'Основателя две тысячи двадцать шестого'? Как объединить жесткость Трампа и логику активов Кийосаки с мощью ИИ?
Подписывайся. Время одиночек прошло. Пришло время дирижеров цифровых империй. 👑
"""

    # Assets will be filled by the actual files on disk
    assets = [
        {
            "image": str(assets_dir / "scene_1_hook.jpg"),
            "keyword": "business man laptop city office cinematic handheld",
        },
        {"image": str(assets_dir / "scene_2_trump_kiyosaki.jpg"), "keyword": "luxury wealth gold coins assets success"},
        {"image": str(assets_dir / "scene_3_ai_core.jpg"), "keyword": "tech server room blue light data abstract"},
        {
            "image": str(assets_dir / "scene_4_orchestrator.jpg"),
            "keyword": "epic orchestra conductor silhouette stage lighting",
        },
        {
            "image": str(assets_dir / "scene_5_sovereign_living.jpg"),
            "keyword": "modern luxury mansion pool aerial cinematic",
        },
        {"image": str(assets_dir / "scene_6_cta.jpg"), "keyword": "mountain peak sunrise triumph success"},
    ]

    orchestrator.INPUT_DIR = assets_dir
    orchestrator.OUTPUT_DIR = assets_dir
    orchestrator.BROLL_DIR = ROOT_DIR / "broll"

    def speed_up_audio(text, output_path, lang="en"):
        if orchestrator.generate_audio_openai(text, output_path, "alloy"):
            print("⚡ Speeding up audio (1.15x)...")
            temp_path = output_path.with_suffix(".tmp.wav")
            output_path.rename(temp_path)
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(temp_path), "-filter:a", "atempo=1.15", str(output_path)], check=True
            )
            return True
        return False

    orchestrator.generate_audio = speed_up_audio

    print("🚀 Starting HYBRID Pipeline (Pexels enabled via ENV)...")
    final_video = orchestrator.run_no_face_pipeline(
        text=script_ru, lang="ru", output_name="legacy_wealth_v3_hybrid", scenes=assets, style="impact"
    )

    if final_video:
        print(f"🎉 SUCCESS! V3 HYBRID video: {final_video}")
    else:
        print("❌ Assembly failed.")


if __name__ == "__main__":
    run_assembly()
