import warnings
from pathlib import Path

import whisper
from tqdm import tqdm

# Suppress FP16 warning on CPU
warnings.filterwarnings("ignore")

CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
TRANSCRIPTS_DIR = CONTEXT_DIR / "transcripts"
SUPPORTED_EXTS = {".mp3", ".mp4", ".m4a", ".wav", ".mov"}


def transcribe_all():
    print("🎙 Loading Whisper model (base)...")
    # Using 'base' for speed on CPU/MPS, can upgrade to 'small' or 'medium' if needed
    model = whisper.load_model("base")

    if not TRANSCRIPTS_DIR.exists():
        TRANSCRIPTS_DIR.mkdir()

    files = [f for f in CONTEXT_DIR.iterdir() if f.suffix.lower() in SUPPORTED_EXTS]
    print(f"📂 Found {len(files)} media files in Context.")

    for file_path in tqdm(files, desc="Transcribing"):
        output_file = TRANSCRIPTS_DIR / f"{file_path.stem}.txt"

        if output_file.exists():
            continue

        print(f"🗣 Processing: {file_path.name}")
        try:
            result = model.transcribe(str(file_path))
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(result["text"].strip())
            print(f"✅ Saved: {output_file.name}")
        except Exception as e:
            print(f"❌ Error transcribing {file_path.name}: {e}")


if __name__ == "__main__":
    transcribe_all()
