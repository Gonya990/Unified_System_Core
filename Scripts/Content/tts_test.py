import os
import torch
from TTS.api import TTS

# Configuration
BIOMETRICS_DIR = "secure_vault/biometrics"
OUTPUT_DIR = "Projects/Content_Factory/outputs/tests"
MODEL_NAME = "tts_models/multilingual/multi-dataset/xtts_v2"


def run_tts_test():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Check for GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if torch.backends.mps.is_available():
        device = "mps"

    print(f"🔊 Initializing XTTS v2 on device: {device}")

    # Initialize TTS
    try:
        tts = TTS(MODEL_NAME).to(device)
    except Exception as e:
        print(f"❌ Failed to load TTS model: {e}")
        return

    # Characters to test
    characters = {
        "unit_x": "Hello, I am Unit-X. All systems are operational.",
        "spark": "Hey! Spark here! Let's build something awesome!",
        "holo_cat": "Greetings. This is Holo-Cat. Parameters are stable.",
    }

    print("\nStarting Voice Cloning Test...\n")

    for char_name, text in characters.items():
        ref_path = os.path.join(BIOMETRICS_DIR, char_name, "ref.wav")
        output_path = os.path.join(OUTPUT_DIR, f"test_{char_name}.wav")

        if not os.path.exists(ref_path):
            print(f"⚠️ Skipping {char_name}: No reference audio found at {ref_path}")
            continue

        print(f"🎙️ Cloning {char_name}...")
        try:
            tts.tts_to_file(text=text, speaker_wav=ref_path, language="en", file_path=output_path)
            print(f"✅ Generated: {output_path}")
        except Exception as e:
            print(f"❌ Error generating {char_name}: {e}")

    print("\nTest Complete.")


if __name__ == "__main__":
    run_tts_test()
