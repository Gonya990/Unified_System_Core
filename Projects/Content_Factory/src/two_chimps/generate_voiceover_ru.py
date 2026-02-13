import json
import re
from pathlib import Path

import torch
from dotenv import load_dotenv
from moviepy.editor import AudioFileClip, concatenate_audioclips
from TTS.api import TTS
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.configs.xtts_config import XttsConfig
from TTS.tts.models.xtts import XttsArgs, XttsAudioConfig

# Fix for torch.load weights_only=True issue
try:
    torch.serialization.add_safe_globals([XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs])
except AttributeError:
    pass  # Older torch versions don't need this

# Пути
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent.parent.parent
# Загрузка переменных окружения
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
AUDIO_DIR = CONTEXT_DIR / "audio_output"
BIOMETRICS_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/secure_vault/biometrics")

if not AUDIO_DIR.exists():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Конфигурация модели XTTS
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
if torch.backends.mps.is_available():
    DEVICE = "mps"


def parse_script(lines):
    """
    Парсит содержимое сценария из строк (JSON или текст).
    """
    content = "".join(lines)

    # Попытка найти блок JSON
    json_match = re.search(r"```json\s*([\s\S]*?)\s*```", content)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            print("⚠️ Не удалось разобрать Markdown JSON, пробуем сырое содержимое...")

    # Попытка разобрать сырой JSON
    try:
        data = json.loads(content)
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Откат к построчному разбору
    print("⚠️ Разбор JSON не удался, переходим к текстовому разбору.")
    script_data = []

    for line in lines:
        text = line.strip()
        if not text:
            continue

        role = "Unknown"
        if "Skeptic" in text or "Host 1" in text or "Rex" in text or "T-Rex" in text:
            role = "Skeptic"
            text = re.sub(r"^(Host 1|Skeptic|Rex|T-Rex):", "", text).strip()
        elif "Enthusiast" in text or "Host 2" in text or "Trike" in text or "Triceratops" in text:
            role = "Enthusiast"
            text = re.sub(r"^(Host 2|Enthusiast|Trike|Triceratops):", "", text).strip()

        if text:
            script_data.append({"role": role, "text": text})

    return script_data


def generate_voiceover_xtts(script_file):
    print(f"🎤 Генерация озвучки XTTS v2 для: {script_file.name}...")

    with open(script_file) as f:
        lines = f.readlines()

    script_data = parse_script(lines)
    audio_segments = []

    # Инициализация TTS
    print(f"⏳ Загрузка модели XTTS ({DEVICE})...")
    try:
        tts = TTS(MODEL_NAME).to(DEVICE)
    except Exception as e:
        print(f"❌ Не удалось загрузить модель TTS: {e}")
        return

    # Определение референсных голосов
    # Рекс (Скептик) -> Unit-X (Аналитический/Глубокий)
    # Трайк (Энтузиаст) -> Spark (Энергичный/Быстрый)
    ref_rex = BIOMETRICS_DIR / "unit_x/ref.wav"
    ref_trike = BIOMETRICS_DIR / "spark/ref.wav"

    if not ref_rex.exists() or not ref_trike.exists():
        print(f"❌ Отсутствуют файлы биометрии в {BIOMETRICS_DIR}")
        return

    for i, line in enumerate(script_data):
        role = line.get("role", "Unknown")
        text = line.get("text", "")

        if not text:
            continue

        # Выбор голоса
        if role == "Skeptic" or "Rex" in role:
            speaker_wav = str(ref_rex)
        else:
            speaker_wav = str(ref_trike)

        print(f"  🗣️ {role}: {text[:30]}...")

        output_segment_path = AUDIO_DIR / f"segment_{i}_{role}.wav"

        try:
            # Генерация аудио через XTTS
            is_cyrillic = bool(re.search("[а-яА-Я]", text))
            lang = "ru" if is_cyrillic else "en"

            tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=lang,
                file_path=str(output_segment_path),
            )

            # Добавление в список
            audio_segments.append(AudioFileClip(str(output_segment_path)))

        except Exception as e:
            print(f"❌ Ошибка генерации речи для строки {i}: {e}")
            continue

    if audio_segments:
        final_audio = concatenate_audioclips(audio_segments)
        # Сохранение как MP3
        output_path = AUDIO_DIR / f"{script_file.stem}.mp3"
        final_audio.write_audiofile(str(output_path))
        print(f"✅ XTTS Аудио сохранено: {output_path.name}")

        # Очистка временных файлов - ОТКЛЮЧЕНО для премиум сборки
        # for segment in audio_segments:
        #     try:
        #         segment.close()
        #         if os.path.exists(segment.filename):
        #             os.remove(segment.filename)
        #     except Exception as e:
        #         print(f"⚠️ Ошибка очистки: {e}")
    else:
        print("❌ Аудио не сгенерировано.")


if __name__ == "__main__":
    # Обработка всех файлов сценариев в папке scripts
    SCRIPTS_DIR = CONTEXT_DIR / "scripts"
    if not SCRIPTS_DIR.exists():
        print(f"❌ Папка скриптов не найдена: {SCRIPTS_DIR}")
        exit()

    script_files = list(SCRIPTS_DIR.glob("*_script.md"))
    if not script_files:
        print(f"❌ Файлы сценариев не найдены в {SCRIPTS_DIR}.")

    for script_file in script_files:
        generate_voiceover_xtts(script_file)
