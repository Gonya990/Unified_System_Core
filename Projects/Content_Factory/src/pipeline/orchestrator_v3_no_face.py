#!/usr/bin/env python3
"""
Content Farm Orchestrator v3 - NO FACE
Complete pipeline: Text -> Voice -> B-Roll -> Subtitles
Supports Russian and English voices
"""

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

# Setup paths
SRC_DIR = Path(__file__).parent.parent.resolve() # Projects/Content_Factory/src
FACTORY_DIR = SRC_DIR.parent  # Projects/Content_Factory
PROJECTS_DIR = FACTORY_DIR.parent # /Projects
ROOT_DIR = PROJECTS_DIR.parent # Unified_System (Root)

# Add all source subdirectories to path
for d in ["researcher", "pipeline", "assets", "video", "uploaders"]:
    sys.path.append(str(SRC_DIR / d))

# Add Scripts/Utilities to path for TokenBroker
sys.path.append(str(ROOT_DIR / "Scripts/Utilities"))

def agent_mindfulness(task: str):
    """Reflecting user request: strategic pauses & token availability checks"""
    print(f"🕵️ Vibranium Agent checking {task} (Pausing for stability)...")
    time.sleep(2.5)

# Load TokenBroker
try:
    from token_broker import TokenBroker
    broker = TokenBroker()
except ImportError:
    print("⚠️ TokenBroker not found. Falling back to environment variables.")
    broker = None

# Load API keys from potential locations
load_dotenv(ROOT_DIR / ".env", override=True)
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)

# Masked key debug
openai_key = os.getenv("OPENAI_API_KEY", "")
pexels_key = os.getenv("PEXELS_API_KEY", "")
masked_openai = f"{openai_key[:8]}...{openai_key[-4:]}" if openai_key else "None"
print(f"📡 API Status: OpenAI={masked_openai} Pexels={pexels_key[:8]}...")

# Import internal tools
try:
    from pexels_broll import semantic_search_broll  # noqa: F401
    from video_assembler import create_video_with_broll, get_video_duration  # noqa: F401
except ImportError:
    print("⚠️ Internal tools not found. Script might fail.")

OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR_OVERRIDE", str(ROOT_DIR / "outputs")))
INPUT_DIR = Path(os.getenv("INPUT_DIR_OVERRIDE", str(ROOT_DIR / "inputs")))
BROLL_DIR = Path(os.getenv("BROLL_DIR_OVERRIDE", str(ROOT_DIR / "broll")))

OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
INPUT_DIR.mkdir(exist_ok=True, parents=True)
BROLL_DIR.mkdir(exist_ok=True, parents=True)

import random

# Voice options (OpenAI TTS preferred, Edge-TTS fallback)
VOICES = {
    "en": "alloy",        # Neutral, clear (No accent/burring)
    "en_female": "shimmer",
    "ru": "alloy",        # Neutral, professional
    "ru_female": "shimmer",
    "he": "alloy",        # Neutral (Best for Hebrew without heavy accent)
    "he_female": "shimmer",
    "fallback_ru": "ru-RU-DmitryNeural",
    "fallback_en": "en-US-EmmaNeural",
    "fallback_he": "he-IL-AvriNeural" # Edge-TTS Hebrew
}

def generate_audio_openai(text: str, output_path: Path, voice: str) -> bool:
    """Generate audio using OpenAI TTS with Studio Post-Processing"""
    print(f"🎙 Generating Studio-Quality OpenAI Audio (voice={voice})...")

    api_key = (broker.get_key("openai") if broker else None) or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found via TokenBroker or Environment.")
        return False

    # Masked key debug
    masked_key = f"{api_key[:8]}...{api_key[-4:]}"
    print(f"🔑 Using API Key: {masked_key}")

    try:
        from openai import OpenAI
        base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        org_id = os.getenv("OPENAI_ORG_ID")

        client = OpenAI(api_key=api_key, base_url=base_url, organization=org_id)

        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text
        )

        mp3_path = output_path.with_suffix(".mp3")
        response.stream_to_file(str(mp3_path))

        # STUDIO POST-PROCESSING
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3_path),
            "-af", "bass=g=4:f=100,treble=g=2:f=8000,acompressor=threshold=-12dB:ratio=3:attack=5:release=50,loudnorm",
            "-ar", "44100", "-ac", "2", "-b:a", "192k", str(output_path)
        ], check=True, capture_output=True)

        print(f"✅ Studio Audio Mastered: {output_path}")
        return True
    except Exception as e:
        print(f"❌ OpenAI TTS failed: {e}")
        return False

def generate_audio_edge(text: str, output_path: Path, voice: str) -> bool:
    """Generate audio using Edge-TTS with rate control"""
    agent_mindfulness("Edge-TTS Audio Generation")
    print(f"🎤 Generating Enhanced Edge-TTS Audio (voice={voice})...")

    mp3_path = output_path.with_suffix(".mp3")
    edge_tts_cmd = "edge-tts"

    # Search paths for edge-tts binary
    search_paths = [
        FACTORY_DIR / "venv/bin/edge-tts",
        ROOT_DIR / "venv_content/bin/edge-tts",
        ROOT_DIR.parent.parent / "venv/bin/edge-tts"
    ]

    for p in search_paths:
        if p.exists():
            edge_tts_cmd = str(p)
            break
    else:
        # Fallback to which
        import shutil
        found = shutil.which("edge-tts")
        if found: edge_tts_cmd = found

    # FIX: Pass --rate as a single argument string or ensure it's correctly handled
    cmd = [
        edge_tts_cmd,
        "--text", text,
        "--write-media", str(mp3_path),
        "--voice", voice,
        "--rate=-10%"
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        # Convert to WAV
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3_path),
            "-ar", "44100", "-ac", "2", str(output_path)
        ], check=True, capture_output=True)
        print(f"✅ Enhanced Fallback Audio: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Edge-TTS command failed: {e.stderr.decode() if e.stderr else e}")
        return False
    except Exception as e:
        print(f"❌ Edge-TTS general error: {e}")
        return False

def transcribe_audio_gemini(audio_path: Path) -> list[dict]:
    """Fallback: Transcription using Gemini 1.5 Flash (Vibranium Resilience)"""
    print("🌠 Falling back to Gemini for transcription...")
    api_key = (broker.get_key("gemini") if broker else None) or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Gemini Transcription failed: No API Key found.")
        return []

    print(f"🔑 Using Gemini Key: {api_key[:8]}... (len={len(api_key)})")
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.0-flash")

        with open(audio_path, "rb") as f:
            audio_data = f.read()

        prompt = "Transcribe this audio. Return ONLY a JSON list of words with start and end timestamps in seconds: [{\"word\": \"text\", \"start\": 0.0, \"end\": 0.5}, ...]. Do not include markdown formatting, just raw JSON."

        # Structure payload correctly for Gemini
        response = model.generate_content([
            prompt,
            {"mime_type": "audio/wav", "data": audio_data}
        ])

        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        # Final cleanup for raw JSON
        if not text.startswith("["):
            # Try to find the first [ and last ]
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end != 0:
                text = text[start:end]

        words = json.loads(text)
        print(f"✅ Gemini Transcription successful: {len(words)} words found.")
        return words
    except Exception as e:
        print(f"❌ Gemini Transcription failed: {e}")
        return []

def transcribe_audio_whisper(audio_path: Path) -> list[dict]:
    """Get word-level timestamps using OpenAI Whisper API with Gemini Fallback"""
    # Rate limit protection
    time.sleep(1.5)

    print("🧠 Transcribing audio for word-level subtitles...")
    api_key = (broker.get_key("openai") if broker else None) or os.getenv("OPENAI_API_KEY")

    # 1. Main Strategy: OpenAI Whisper
    if api_key:
        temp_mp3 = audio_path.with_suffix(".mp3")
        try:
            subprocess.run([
                "ffmpeg", "-y", "-i", str(audio_path),
                "-b:a", "128k", str(temp_mp3)
            ], check=True, capture_output=True)

            from openai import OpenAI
            base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            org_id = os.getenv("OPENAI_ORG_ID")
            client = OpenAI(api_key=api_key, base_url=base_url, organization=org_id)

            with open(temp_mp3, "rb") as f:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=f,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )

            if temp_mp3.exists(): temp_mp3.unlink()
            words = transcript.words if hasattr(transcript, 'words') else []
            if words: return words
        except Exception as e:
            print(f"⚠️ OpenAI Whisper failed: {e}")
            if temp_mp3.exists(): temp_mp3.unlink()

    # 2. Strategy 2: Gemini Fallback
    return transcribe_audio_gemini(audio_path)

def generate_audio(text: str, output_path: Path, lang: str = "en") -> bool:
    """Main audio generation with premium support and fallback"""
    time.sleep(1.0) # Tactical pause
    voice = VOICES.get(lang, VOICES["en"])

    # Special case for Hebrew with Onyx (it works well for deep voice)
    if lang == "he":
        voice = VOICES["en"] # Use Onyx (multilingual model) for Hebrew

    # 1. Try OpenAI (Premium)
    if generate_audio_openai(text, output_path, voice):
        return True

    # 2. Fallback to Edge-TTS
    print("⚠️ OpenAI Failed, falling back to Edge-TTS...")
    fallback_voice = VOICES.get(f"fallback_{lang}", "en-US-EmmaNeural")
    return generate_audio_edge(text, output_path, fallback_voice)

def add_subtitles(video_path: Path, output_path: Path, lang: str = "ru", style: str = "impact") -> bool:
    """Add dynamic word-by-word subtitles matching style"""
    style_label = "Impact Vision" if style == "impact" else "Cartoon Fun"
    print(f"📝 Burning '{style_label}' Style Subtitles...")

    # 1. Extract audio and transcribe
    temp_audio = output_path.parent / f"temp_{output_path.stem}_sub.wav"
    subprocess.run(["ffmpeg", "-y", "-i", str(video_path), "-vn", "-ac", "1", str(temp_audio)], check=True, capture_output=True)

    words = transcribe_audio_whisper(temp_audio)
    if not words:
        print("⚠️ No words found for subtitles.")
        return False

    # 2. Build drawtext filters
    # Motivaider: High contrast, centered, Gold/White
    filters = []
    font_path = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
    if not Path(font_path).exists(): font_path = "Arial"

    for _i, w in enumerate(words):
        # Handle both dict and object (OpenAI SDK returns objects)
        start = w.start if hasattr(w, 'start') else w.get('start', 0)
        end = w.end if hasattr(w, 'end') else w.get('end', 0)
        text = w.word if hasattr(w, 'word') else w.get('word', "")

        text = text.upper().replace("'", "").replace(":", "").replace("\"", "").replace("\\", "")

        if style == "impact":
            # Color: Golden Yellow (0xFFD700)
            f = (f"drawtext=fontfile='{font_path}':text='{text}':fontcolor=0xFFD700:fontsize=80:"
                 f"x=(w-text_w)/2:y=h-(h*0.2):borderw=4:bordercolor=black:"
                 f"enable='between(t,{start},{end})'")
        else:
            # Cartoon Style: Vibrant Pink/Cyan with white border, bigger and slightly higher
            color = random.choice(["0xFF69B4", "0x00FFFF", "0xFFFF00"]) # Pink, Cyan, Yellow
            f = (f"drawtext=fontfile='{font_path}':text='{text}':fontcolor={color}:fontsize=100:"
                 f"x=(w-text_w)/2:y=h-(h*0.3):borderw=6:bordercolor=white:"
                 f"enable='between(t,{start},{end})'")
        filters.append(f)

    filter_str = ",".join(filters)

    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_path),
            "-vf", filter_str,
            "-c:a", "copy", str(output_path)
        ], check=True, capture_output=True)
        print(f"✨ Impact Vision Masterpiece Finalized: {output_path}")
        temp_audio.unlink()
        return True
    except Exception as e:
        print(f"❌ Subtitle burning failed: {e}")
        return False

def assemble_broll_only_video(audio_path: Path, clips: list[Path], output_path: Path):
    """
    Create a video containing ONLY B-Roll clips, matched to audio length
    """
    print("🎬 Assembling B-Roll only video...")

    # 1. Get total audio duration
    audio_duration = float(subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ], capture_output=True, text=True).stdout.strip())

    print(f"⏱ Audio duration: {audio_duration}s")

    # 2. Prepare clips to fill the duration
    final_clips = []
    current_time = 0
    clip_idx = 0

    while current_time < audio_duration and clips:
        clip = clips[clip_idx % len(clips)]
        clip_duration = get_video_duration(clip)

        # If last clip, trim it to match remaining audio time
        remaining = audio_duration - current_time
        target_duration = min(clip_duration, remaining)

        trimmed_path = output_path.parent / f"temp_{output_path.stem}_clip_{len(final_clips)}.mp4"
        subprocess.run([
            "ffmpeg", "-y", "-i", str(clip),
            "-t", str(target_duration),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920", # Vertical format
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            str(trimmed_path)
        ], check=True, capture_output=True)

        final_clips.append(trimmed_path)
        current_time += target_duration
        clip_idx += 1

    # 3. Concatenate clips
    concat_list = output_path.parent / f"temp_{output_path.stem}_concat.txt"
    with open(concat_list, "w") as f:
        for clip in final_clips:
            f.write(f"file '{clip.name}'\n")

    video_no_audio = output_path.parent / f"temp_{output_path.stem}_no_audio.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(video_no_audio)
    ], check=True, capture_output=True, cwd=str(output_path.parent))

    # 4. Merge with audio
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_no_audio), "-i", str(audio_path),
        "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0",
        str(output_path)
    ], check=True, capture_output=True)

    # Cleanup
    for clip in final_clips: clip.unlink()
    video_no_audio.unlink()
    concat_list.unlink()

    print(f"✅ Video assembled: {output_path}")

# FORCE CORRECT API KEY (bypassing potentially bad environment)
    # API Setup (loaded from .env)

def assemble_hybrid_video(audio_path: Path, scenes: list[dict], output_path: Path, style: str = "impact"):
    """
    Create a CINEMATIC or CARTOON high-energy video.
    """
    kind = "CINEMATIC MASTERPIECE" if style == "impact" else "CARTOON ADVENTURE"
    print(f"🎬 Producing {kind}...")

    audio_duration = float(subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ], capture_output=True, text=True).stdout.strip())

    num_scenes = len(scenes)
    # Calculate duration per scene to exactly cover audio duration
    if num_scenes > 0:
        duration_per_scene = audio_duration / num_scenes
    else:
        duration_per_scene = 5.0 # Fallback

    print(f"⏱️ Exact Scene Duration: {duration_per_scene:.2f}s (Total: {audio_duration:.2f}s)")

    segments = []

    # Generate unique prefix based on output filename to prevent collisions in parallel runs
    unique_prefix = output_path.stem

    for i, scene in enumerate(scenes):
        agent_mindfulness(f"Assembling Scene {i}")

        # 🧪 Robust Image Path Resolution (Vibranium Standard)
        img_path = scene.get('resolved_path') or scene.get('image')
        if img_path and not os.path.isabs(img_path):
            # Try with various extensions in INPUT_DIR
            potential_path = INPUT_DIR / img_path
            if not potential_path.exists():
                for ext in [".jpg", ".png", ".webp", ".jpeg"]:
                    if (INPUT_DIR / f"{img_path}{ext}").exists():
                        potential_path = INPUT_DIR / f"{img_path}{ext}"
                        break
            img_path = str(potential_path)

        keyword = scene.get('keyword', 'abstract technology')

        # Timing: 80% B-Roll, 20% Image Flash
        broll_dur = duration_per_scene * 0.8
        img_dur = duration_per_scene * 0.2

        # Get more clips to ensure we cover the duration
        broll_clips = semantic_search_broll(keyword, BROLL_DIR, num_clips=5)

        # 1. B-Roll Sequence (2-3 clips per scene for fast rhythm)
        if broll_clips:
            # We need to cover broll_dur. If clips are too short, we loop or use multiple.
            accumulated_broll = 0
            clip_idx = 0
            while accumulated_broll < broll_dur:
                clip = broll_clips[clip_idx % len(broll_clips)]
                clip_idx += 1

                remaining = broll_dur - accumulated_broll
                this_clip_dur = min(get_video_duration(clip), remaining)
                # If clip is extremely short (<1s), skip to avoid ffmpeg errors
                if this_clip_dur < 0.5: break

                seg_p = output_path.parent / f"{unique_prefix}_seg_{i}_b{clip_idx}.mp4"
                if style == "impact":
                    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.1:saturation=1.3,vignette=angle=0.3"
                else:
                    vf = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=saturation=1.5"

                subprocess.run([
                    "ffmpeg", "-y", "-i", str(clip),
                    "-t", str(this_clip_dur),
                    "-vf", vf,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(seg_p)
                ], check=True, capture_output=True)
                segments.append(seg_p)
                accumulated_broll += this_clip_dur
        else:
            img_dur += broll_dur

        # 2. Visionary AI Image Flash (STABLE ROBUST MOTION)
        seg_p_img = output_path.parent / f"{unique_prefix}_seg_{i}_img.mp4"
        if style == "impact":
            vf_img = "scale=w=1080:h=1920:force_original_aspect_ratio=increase,crop=1080:1920,fade=in:0:5:color=white,vignette=angle=0.5"
        else:
            vf_img = "scale=w=1080:h=1920:force_original_aspect_ratio=increase,crop=1080:1920,fade=in:0:5:color=pink"

        subprocess.run([
            "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
            "-t", str(img_dur),
            "-vf", vf_img,
            "-pix_fmt", "yuv420p", "-c:v", "libx264", "-r", "30", str(seg_p_img)
        ], check=True, capture_output=True)
        segments.append(seg_p_img)

    # Concat visuals
    concat_file = output_path.parent / f"{unique_prefix}_concat.txt"
    with open(concat_file, "w") as f:
        for seg in segments: f.write(f"file '{seg.name}'\n")

    raw_visuals = output_path.parent / f"temp_{unique_prefix}_visuals.mp4"
    try:
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
            "-c", "copy", str(raw_visuals)
        ], check=True, capture_output=True, cwd=str(output_path.parent))
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Concat Error: {e.stderr.decode()}")
        raise

    # 3. PRO AUDIO ENGINE: Compression + Reverb
    print("🔊 Mixing professional audio suite...")
    final_audio = output_path.parent / f"temp_{unique_prefix}_audio.wav"

    if style == "impact":
        # Ultra-clean audio with minimal reverb for heavy documentaries
        audio_filter = (
            "acompressor=threshold=-15dB:ratio=4:attack=5:release=50,"
            "aecho=0.8:0.3:20:0.1,"
            "loudnorm"
        )
    else:
        audio_filter = "acompressor=threshold=-12dB:ratio=3:attack=5:release=50,loudnorm"

    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(audio_path),
            "-af", audio_filter,
            str(final_audio)
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Audio Error: {e.stderr.decode()}")
        raise

    # 4. Final Final Merge
    try:
        subprocess.run([
            "ffmpeg", "-y", "-i", str(raw_visuals), "-i", str(final_audio),
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", "-shortest",
            str(output_path)
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg Merge Error: {e.stderr.decode()}")
        raise

    # Cleanup
    for seg in segments:
        if seg.exists(): seg.unlink()
    if raw_visuals.exists(): raw_visuals.unlink()
    if final_audio.exists(): final_audio.unlink()
    if concat_file.exists(): concat_file.unlink()
    return True

def run_no_face_pipeline(text: str, lang: str = "ru", output_name: str = "no_face_video", scenes: list[dict] = None, style: str = "impact"):
    """Run pipeline without face usage"""
    print(f"\n🚀 Starting ENHANCED NO-FACE Pipeline (lang={lang}, style={style})")

    # 1. Audio
    audio_path = INPUT_DIR / f"{output_name}_audio.wav"
    if not generate_audio(text, audio_path, lang):
        return None

    # 2. Visuals
    final_video = OUTPUT_DIR / f"{output_name}_final.mp4"
    raw_video = OUTPUT_DIR / f"{output_name}_raw.mp4"

    if scenes:
        assemble_hybrid_video(audio_path, scenes, raw_video, style=style)
    else:
        # Fallback to simple B-Roll logic if no scenes provided
        clips = semantic_search_broll(text, BROLL_DIR, num_clips=5)
        if clips:
            assemble_broll_only_video(audio_path, clips, raw_video)
        else:
            print("❌ No visual assets found.")
            return None

    # 3. Subtitles
    if not add_subtitles(raw_video, final_video, lang, style=style):
        print("⚠️ Subtitles failed, using raw video.")
        if final_video.exists(): final_video.unlink()
        raw_video.rename(final_video)

    print(f"\n✨ DONE: {final_video}")
    return final_video

if __name__ == "__main__":
    # Council-Generated 15-Scene Script (Refined for Natural TTS & Pronunciation)
    script_ru = (
        "Добро пожаловать в две тысячи двадцать шестой год. Мир, где искусственный интеллект стал частью нашей реальности... навсегда изменив экономику и общество. "
        "Пятнадцать триллионов долларов. Именно столько искусственный интеллект привнес в мировую экономику... став главным двигателем прогресса. "
        "Девяносто процентов контента, который мы видим каждый день... теперь создается алгоритмами. От новостей... до кино и музыки. "
        "Задачи, которые раньше требовали десятилетий... сегодня решаются за считанные недели. Это открывает перед человечеством новые... невероятные горизонты. "
        "Мы наблюдаем настоящую эволюцию разума... уникальный симбиоз человеческого опыта и цифрового интеллекта. "
        "Код становится новой материей... фундаментом, на котором строятся наши будущие творения. "
        "Автоматизация труда. Она не заменяет нас... она освобождает человека для истинного творчества и самовыражения. "
        "Искусственный интеллект вдохновляет на новые формы искусства... расширяя границы нашей фантазии до бесконечности. "
        "Образование трансформируется прямо сейчас... оно становится персональным... доступным каждому, в любой точке планеты. "
        "В медицине происходит революция. Цифровой разум обеспечивает каждому из нас доступ к диагностике... и лечению высочайшего уровня. "
        "Умные города и экологичные технологии. С помощью современных алгоритмов... мы находим способы сохранить наш общий дом... нашу планету. "
        "Но с великой силой приходят и вопросы... вопросы безопасности... и этики. Они требуют нашего глубокого внимания. "
        "Мы учимся взаимодействовать с новым типом разума... выстраивая мосты взаимопонимания... и сотрудничества. "
        "Глобальная сеть интеллектуальных систем объединяет мир... и ускоряет наше общее развитие... с каждым днем. "
        "Две тысячи двадцать шестой год. Это лишь начало новой эры... где разум и технологии создают совершенно новый мир... мир будущего."
    )

    # Mapping scenes to images (using the ones generated across steps)
    gen_dir = Path("/Users/macbook/.gemini/antigravity/brain/74acf072-6bc0-4fdc-9ad0-33f04fb9fa16")

    # Selecting the best 15 images and defining keywords for B-roll (POWER, NATURE, CINEMA)
    scene_data = [
        {"image": "ai_scene_1_network", "keyword": "cinematic nebula space 4k slow motion"},
        {"image": "ai_scene_2_economy", "keyword": "stormy ocean waves cinematic 4k"},
        {"image": "ai_scene_3_content_gen", "keyword": "lion roar slow motion cinematic"},
        {"image": "ai_future_bg_3", "keyword": "eagle flying mountains cinematic"},
        {"image": "ai_future_bg_4", "keyword": "lightning storm night sky cinematic"},
        {"image": "ai_scene_6_code_matter", "keyword": "matrix code rain slow motion cinematic"},
        {"image": "ai_future_bg_1", "keyword": "mountain fireplace cozy dark cinematic"},
        {"image": "ai_scene_8_art_exhibit", "keyword": "ink in water slow motion cinematic"},
        {"image": "ai_scene_9_edu_tutor", "keyword": "old library bookshelf cinematic"},
        {"image": "ai_fact_3_medical", "keyword": "human heart 3d rendering cinematic"},
        {"image": "ai_scene_11_green_city", "keyword": "waterfall cinematic 4k slow motion"},
        {"image": "ai_scene_12_ethics_safety", "keyword": "cyber attack digital shield cinematic"},
        {"image": "ai_fact_1_robot", "keyword": "artificial intelligence robot thinking cinematic"},
        {"image": "ai_scene_14_global_net_earth", "keyword": "planet earth from space cinematic"},
        {"image": "ai_scene_15_sunrise_digital", "keyword": "futuristic city sunrise cinematic"}
    ]

    selected_scenes = []
    for scene in scene_data:
        matches = list(gen_dir.glob(f"{scene['image']}_*.png"))
        if matches:
            selected_scenes.append({
                "image": sorted(matches)[-1],
                "keyword": scene['keyword']
            })
        else:
            print(f"⚠️ Image {scene['image']} not found in {gen_dir}")

    print(f"🔍 Found {len(selected_scenes)}/15 scenes with images.")

    # Run RU pipeline
    if len(selected_scenes) >= 15:
        run_no_face_pipeline(script_ru, lang="ru", output_name="ai_council_ru", scenes=selected_scenes)

        # English translation (Refined for Natural TTS)
        script_en = (
            "Welcome to the year twenty twenty-six... a world where artificial intelligence has become an inseparable part of our reality... forever changing our economy and our society. "
            "Fifteen trillion dollars. That is how much AI has contributed to the global wealth... becoming the ultimate engine of progress. "
            "Ninety percent of the content we consume every single day... is now generated by algorithms. From breaking news... to cinema and music. "
            "Tasks that used to take decades of research... are now solved in just a few weeks. This opens up new... incredible horizons for all of humanity. "
            "We are witnessing a true evolution of the mind... a unique symbiosis between human experience and digital intelligence. "
            "Code is becoming the new matter... the very foundation upon which our future creations are built. "
            "The automation of labor. It is not here to replace us... it is here to free us for true creativity and self-expression. "
            "Artificial intelligence inspires new forms of art... pushing the boundaries of our imagination to infinity. "
            "Education is transforming right before our eyes. It is becoming personal... accessible to everyone, anywhere on the planet. "
            "A revolution is happening in healthcare. AI provides each of us with diagnostics... and medical care of the highest standard. "
            "Smart cities and sustainable technologies. With the help of AI... we are finding ways to preserve our common home... our planet. "
            "But with great power come deep questions... questions of safety... and ethics. They demand our absolute attention. "
            "We are learning to interact with a new kind of consciousness... building bridges of understanding... and cooperation. "
            "A global network of intelligent systems is uniting the world... accelerating our collective progress... every single day. "
            "Twenty twenty-six. This is just the beginning of a new era... where mind and technology unite to create a completely new world... the world of tomorrow."
        )
        run_no_face_pipeline(script_en, lang="en", output_name="ai_council_en", scenes=selected_scenes)
    else:
        print(f"❌ Not enough images found ({len(selected_scenes)}/15). Check gen_dir: {gen_dir}")
