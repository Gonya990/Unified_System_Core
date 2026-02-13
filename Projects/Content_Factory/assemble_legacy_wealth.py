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
    print("🎬 RE-PROCESSING: Legacy Wealth Short (Speed 1.15x, Fixed Year)...")

    orchestrator.broker = None
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    day_str = datetime.now().strftime("%Y-%m-%d")
    assets_dir = ROOT_DIR / "Local_Dev" / "Media" / "legacy_wealth" / day_str

    # Phonetic year to ensure 'Две тысячи двадцать шестой'
    script_ru = """
Почему девяносто процентов предпринимателей провалятся в две тысячи двадцать шестом году? 🛑

Потому что они застряли в модели 'работа за деньги'. Трамп всегда говорил: 'Думай масштабно'. Кийосаки учил: 'Заставляй деньги работать на себя'. 📉

Сегодня Масштаб - это не сотрудники. Это Эй-Ай Оркестрация. 🤖

Ваш бизнес в две тысячи двадцать шестом - это не офис. Это сеть автономных агентов. Один пишет код, второй ведет продажи, третий - анализирует рынки. Пока вы спите. 😴

Это не будущее. Это то, что мы строим в Unified System Core прямо сейчас. 🏗️

Хочешь узнать стратегию 'Основателя две тысячи двадцать шестого'? Как объединить жесткость Трампа и логику активов Кийосаки с мощью ИИ?

Подписывайся. Время одиночек прошло. Пришло время дирижеров цифровых империй. 👑
"""

    assets = [
        {"image": str(assets_dir / "scene_1_hook.jpg"), "keyword": "stressed entrepreneur"},
        {"image": str(assets_dir / "scene_2_trump_kiyosaki.jpg"), "keyword": "trump kiyosaki"},
        {"image": str(assets_dir / "scene_3_ai_core.jpg"), "keyword": "ai core neural"},
        {"image": str(assets_dir / "scene_4_orchestrator.jpg"), "keyword": "orchestrator conductor"},
        {"image": str(assets_dir / "scene_5_sovereign_living.jpg"), "keyword": "sovereign living"},
        {"image": str(assets_dir / "scene_6_cta.jpg"), "keyword": "cta light"},
    ]

    orchestrator.INPUT_DIR = assets_dir
    orchestrator.OUTPUT_DIR = assets_dir
    orchestrator.BROLL_DIR = ROOT_DIR / "broll"

    # Monkey-patch generate_audio to support speedup
    original_gen_audio = orchestrator.generate_audio

    def speed_up_audio(text, output_path, lang="en"):
        if original_gen_audio(text, output_path, lang):
            print("⚡ Speeding up audio (1.15x)...")
            temp_path = output_path.with_suffix(".tmp.wav")
            output_path.rename(temp_path)
            subprocess.run(
                ["ffmpeg", "-y", "-i", str(temp_path), "-filter:a", "atempo=1.15", str(output_path)], check=True
            )
            return True
        return False

    orchestrator.generate_audio = speed_up_audio

    final_video = orchestrator.run_no_face_pipeline(
        text=script_ru, lang="ru", output_name="legacy_wealth_short_v2", scenes=assets, style="impact"
    )

    if final_video:
        print(f"🎉 SUCCESS! V2 video: {final_video}")
    else:
        print("❌ Assembly failed.")


if __name__ == "__main__":
    run_assembly()
