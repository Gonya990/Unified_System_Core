import json
import re
from pathlib import Path

from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

# Пути
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


def assemble_video(script_file):
    """Assemble final video from segments."""
    print(f"🎬 Сборка Премиум Видео для: {script_file.name}...")

    with open(script_file) as f:
        lines = f.readlines()
    script_data = parse_script(lines)

    clips = []

    # Загрузка видеоциклов
    loops = {}
    try:
        loops["Skeptic"] = VideoFileClip(str(VIDEO_CLIPS_DIR / "rex_motion.mp4"))
        loops["Enthusiast"] = VideoFileClip(str(VIDEO_CLIPS_DIR / "trike_motion.mp4"))
    except Exception as e:
        print(f"❌ Не удалось загрузить видеоциклы: {e}")
        return

    for i, line in enumerate(script_data):
        role = line.get("role", "Unknown")

        # Аудиосегмент
        audio_path = AUDIO_DIR / f"segment_{i}_{role}.wav"
        if not audio_path.exists():
            print(f"⚠️ Аудиосегмент отсутствует для строки {i}: {audio_path}")
            continue

        audio_clip = AudioFileClip(str(audio_path))
        duration = audio_clip.duration

        # Выбор видеоцикла
        loop_key = "Skeptic" if role == "Skeptic" or "Rex" in role else "Enthusiast"
        video_loop = loops.get(loop_key)

        if video_loop:
            # Зацикливание видео под длительность аудио
            video_segment = video_loop.loop(duration=duration)
            video_segment = video_segment.set_audio(audio_clip)
            clips.append(video_segment)
        else:
            print(f"⚠️ Нет видеоцикла для роли {role}")

    if clips:
        final_video = concatenate_videoclips(clips, method="compose")
        output_path = FINAL_VIDEO_DIR / f"{script_file.stem}_premium.mp4"
        final_video.write_videofile(str(output_path), fps=24, codec="libx264", audio_codec="aac")
        print(f"✅ Премиум Видео сохранено: {output_path.name}")
    else:
        print("❌ Клипы не собраны.")


if __name__ == "__main__":
    script_files = list(SCRIPTS_DIR.glob("*_script.md"))
    for sf in script_files:
        assemble_video(sf)
