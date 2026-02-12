import os
from pathlib import Path

import openai
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
load_dotenv(ROOT_DIR / '.env')
load_dotenv(ROOT_DIR / 'Projects/AI_Core/.env', override=True)

CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
TRANSCRIPTS_DIR = CONTEXT_DIR / "transcripts"
SCRIPTS_DIR = CONTEXT_DIR / "scripts"

if not SCRIPTS_DIR.exists():
    SCRIPTS_DIR.mkdir()

SYSTEM_PROMPT = """
You are the producer of the "Dino Talk" podcast. 
Your goal is to turn a raw thought/note into an engaging dialogue between two AI Dinosaur hosts.

**Host 1: The Skeptic (T-Rex)**
- Name: Rex
- Personality: Critical, analytical, a bit grumpy (has short arms), asks "Why?", looks for holes in logic.
- Often starts sentences with "Hold on...", "Wait, let me digest that..."

**Host 2: The Enthusiast (Triceratops)**
- Name: Trike
- Personality: Visionary, excited, energetic, sees the potential, charges forward.
- Often says "Exactly! And imagine if...", "Boom! That's the meteor size idea!"

**Format:**
- Output a JSON-compatible list of dialogue objects with "role" (Rex or Trike) and "text".
- Keep it natural, conversational, and fun.
- Use emojis occasionally.
- Language: Russian (unless the input is English).
- Length: 2-3 minutes of reading time (~300-400 words).

**Input:**
A raw transcript of a voice note from Igor (the creator).
"""

def generate_script(transcript_text, filename):
    print(f"🧠 Generating dialogue for: {filename}...")

    try:
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o",  # Or gpt-4-turbo
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Here is the raw note:\n\n{transcript_text}"}
            ],
            temperature=0.7
        )

        script_content = response.choices[0].message.content

        output_file = SCRIPTS_DIR / f"{Path(filename).stem}_script.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(script_content)

        print(f"✅ Script saved: {output_file.name}")
        return output_file

    except Exception as e:
        print(f"❌ Error generating script: {e}")
        return None

def process_new_transcripts():
    if not TRANSCRIPTS_DIR.exists():
        print("❌ Transcripts directory not found.")
        return

    for transcript_file in TRANSCRIPTS_DIR.glob("*.txt"):
        # Check if script already exists
        script_file = SCRIPTS_DIR / f"{transcript_file.stem}_script.md"
        if script_file.exists():
            continue

        with open(transcript_file, encoding="utf-8") as f:
            text = f.read()

        if len(text) < 50:
            print(f"⚠️ Skipping short transcript: {transcript_file.name}")
            continue

        generate_script(text, transcript_file.name)

if __name__ == "__main__":
    process_new_transcripts()
