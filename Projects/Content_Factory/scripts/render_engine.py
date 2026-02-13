import os
import re

from moviepy import *

# Config
REPORT_FILE = "/home/gonya/Unified_System_Core/Projects/Content_Factory/reports/series_plan_v1.md"
OUTPUT_DIR = "/home/gonya/Unified_System_Core/Projects/Content_Factory/output/nightly_build"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Fallback, might need to check


def parse_markdown_plan(file_path):
    episodes = []
    current_ep = {}

    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("## 📺 Episode"):
                if current_ep:
                    episodes.append(current_ep)
                current_ep = {"title": line.split(":", 1)[1].strip()}
            elif line.startswith("**Hook:**") and current_ep:
                current_ep["hook"] = line.split("**Hook:**")[1].strip()

    if current_ep:
        episodes.append(current_ep)
    return episodes


def create_video(episode):
    print(f"🎬 Rendering: {episode['title']}")

    # Create simple clips
    # 1. Title Screen (Black bg, White Text)
    # Note: TextClip in MoviePy 2.x often needs ImageMagick.
    # If ImageMagick is tricky, we can use ColorClip.
    # Let's try simple ColorClip first to ensure file creation works.

    try:
        # Background
        clip = ColorClip(size=(720, 1280), color=(0, 0, 50), duration=5)  # 9:16 Vertical video

        # We will try to add text, but catch error if ImageMagick missing
        try:
            txt_clip = TextClip(
                font=FONT_PATH, text=episode["title"], font_size=50, color="white", size=(700, 1280), method="caption"
            )
            txt_clip = txt_clip.with_position("center").with_duration(5)
            video = CompositeVideoClip([clip, txt_clip])
        except Exception as e:
            print(f"⚠️ Text rendering failed ({e}), finding workaround...")
            # Fallback: Just color clip with different colors
            video = clip

    except Exception as e:
        print(f"❌ Video creation error: {e}")
        return

    # Output filename
    safe_title = re.sub(r"[^a-zA-Z0-9]", "_", episode["title"])
    filename = os.path.join(OUTPUT_DIR, f"EP_{safe_title}.mp4")

    video.write_videofile(filename, fps=24, codec="libx264")
    print(f"✅ Saved to: {filename}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    episodes = parse_markdown_plan(REPORT_FILE)

    print(f"Found {len(episodes)} episodes to render.")

    for ep in episodes:
        create_video(ep)


if __name__ == "__main__":
    main()
