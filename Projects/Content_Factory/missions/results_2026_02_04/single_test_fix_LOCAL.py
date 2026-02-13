import os
import subprocess
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv("/home/gonya/Unified_System_Core/Projects/Content_Factory/.env")
os.environ["PEXELS_API_KEY"] = os.getenv("PEXELS_API_KEY", "")
os.environ["ELEVENLABS_API_KEY"] = os.getenv("ELEVENLABS_API_KEY", "")

FACTORY_ROOT = "/home/gonya/Unified_System_Core/Projects/Content_Factory"
sys.path.append(os.path.join(FACTORY_ROOT, "src"))
sys.path.append(os.path.join(FACTORY_ROOT, "src/pipeline"))

from orchestrator_v3_no_face import run_no_face_pipeline


def run_test():
    print("🚀 Testing FIXED Pipeline (Padding + Pexels)...")
    text = "Это тестовое видео для проверки длительности. Мы добавили буфер времени к каждой сцене, чтобы видеоряд гарантированно перекрывал аудиодорожку. Теперь текст не должен обрываться на полуслове."

    scenes = [
        {"keyword": "clock time lapse"},
        {"keyword": "engineering blueprint"},
        {"keyword": "green checkmark success"},
    ]

    name = f"TEST_FIX_{int(time.time())}"
    try:
        run_no_face_pipeline(text=text, lang="ru", output_name=name, scenes=scenes, style="impact")

        output_file = Path(FACTORY_ROOT) / f"outputs/{name}_final.mp4"
        if output_file.exists():
            caption = "🛡️ <b>FIX TEST</b>\n\nAudio Length Check.\nScene buffer applied."
            subprocess.run(
                [
                    "curl",
                    "-F",
                    f"video=@{output_file}",
                    "-F",
                    "chat_id=708531393",
                    "-F",
                    f"caption={caption}",
                    "-F",
                    "parse_mode=HTML",
                    "https://api.telegram.org/bot8518131338:AAHtcEgI--E2Fktdo3nE3oynhzq1gvrVON4/sendVideo",
                ]
            )
            print(f"📤 Sent {name}")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    run_test()
