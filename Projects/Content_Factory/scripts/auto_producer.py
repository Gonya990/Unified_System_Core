import json
import logging
import os
import time

import requests

# Config
LLM_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"
OUTPUT_DIR = "/home/gonya/Unified_System_Core/Projects/Content_Factory/output/nightly_build"
SCENARIO_FILE = os.path.join(OUTPUT_DIR, "production_plan.json")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def check_system_load():
    """Wait until 1-minute load average is below 2.0 (indicating rsync is likely done or CPU is free)."""
    while True:
        load1, load5, load15 = os.getloadavg()
        logging.info(f"Current Load: {load1:.2f} (Waiting for < 2.0)")
        if load1 < 2.0:
            logging.info("✅ Load is low. System ready.")
            return
        time.sleep(300)  # Check every 5 minutes


def generate_scenario_json():
    """Generate the scenario content using LLM with retry."""
    prompt = """
    Create a JSON content plan for 3 short video episodes (TikTok/Reels style, 60s each).
    Format must be valid JSON:
    [
        {
            "episode": 1,
            "title": "My AI Took Over Telegram",
            "script": "Voiceover: I gave my Telegram to AI... Visual: Terminal scrolling...",
            "keywords": ["AI", "Telegram", "Automation"]
        },
        ...
    ]
    Based on the theme: 'Building a Cyberpunk Digital Life from Archives'.
    """

    retries = 10
    while retries > 0:
        try:
            logging.info("🧠 Requesting Scenario from Llama...")
            response = requests.post(
                LLM_URL, json={"model": MODEL, "prompt": prompt, "stream": false, "format": "json"}, timeout=120
            )
            if response.status_code == 200:
                data = response.json()
                content = data.get("response", "")
                # Parse JSON
                plan = json.loads(content)
                return plan
        except Exception as e:
            logging.error(f"⚠️ LLM Error: {e}. Retrying in 60s...")
            time.sleep(60)
            retries -= 1
    return None


def mock_render_video(episode):
    """Simulate video rendering (since we don't have the full video engine linked yet)."""
    filename = f"Episode_{episode['episode']}_{episode['title'].replace(' ', '_')}.mp4"
    filepath = os.path.join(OUTPUT_DIR, filename)

    logging.info(f"🎬 Rendering {filename}...")
    time.sleep(5)  # Simulate work

    # Create a dummy video file or text file for now if moviepy fails/is complex headers
    with open(filepath, "w") as f:
        f.write(f"VIDEO DATA FOR: {episode['title']}\nSCRIPT: {episode['script']}")

    logging.info(f"✅ Rendered: {filepath}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logging.info("🌙 Nightly Producer Initialized.")
    check_system_load()

    plan = generate_scenario_json()
    if not plan:
        logging.error("❌ Failed to generate plan after retries.")
        # Fallback plan
        plan = [{"episode": 1, "title": "System_Boot_Sequence", "script": "Hello World", "keywords": []}]

    # Save Plan
    with open(SCENARIO_FILE, "w") as f:
        json.dump(plan, f, indent=2)

    # Render
    for ep in plan:
        mock_render_video(ep)

    logging.info("💤 Production complete. Going to sleep.")


if __name__ == "__main__":
    main()
