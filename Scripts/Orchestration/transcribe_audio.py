import os
import sys
from pathlib import Path

# Add necessary paths
ROOT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core")
sys.path.append(str(ROOT_DIR / "Scripts" / "Utilities"))
from token_broker import TokenBroker


def transcribe_audio(file_path):
    broker = TokenBroker()
    api_key = broker.get_key("gemini")

    if not api_key:
        print("Error: No Gemini API key found.")
        return

    from google import genai

    client = genai.Client(api_key=api_key)

    print(f"Uploading and transcribing {file_path}...")

    # Upload the file
    file_uri = client.files.upload(file=file_path)

    print(f"File uploaded to {file_uri.name}. Starting generation...")
    # Generate content
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                file_uri,
                "Please provide a complete transcript of this audio file (in Russian/English as spoken). "
                "Then, summarize the core logic regarding 'personality protection' and system security discussed."
            ]
        )
        print("Generation complete.")
        output_text = response.text
    except Exception as e:
        print(f"Generation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    print("\n--- TRANSCRIPTION & ANALYSIS ---\n")
    print(output_text)

    # Save to Context/transcripts
    transcript_path = ROOT_DIR / "Context" / "transcripts" / (Path(file_path).stem + "_full.txt")
    transcript_path.parent.mkdir(parents=True, exist_ok=True)
    transcript_path.write_text(output_text)
    print(f"\nSaved to {transcript_path}")

if __name__ == "__main__":
    audio_file = "/Users/igorgoncharenko/Documents/Unified_System_Core/Context/crypto_billions_threat.m4a"
    if os.path.exists(audio_file):
        transcribe_audio(audio_file)
    else:
        print(f"File not found: {audio_file}")
