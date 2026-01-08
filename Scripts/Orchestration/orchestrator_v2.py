#!/usr/bin/env python3
"""
Content Farm Orchestrator v2
Complete pipeline: Text -> Voice -> Animation -> Lip Sync -> Subtitles
Supports Russian and English voices
"""

import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
LIVE_PORTRAIT_DIR = ROOT_DIR / "LivePortrait"
WAV2LIP_DIR = ROOT_DIR / "Wav2Lip"
OUTPUT_DIR = ROOT_DIR / "outputs"
INPUT_DIR = ROOT_DIR / "inputs"

OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)

# Voice options
VOICES = {
    "en": "en-US-ChristopherNeural",  # English male
    "en_female": "en-US-JennyNeural",  # English female  
    "ru": "ru-RU-DmitryNeural",         # Russian male
    "ru_female": "ru-RU-SvetlanaNeural" # Russian female
}

def generate_audio(text: str, output_path: Path, lang: str = "en") -> bool:
    """Generate audio using Edge-TTS"""
    print(f"🎤 Generating Audio ({lang})...")
    
    voice = VOICES.get(lang, VOICES["en"])
    mp3_path = output_path.with_suffix(".mp3")
    
    cmd = ["edge-tts", "--text", text, "--write-media", str(mp3_path), "--voice", voice]
    
    try:
        subprocess.run(cmd, check=True, cwd=str(ROOT_DIR))
        # Convert to WAV
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3_path),
            "-ar", "16000", "-ac", "1", str(output_path)
        ], check=True, capture_output=True)
        print(f"✅ Audio: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Audio failed: {e}")
        return False

def animate_face(image_path: Path, driver_path: Path) -> Path:
    """Animate face using LivePortrait"""
    print(f"🎬 Animating face...")
    
    cmd = [
        sys.executable, str(LIVE_PORTRAIT_DIR / "inference.py"),
        "--source", str(image_path),
        "--driving", str(driver_path),
        "--output-dir", str(OUTPUT_DIR)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        output_name = f"{image_path.stem}--{driver_path.stem}.mp4"
        print(f"✅ Animation: {OUTPUT_DIR / output_name}")
        return OUTPUT_DIR / output_name
    except Exception as e:
        print(f"❌ Animation failed: {e}")
        return None

def lip_sync(video_path: Path, audio_path: Path, output_path: Path) -> bool:
    """Apply lip sync using Wav2Lip"""
    print(f"👄 Applying lip sync...")
    
    venv_python = ROOT_DIR / "venv_wav2lip/bin/python3"
    
    cmd = [
        str(venv_python), str(WAV2LIP_DIR / "inference.py"),
        "--checkpoint_path", str(WAV2LIP_DIR / "checkpoints/wav2lip.pth"),
        "--face", str(video_path),
        "--audio", str(audio_path),
        "--outfile", str(output_path)
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=str(WAV2LIP_DIR))
        print(f"✅ Lip sync: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Lip sync failed: {e}")
        return False

def add_subtitles(video_path: Path, output_path: Path, lang: str = "en") -> bool:
    """Add dynamic subtitles using PyCaps"""
    print(f"📝 Adding subtitles...")
    
    cmd = [
        "pycaps", "render",
        "--input", str(video_path),
        "--output", str(output_path),
        "--lang", lang[:2],
        "--layout-align", "bottom",
        "--video-quality", "high",
        "--whisper-model", "base"
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=str(ROOT_DIR))
        print(f"✅ Subtitles: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Subtitles failed: {e}")
        return False

def run_pipeline(text: str, image_path: Path, lang: str = "en", output_name: str = "final"):
    """Run complete pipeline"""
    print(f"\n🚀 Starting Content Farm Pipeline (lang={lang})")
    print(f"📝 Text: {text[:50]}...")
    
    audio_path = INPUT_DIR / f"speech_{lang}.wav"
    driver = LIVE_PORTRAIT_DIR / "assets/examples/driving/d0.mp4"
    
    # 1. Generate Audio
    if not generate_audio(text, audio_path, lang):
        return None
    
    # 2. Animate Face
    animated = animate_face(image_path, driver)
    if not animated or not animated.exists():
        return None
    
    # 3. Lip Sync
    lipsync_path = OUTPUT_DIR / f"{output_name}_lipsync.mp4"
    if not lip_sync(animated, audio_path, lipsync_path):
        return None
    
    # 4. Add Subtitles
    final_path = OUTPUT_DIR / f"{output_name}_final.mp4"
    if not add_subtitles(lipsync_path, final_path, lang):
        return lipsync_path  # Return without subtitles if failed
    
    print(f"\n✅ Pipeline complete: {final_path}")
    return final_path

if __name__ == "__main__":
    # Russian text demo
    russian_text = "Привет! Я новый AI блогер. Я создан с помощью нейросетей и говорю на русском языке."
    english_text = "Hello! I am a new AI blogger. I was created using neural networks and I speak English."
    
    image = LIVE_PORTRAIT_DIR / "assets/examples/source/igor_wings.png"
    
    # Generate Russian version
    run_pipeline(russian_text, image, lang="ru", output_name="igor_ru")
    
    # Generate English version
    # run_pipeline(english_text, image, lang="en", output_name="igor_en")
