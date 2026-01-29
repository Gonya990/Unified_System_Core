#!/usr/bin/env python3
"""
PyCaps Subtitle Generator for Content Farm
Adds dynamic word-by-word subtitles to videos
"""

import subprocess
from pathlib import Path


def add_subtitles(video_path: str, output_path: str, text: str):
    """
    Add dynamic subtitles to video using PyCaps CLI

    Args:
        video_path: Path to input video
        output_path: Path to output video with subtitles
        text: Text to display as subtitles (will be transcribed if not provided)
    """
    print(f"📝 Adding subtitles to: {video_path}")

    # PyCaps command
    # pycaps <video> -o <output> --style hormozi
    cmd = [
        "pycaps",
        str(video_path),
        "-o", str(output_path),
        "--style", "hormozi",  # Dynamic word-by-word style
        "--font-size", "60",
        "--stroke-width", "3"
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"✅ Subtitles added: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Subtitle generation failed: {e}")
        return False
    except FileNotFoundError:
        print("❌ Error: 'pycaps' command not found")
        return False

if __name__ == "__main__":
    import sys

    ROOT_DIR = Path(__file__).parent.resolve()
    OUTPUT_DIR = ROOT_DIR / "outputs"

    # Default: Add subtitles to lip-synced video
    input_video = OUTPUT_DIR / "igor_lipsync.mp4"
    output_video = OUTPUT_DIR / "igor_final_subtitled.mp4"

    if len(sys.argv) >= 3:
        input_video = Path(sys.argv[1])
        output_video = Path(sys.argv[2])

    add_subtitles(input_video, output_video, "")
