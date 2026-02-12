import json
import random
import re
from pathlib import Path

from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

# Paths
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path("/Users/igorgoncharenko/Documents/Unified_System_Core")
CONTEXT_DIR = PROJECT_ROOT / "Context"
AUDIO_DIR = CONTEXT_DIR / "audio_output"
VIDEO_CLIPS_DIR = CONTEXT_DIR / "video_clips"
FINAL_VIDEO_DIR = CONTEXT_DIR / "final_videos"
SCRIPTS_DIR = CONTEXT_DIR / "scripts"

if not FINAL_VIDEO_DIR.exists():
    FINAL_VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def parse_script(lines):
    """Parse dialogue script (JSON or text)."""
    content = "".join(lines)
    json_match = re.search(r"```json\s*([\s\S]*?)\s*```", content)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    try:
        data = json.loads(content)
        if isinstance(data, dict) and "segments" in data:
            return data["segments"]
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    script_data = []
    for line in lines:
        text = line.strip()
        if not text:
            continue
        role = "Unknown"
        if any(k in text for k in ["Skeptic", "Host 1", "Rex"]):
            role = "Skeptic"
            text = re.sub(r"^(Host 1|Skeptic|Rex|T-Rex):", "", text).strip()
        elif any(k in text for k in ["Enthusiast", "Host 2", "Trike"]):
            role = "Enthusiast"
            text = re.sub(r"^(Host 2|Enthusiast|Trike|Triceratops):", "", text).strip()
        if text:
            script_data.append({"role": role, "text": text})
    return script_data

def assemble_directed_video(script_file):
    """Assemble final video from segments."""
    print(f"🎬 [DIRECTOR'S CUT] Assembling: {script_file.name}...")

    with open(script_file) as f:
        lines = f.readlines()
    script_data = parse_script(lines)

    clips = []

    # Load all available directed clips
    angle_pool = {
        "Skeptic": {
            "wide": str(VIDEO_CLIPS_DIR / "rex_wide.mp4"),
            "medium": str(VIDEO_CLIPS_DIR / "rex_medium.mp4"),
            "close": str(VIDEO_CLIPS_DIR / "rex_close.mp4")
        },
        "Enthusiast": {
            "wide": str(VIDEO_CLIPS_DIR / "trike_wide.mp4"),
            "medium": str(VIDEO_CLIPS_DIR / "trike_medium.mp4"),
            "close": str(VIDEO_CLIPS_DIR / "trike_close.mp4")
        }
    }

    broll_clips = list(VIDEO_CLIPS_DIR.glob("broll_*_motion.mp4"))
    random.shuffle(broll_clips)

    # Assembly Logic: Cycle angles and insert B-roll
    shot_sequence = ["wide", "medium", "close", "medium"]

    for i, line in enumerate(script_data):
        role = line.get("role", "Unknown")
        audio_path = AUDIO_DIR / f"segment_{i}_{role}.wav"

        if not audio_path.exists():
            print(f"⚠️ Missing audio: {audio_path}")
            continue

        audio_clip = AudioFileClip(str(audio_path))
        duration = audio_clip.duration

        # Mapping role to key
        actor_key = "Skeptic" if role == "Skeptic" or "Rex" in role else "Enthusiast"

        if i > 0 and i % 4 == 0 and broll_clips:
            broll_path = broll_clips[i % len(broll_clips)]
            print(f"   🎥 Cut to B-Roll: {broll_path.name}")
            video_source = VideoFileClip(str(broll_path))
        else:
            # Use directed angle if available
            angle = line.get("angle", shot_sequence[i % len(shot_sequence)])
            print(f"   🎥 Shot: {actor_key} ({angle})")
            video_source = VideoFileClip(angle_pool[actor_key][angle])

        # Loop/Subclip to match audio
        segment = video_source.loop(duration=duration)
        segment = segment.set_audio(audio_clip)
        clips.append(segment)

    if clips:
        final_video = concatenate_videoclips(clips, method="compose")
        output_prefix = "directed_" if "premium" not in script_file.name else ""
        output_path = FINAL_VIDEO_DIR / f"{output_prefix}{script_file.stem}_premium.mp4"

        final_video.write_videofile(
            str(output_path),
            fps=24,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        print(f"✅ Directed Premium Video saved: {output_path.name}")
    else:
        print("❌ Assembly failed: No clips.")

if __name__ == "__main__":
    valid_patterns = ["*_script.md", "*.json"]
    script_files = []
    for pattern in valid_patterns:
        script_files.extend(SCRIPTS_DIR.glob(pattern))

    for sf in script_files:
        assemble_directed_video(sf)
