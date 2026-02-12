
import json
import logging
import sys
import time
from pathlib import Path

# Paths
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent.parent.parent.parent
# /Users/igorgoncharenko/Documents/Unified_System_Core
# Use absolute path for reliability
AI_CORE_SRC_PATH = "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/AI_Core/src"
if AI_CORE_SRC_PATH not in sys.path:
    sys.path.append(AI_CORE_SRC_PATH)

import openai
from token_broker import TokenBroker

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SoraGenerator")

CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
VIDEO_CLIPS_DIR = CONTEXT_DIR / "video_clips"
SCRIPTS_DIR = CONTEXT_DIR / "scripts"

class SoraVideoGenerator:
    """
    Generates realistic video clips using OpenAI Sora-2.
    Replaces static 'zooming' images with actual character motion.
    """
    def __init__(self):
        self.broker = TokenBroker()
        self.api_key = self.broker.get_key("openai")
        self.client = openai.OpenAI(api_key=self.api_key)

    def generate_video(self, segment_id, prompt, role, angle):
        print(f"🎬 [SORA-2] Generating motion for segment {segment_id} ({role})...")
        print(f"   Prompt: {prompt}")

        try:
            # Using the sora-2 model as seen in model list
            # Note: API syntax based on 2025/2026 specs for Sora-2
            response = self.client.video.generations.create(
                model="sora-2",
                prompt=f"A cinematic {angle} shot of a {role} dinosaur in a podcast studio. {prompt}. High fidelity, 4k.",
                duration=5,
                aspect_ratio="16:9"
            )

            job_id = response.id
            print(f"   🚀 Job created: {job_id}. Polling for completion...")

            while True:
                job = self.client.video.generations.retrieve(job_id)
                if job.status == "completed":
                    video_url = job.video.url
                    print(f"   ✅ Video ready: {video_url}")
                    return video_url
                elif job.status == "failed":
                    print(f"   ❌ Sora job failed: {job.error}")
                    return None
                time.sleep(5)

        except Exception as e:
            print(f"   ❌ Sora API Error: {e}")
            return None

    def process_script(self, script_path):
        with open(script_path) as f:
            data = json.loads(f.read())

        segments = data.get("segments", [])
        for i, seg in enumerate(segments):
            # Only generate if motion_prompt exists and we don't have it yet
            motion_prompt = seg.get("motion_prompt")
            if not motion_prompt:
                continue

            output_name = f"sora_{Path(script_path).stem}_{i}.mp4"
            output_path = VIDEO_CLIPS_DIR / output_name

            if output_path.exists():
                print(f"   ⏭️ Skipping existing clip: {output_name}")
                continue

            video_url = self.generate_video(i, motion_prompt, seg['role'], seg['angle'])
            if video_url:
                # Download (pseudo-code for brevity, would use requests)
                import requests
                r = requests.get(video_url)
                with open(output_path, "wb") as f:
                    f.write(r.content)
                print(f"   💾 Saved to: {output_path}")

if __name__ == "__main__":
    generator = SoraVideoGenerator()
    latest_script = SCRIPTS_DIR / "ai_future_2026_directed.json"
    if latest_script.exists():
        generator.process_script(latest_script)
    else:
        print("❌ Latest script not found.")
