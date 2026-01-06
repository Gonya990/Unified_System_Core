#!/usr/bin/env python3
"""
Content Farm Orchestrator v3 - NO FACE
Complete pipeline: Text -> Voice -> B-Roll -> Subtitles
Supports Russian and English voices
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict
import json

# Import internal tools
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

try:
    from pexels_broll import semantic_search_broll
    from video_assembler import create_video_with_broll, get_video_duration
except ImportError:
    print("⚠️ Internal tools not found. Script might fail.")

OUTPUT_DIR = ROOT_DIR / "outputs"
INPUT_DIR = ROOT_DIR / "inputs"
BROLL_DIR = ROOT_DIR / "broll"

OUTPUT_DIR.mkdir(exist_ok=True)
INPUT_DIR.mkdir(exist_ok=True)
BROLL_DIR.mkdir(exist_ok=True)

# Voice options (Edge-TTS)
VOICES = {
    "en": "en-US-ChristopherNeural",  # English male
    "en_female": "en-US-JennyNeural",  # English female  
    "ru": "ru-RU-DmitryNeural",         # Russian male
    "ru_female": "ru-RU-SvetlanaNeural" # Russian female
}

def generate_audio(text: str, output_path: Path, lang: str = "en") -> bool:
    """Generate audio using Edge-TTS"""
    print(f"🎤 Generating Audio ({lang})...")
    
    voice = VOICES.get(lang, VOICES["en"])
    mp3_path = output_path.with_suffix(".mp3")
    
    # Try multiple ways to find edge-tts
    edge_tts_cmd = "edge-tts"
    venv_bin = ROOT_DIR / "venv_content/bin/edge-tts"
    if venv_bin.exists():
        edge_tts_cmd = str(venv_bin)
        
    cmd = [edge_tts_cmd, "--text", text, "--write-media", str(mp3_path), "--voice", voice]
    
    try:
        subprocess.run(cmd, check=True, cwd=str(ROOT_DIR))
        # Convert to WAV
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3_path),
            "-ar", "16000", "-ac", "1", str(output_path)
        ], check=True, capture_output=True)
        print(f"✅ Audio: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Audio failed: {e}")
        return False

def add_subtitles(video_path: Path, output_path: Path, lang: str = "en") -> bool:
    """Add dynamic subtitles using PyCaps"""
    print(f"📝 Adding subtitles...")
    
    cmd = [
        "pycaps",
        str(video_path),
        "-o", str(output_path),
        "--style", "hormozi",
        "--font-size", "70",
        "--stroke-width", "4"
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=str(ROOT_DIR))
        print(f"✅ Subtitles: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Subtitles failed: {e}")
        return False

def assemble_broll_only_video(audio_path: Path, clips: List[Path], output_path: Path):
    """
    Create a video containing ONLY B-Roll clips, matched to audio length
    """
    print(f"🎬 Assembling B-Roll only video...")
    
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
        
        trimmed_path = OUTPUT_DIR / f"temp_clip_{len(final_clips)}.mp4"
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
    concat_list = OUTPUT_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for clip in final_clips:
            f.write(f"file '{clip.name}'\n")
            
    video_no_audio = OUTPUT_DIR / "temp_video_no_audio.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy", str(video_no_audio)
    ], check=True, capture_output=True, cwd=str(OUTPUT_DIR))
    
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

def assemble_slideshow_video(audio_path: Path, images: List[Path], output_path: Path):
    """
    Create a professional slideshow with Ken Burns (zoom) effect
    """
    print(f"🖼 Assembling professional slideshow from {len(images)} images...")
    
    audio_duration = float(subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ], capture_output=True, text=True).stdout.strip())
    
    if not images:
        print("❌ No images provided")
        return False
        
    img_duration = audio_duration / len(images)
    
    # We will use a complex filter to generate zoom effects for each image and then concat them
    # This is more robust than simple concat for "movement"
    
    segments = []
    for i, img in enumerate(images):
        seg_path = OUTPUT_DIR / f"seg_zoom_{i}.mp4"
        # Ken Burns effect: zoom in slowly
        # scale=8000:-1: zooming works better on higher res
        # zoompan: zoom=zoom+0.001 (slow zoom)
        cmd = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(img),
            "-t", str(img_duration),
            "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
                   "zoompan=z='zoom+0.0005':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=125:s=1080x1920",
            "-pix_fmt", "yuv420p", "-c:v", "libx264", "-r", "30",
            str(seg_path)
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        segments.append(seg_path)
        
    # Concat segments
    concat_file = OUTPUT_DIR / "seg_concat.txt"
    with open(concat_file, "w") as f:
        for seg in segments:
            f.write(f"file '{seg.name}'\n")
            
    video_no_audio = OUTPUT_DIR / "temp_motion_video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-c", "copy", str(video_no_audio)
    ], check=True, capture_output=True, cwd=str(OUTPUT_DIR))
    
    # Final merge
    subprocess.run([
        "ffmpeg", "-y", "-i", str(video_no_audio), "-i", str(audio_path),
        "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0",
        "-shortest", str(output_path)
    ], check=True, capture_output=True)
    
    # Cleanup
    for seg in segments: seg.unlink()
    video_no_audio.unlink()
    concat_file.unlink()
    return True

def run_no_face_pipeline(text: str, lang: str = "ru", output_name: str = "no_face_video", image_paths: List[Path] = None):
    """Run pipeline without face usage"""
    print(f"\n🚀 Starting NO-FACE Pipeline (lang={lang})")
    
    # 1. Audio
    audio_path = INPUT_DIR / f"{output_name}_audio.wav"
    if not generate_audio(text, audio_path, lang):
        return None
        
    # 2. Visuals (B-Roll or Slideshow)
    raw_video = OUTPUT_DIR / f"{output_name}_raw.mp4"
    
    if image_paths:
        assemble_slideshow_video(audio_path, image_paths, raw_video)
    else:
        # Fallback to B-Roll
        clips = semantic_search_broll(text, BROLL_DIR, num_clips=5)
        if clips:
            assemble_broll_only_video(audio_path, clips, raw_video)
        else:
            print("❌ No visual assets found.")
            return None
    
    # 3. Subtitles
    final_video = OUTPUT_DIR / f"{output_name}_final.mp4"
    if not add_subtitles(raw_video, final_video, lang):
        print("⚠️ Subtitles failed, using raw video.")
        if final_video.exists(): final_video.unlink()
        raw_video.rename(final_video)
        
    print(f"\n✨ DONE: {final_video}")
    return final_video

if __name__ == "__main__":
    # Extended Script with Facts
    script_ru = (
        "Искусственный интеллект в 2026 году — это не просто чат-боты. "
        "Знаете ли вы, что современные модели уже обладают уровнем логики, сопоставимым с докторантами топовых вузов? "
        "К 2030 году вклад ИИ в мировую экономику составит невероятные 15 триллионов долларов. "
        "Уже сегодня нейросети проектируют новые материалы за недели, на что раньше уходили десятилетия. "
        "А к концу этого года более 90 процентов цифрового контента будет создано при поддержке алгоритмов. "
        "Мы живем в эпоху самой быстрой технологической революции в истории человечества. "
        "Будущее уже наступило, и оно работает на коде."
    )
    
    script_en = (
        "AI in 2026 is far more than just chatbots. "
        "Did you know that modern models now possess reasoning capabilities comparable to PhD students at top universities? "
        "By 2030, AI is predicted to contribute a staggering 15 trillion dollars to the global economy. "
        "Today, neural networks are designing new materials in weeks — a process that used to take decades. "
        "By the end of this year, over 90 percent of online content will be generated or assisted by algorithms. "
        "We are living through the fastest technological revolution in human history. "
        "The future has arrived, and it runs on code."
    )
    
    # Local generated images
    gen_dir = Path("/Users/macbook/.gemini/antigravity/brain/74acf072-6bc0-4fdc-9ad0-33f04fb9fa16")
    images = sorted(list(gen_dir.glob("ai_*.png")))
    
    # Run RU
    run_no_face_pipeline(script_ru, lang="ru", output_name="ai_edu_ru", image_paths=images)
    
    # Run EN
    run_no_face_pipeline(script_en, lang="en", output_name="ai_edu_en", image_paths=images)
