import json
import re
import sys
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

# Paths
CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent.parent.parent.parent
# Load environment variables
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
AUDIO_DIR = CONTEXT_DIR / "audio_output"
BIOMETRICS_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/secure_vault/biometrics")

if not AUDIO_DIR.exists():
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# XTTS Model Configuration
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
if torch.backends.mps.is_available():
    DEVICE = "mps"


def parse_script(lines):
    """
    Parse script content from lines (JSON or text).
    """
    content = "".join(lines)

    # Try to find JSON block
    json_match = re.search(r"```json\s*([\s\S]*?)\s*```", content)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            print("⚠️ Failed to parse Markdown JSON, trying raw content...")

    # Try raw JSON
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "segments" in data:
            return data["segments"]
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    # Fallback to line-by-line parsing
    print("⚠️ JSON parse failed, falling back to text parsing.")
    script_data = []

    for line in lines:
        text = line.strip()
        if not text:
            continue

        role = "Unknown"
        if any(kw in text for kw in ["Skeptic", "Host 1", "Rex", "T-Rex"]):
            role = "Skeptic"
            text = re.sub(r"^(Host 1|Skeptic|Rex|T-Rex):", "", text).strip()
        elif any(kw in text for kw in ["Enthusiast", "Host 2", "Trike", "Triceratops"]):
            role = "Enthusiast"
            text = re.sub(r"^(Host 2|Enthusiast|Trike|Triceratops):", "", text).strip()

        if text:
            script_data.append({"role": role, "text": text})

    return script_data


def generate_voiceover_xtts(script_path):
    print(f"🎤 Generating XTTS v2 Voiceover for: {script_path.name}...")

    with open(script_path) as f:
        lines = f.readlines()

    script_data = parse_script(lines)
    audio_segments = []

    # Initialize TTS
    print(f"⏳ Loading XTTS model ({DEVICE})...")
    try:
        tts = TTS(MODEL_NAME).to(DEVICE)
    except Exception as e:
        print(f"❌ Failed to load TTS model: {e}")
        return

    # Define Reference Voices
    # Rex (Skeptic) -> Unit-X (Analytical/Deep)
    # Trike (Enthusiast) -> Spark (Energetic/Fast)
    ref_rex = BIOMETRICS_DIR / "unit_x/ref.wav"
    ref_trike = BIOMETRICS_DIR / "spark/ref.wav"

    if not ref_rex.exists() or not ref_trike.exists():
        print(f"❌ Missing biometric reference files in {BIOMETRICS_DIR}")
        return

    for i, line in enumerate(script_data):
        role = line.get("role", "Unknown")
        text = line.get("text", "")

        if not text:
            continue

        # Select Voice
        speaker_wav = str(ref_rex) if (role == "Skeptic" or "Rex" in role) else str(ref_trike)

        print(f"  🗣️ {role}: {text[:30]}...")

        output_segment_path = AUDIO_DIR / f"segment_{i}_{role}.wav"

        try:
            # Generate Audio via XTTS
            # Check if text contains cyrillic to set language?
            is_cyrillic = bool(re.search("[а-яА-Я]", text))
            lang = "ru" if is_cyrillic else "en"

            tts.tts_to_file(
                text=text,
                speaker_wav=speaker_wav,
                language=lang,
                file_path=str(output_segment_path),
            )

            # Add to list
            audio_segments.append(AudioFileClip(str(output_segment_path)))

        except Exception as e:
            print(f"❌ Error generating speech for line {i}: {e}")
            continue

    if audio_segments:
        final_audio = concatenate_audioclips(audio_segments)
        # Save as MP3
        output_path = AUDIO_DIR / f"{script_path.stem}.mp3"
        final_audio.write_audiofile(str(output_path))
        print(f"✅ XTTS Audio saved: {output_path.name}")
    else:
        print("❌ No audio generated.")


if __name__ == "__main__":
    SCRIPTS_DIR = CONTEXT_DIR / "scripts"

    if len(sys.argv) > 1:
        script_file = Path(sys.argv[1])
        if script_file.exists():
            generate_voiceover_xtts(script_file)
        else:
            print(f"❌ File not found: {script_file}")
    else:
        # Process all script files in SCRIPTS dir
        if not SCRIPTS_DIR.exists():
            print(f"❌ Scripts directory not found: {SCRIPTS_DIR}")
            sys.exit(1)

        script_files = list(SCRIPTS_DIR.glob("*_script.md")) + list(SCRIPTS_DIR.glob("*.json"))
        if not script_files:
            print(f"❌ No script files found in {SCRIPTS_DIR}.")

        for f_path in script_files:
            generate_voiceover_xtts(f_path)
