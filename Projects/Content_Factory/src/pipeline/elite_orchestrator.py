import os
import subprocess
from pathlib import Path

try:
    from elevenlabs import generate, save, set_api_key

    HAS_ELEVEN = True
except ImportError:
    HAS_ELEVEN = False


class EliteContentOrchestrator:
    def __init__(self):
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "/home/gonya/factory_outputs"))
        self.output_dir.mkdir(exist_ok=True, parents=True)
        self.eleven_key = os.getenv("ELEVENLABS_API_KEY")
        if HAS_ELEVEN and self.eleven_key:
            set_api_key(self.eleven_key)

    def generate_elite_audio(self, text, lang="ru"):
        print("🎙 Generating ELITE Audio...")
        if not HAS_ELEVEN:
            print("⚠️ Falling back to edge-tts (No ElevenLabs)...")
            audio_path = self.output_dir / "voice.mp3"
            subprocess.run(
                ["edge-tts", "--text", text, "--write-media", str(audio_path)],
                check=True,
            )
            return audio_path

        voice = "Antoni"  # Elite
        audio = generate(text=text, voice=voice, model="eleven_multilingual_v2")
        path = self.output_dir / "elite_voice.mp3"
        save(audio, str(path))
        return path

    def run_elite_pipeline(self, script_data):
        print("🚀 ELITE CONTENT PIPELINE STARTED")
        audio_path = self.generate_elite_audio(script_data["script_ru"])
        print(f"✅ Audio Ready: {audio_path}")
        print("✅ Pipeline Initial Stage Complete. Moving to Visuals...")


if __name__ == "__main__":
    orch = EliteContentOrchestrator()
    import time

    orch = EliteContentOrchestrator()
    print("✅ Orchestrator Initialized. Entering Daemon Mode...")
    
    while True:
        # pending_tasks = check_queue() # Future: Check Redis/Queue
        print("💤 Waiting for new content tasks...")
        time.sleep(60)
        # For testing, we can trigger manually or via API

