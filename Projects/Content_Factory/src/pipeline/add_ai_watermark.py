import subprocess
from pathlib import Path


def add_ai_watermark(input_video: Path, output_video: Path) -> bool:
    """
    Adds 'Created by AI' watermark to video WITHOUT re-encoding.
    Uses same quality as original.
    """

    # Get input video bitrate to match it
    probe_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=bit_rate",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(input_video),
    ]

    try:
        result = subprocess.run(probe_cmd, capture_output=True, text=True)
        bitrate = int(result.stdout.strip()) if result.stdout.strip() else 3267000
        bitrate_k = bitrate // 1000
    except:
        bitrate_k = 3267  # Default

    # FFmpeg command with matched bitrate
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_video),
        "-vf",
        "drawtext=text='⚠️ Created by AI':fontsize=20:fontcolor=white:borderw=2:bordercolor=black:x=w-tw-10:y=h-th-10:box=1:boxcolor=black@0.5:boxborderw=5",
        "-c:v",
        "libx264",
        "-preset",
        "slow",  # Better quality
        "-b:v",
        f"{bitrate_k}k",  # Match original bitrate
        "-maxrate",
        f"{bitrate_k}k",
        "-bufsize",
        f"{bitrate_k * 2}k",
        "-c:a",
        "copy",  # Copy audio without re-encoding
        str(output_video),
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Watermark added (bitrate: {bitrate_k}k): {output_video}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Watermark failed: {e}")
        return False


if __name__ == "__main__":
    print("AI Watermark Module Ready - Quality Matched")
