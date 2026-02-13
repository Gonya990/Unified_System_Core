import os
import subprocess
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv(".env")
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in .env")
    exit(1)

client = OpenAI(api_key=api_key)

# OpenAI Whisper limit is 25MB
MAX_FILE_SIZE_MB = 24


def get_file_size_mb(path):
    return os.path.getsize(path) / (1024 * 1024)


def split_audio(file_path, output_dir):
    """Splits audio/video into 10-minute chunks to stay under 25MB."""
    print(f"Splitting: {file_path}")
    stem = Path(file_path).stem
    chunk_pattern = os.path.join(output_dir, f"{stem}_chunk_%03d.mp3")

    # Extract audio and split into 10m chunks. 10m of 128kbps MP3 is ~10MB.
    cmd = [
        "ffmpeg",
        "-i",
        str(file_path),
        "-f",
        "segment",
        "-segment_time",
        "600",
        "-acodec",
        "libmp3lame",
        "-ab",
        "128k",
        chunk_pattern,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sorted(Path(output_dir).glob(f"{stem}_chunk_*.mp3"))


def transcribe_chunk(chunk_path):
    print(f"Transcribing chunk: {chunk_path.name}")
    try:
        with open(chunk_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
        return transcript
    except Exception as e:
        print(f"Error transcribing chunk {chunk_path.name}: {e}")
        return ""


def process_file(file_path, transcription_dir, temp_dir):
    file_path = Path(file_path)
    output_file = transcription_dir / f"{file_path.stem}.txt"

    if output_file.exists():
        print(f"Skipping {file_path.name}, already exists.")
        return

    # For OpenAI we always convert to MP3/split because even small videos might be >25MB
    # and Whisper-1 prefers small audio files.
    chunks = split_audio(file_path, temp_dir)

    full_transcript = []
    for chunk in chunks:
        text = transcribe_chunk(chunk)
        if text:
            full_transcript.append(text)
        # Cleanup chunk
        os.remove(chunk)

    if full_transcript:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(full_transcript))
        print(f"✅ Saved transcript: {output_file.name}")


def main():
    root_dir = Path(".")
    transcription_dir = Path("Transcriptions")
    temp_dir = Path("tmp_audio_chunks")

    transcription_dir.mkdir(exist_ok=True)
    temp_dir.mkdir(exist_ok=True)

    # Find all media files
    extensions = [".mp4", ".m4a"]
    media_files = []
    for ext in extensions:
        media_files.extend(list(root_dir.glob(f"**/*{ext}")))

    # Unique files, ignoring trash
    seen = set()
    to_process = []
    for f in media_files:
        if f.name in seen or "tmp/" in str(f) or ".venv" in str(f) or "Projects/AI_Core/antibridge.worktrees" in str(f):
            continue
        seen.add(f.name)
        to_process.append(f)

    print(f"Found {len(to_process)} files to process.")

    for i, file_path in enumerate(to_process):
        print(f"\n[{i + 1}/{len(to_process)}] Processing: {file_path}")
        process_file(file_path, transcription_dir, temp_dir)

    # Final cleanup
    if temp_dir.exists():
        import shutil

        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    main()
