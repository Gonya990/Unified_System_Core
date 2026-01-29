import os
import time
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in .env")
    exit(1)

genai.configure(api_key=api_key)

def transcribe_file(file_path):
    print(f"Processing: {file_path}")
    try:
        # Upload the file
        uploaded_file = genai.upload_file(path=str(file_path))
        print(f"Uploaded {file_path.name}. Waiting for processing...")

        # Wait for the file to be processed
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = genai.get_file(uploaded_file.name)

        if uploaded_file.state.name == "FAILED":
            raise Exception("File processing failed.")

        # Use the Gemini model to transcribe
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            "Please transcribe this audio/video file accurately and completely in its original language. If there are multiple speakers, label them if possible. Output ONLY the transcription text.",
            uploaded_file
        ])

        # Delete the file from Gemini storage
        genai.delete_file(uploaded_file.name)

        return response.text
    except Exception as e:
        print(f"Error transcribing {file_path.name}: {e}")
        return None

def main():
    root_dir = Path(".")
    transcription_dir = Path("Transcriptions")
    transcription_dir.mkdir(exist_ok=True)

    # Find all media files
    extensions = [".mp4", ".m4a"]
    media_files = []
    for ext in extensions:
        media_files.extend(list(root_dir.glob(f"**/*{ext}")))

    # Unique files and skip those already transcribed
    seen = set()
    to_process = []
    for f in media_files:
        if f.name in seen or "tmp/" in str(f) or ".venv" in str(f):
            continue
        
        output_name = transcription_dir / f"{f.stem}.txt"
        if output_name.exists():
            print(f"Skipping {f.name}, already transcribed.")
            continue
            
        seen.add(f.name)
        to_process.append(f)

    print(f"Found {len(to_process)} new files to transcribe.")

    for i, file_path in enumerate(to_process):
        print(f"[{i+1}/{len(to_process)}] {file_path}")
        transcript = transcribe_file(file_path)
        
        if transcript:
            output_file = transcription_dir / f"{file_path.stem}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(transcript)
            print(f"Saved: {output_file}")
        
        # Avoid rate limits
        time.sleep(5)

if __name__ == "__main__":
    main()
