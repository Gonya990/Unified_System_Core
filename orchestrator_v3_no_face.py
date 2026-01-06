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
from dotenv import load_dotenv

# Setup paths
ROOT_DIR = Path(__file__).parent.resolve()
sys.path.append(str(ROOT_DIR))

# Load API keys from potential locations
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR / "LLM_Council" / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")

# Import internal tools
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

# Voice options (OpenAI TTS preferred, Edge-TTS fallback)
VOICES = {
    "en": "alloy",       # More neutral/pro
    "en_female": "shimmer",
    "ru": "alloy",       # Clear, professional male
    "ru_female": "shimmer",
    "fallback_ru": "ru-RU-DmitryNeural",
    "fallback_en": "en-US-EmmaNeural"
}

def generate_audio_openai(text: str, output_path: Path, voice: str) -> bool:
    """Generate audio using OpenAI TTS"""
    print(f"🎙 Generating Premium OpenAI Audio (voice={voice})...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False
        
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        # Prepare text - OpenAI handles punctuation well
        response = client.audio.speech.create(
            model="tts-1-hd",
            voice=voice,
            input=text
        )
        
        mp3_path = output_path.with_suffix(".mp3")
        response.stream_to_file(str(mp3_path))
        
        # Convert to WAV
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3_path),
            "-ar", "16000", "-ac", "1", str(output_path)
        ], check=True, capture_output=True)
        
        print(f"✅ Premium Audio: {output_path}")
        return True
    except Exception as e:
        print(f"❌ OpenAI TTS failed: {e}")
        return False

def generate_audio_edge(text: str, output_path: Path, voice: str) -> bool:
    """Generate audio using Edge-TTS with rate control for better naturalness"""
    print(f"🎤 Generating Enhanced Edge-TTS Audio (voice={voice}, rate=-10%)...")
    
    mp3_path = output_path.with_suffix(".mp3")
    
    # Try multiple ways to find edge-tts
    edge_tts_cmd = "edge-tts"
    venv_bin = ROOT_DIR / "venv_content/bin/edge-tts"
    if venv_bin.exists():
        edge_tts_cmd = str(venv_bin)
        
    # Using --rate to slow down speech for more natural delivery
    cmd = [
        edge_tts_cmd, 
        "--text", text, 
        "--write-media", str(mp3_path), 
        "--voice", voice,
        "--rate", "-10%"
    ]
    
    try:
        subprocess.run(cmd, check=True, cwd=str(ROOT_DIR))
        # Convert to WAV
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3_path),
            "-ar", "16000", "-ac", "1", str(output_path)
        ], check=True, capture_output=True)
        print(f"✅ Enhanced Fallback Audio: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Edge-TTS failed: {e}")
        return False

def generate_audio(text: str, output_path: Path, lang: str = "en") -> bool:
    """Main audio generation with premium support and fallback"""
    voice = VOICES.get(lang, VOICES["en"])
    
    # 1. Try OpenAI (Premium)
    if generate_audio_openai(text, output_path, voice):
        return True
        
    # 2. Fallback to Edge-TTS
    fallback_voice = VOICES.get(f"fallback_{lang}", "en-US-ChristopherNeural")
    return generate_audio_edge(text, output_path, fallback_voice)

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
            "-c:v", "libx264", "-pix_fmt", "yuv4202p",
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

def assemble_hybrid_video(audio_path: Path, scenes: List[Dict], output_path: Path):
    """
    Create a HIGH-ENERGY hybrid video. 
    Prioritizes B-Roll (80%) and uses AI Images as stylized flashes (20%).
    """
    print(f"🔥 Assembling DYNAMIC high-energy video sequence...")
    
    audio_duration = float(subprocess.run([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ], capture_output=True, text=True).stdout.strip())
    
    num_scenes = len(scenes)
    seg_duration = audio_duration / num_scenes
    
    segments = []
    
    for i, scene in enumerate(scenes):
        img_path = scene['image']
        keyword = scene['keyword']
        
        # 1. B-Roll Segment (Hero - 80% of time)
        broll_duration = seg_duration * 0.8
        img_duration = seg_duration * 0.2
        
        # Fast cutting: We try to get 2 clips per keyword to keep it moving
        broll_clips = semantic_search_broll(keyword, BROLL_DIR, num_clips=2)
        
        if broll_clips:
            # First clip
            clip_path = broll_clips[0]
            seg_path_b1 = OUTPUT_DIR / f"dyn_seg_{i}_b1.mp4"
            subprocess.run([
                "ffmpeg", "-y", "-i", str(clip_path),
                "-t", str(broll_duration / 2),
                "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.1:brightness=0.02:saturation=1.3",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(seg_path_b1)
            ], check=True, capture_output=True)
            segments.append(seg_path_b1)
            
            # Second clip (if exists) or stylized image flash
            if len(broll_clips) > 1:
                clip_path_2 = broll_clips[1]
                seg_path_b2 = OUTPUT_DIR / f"dyn_seg_{i}_b2.mp4"
                subprocess.run([
                    "ffmpeg", "-y", "-i", str(clip_path_2),
                    "-t", str(broll_duration / 2),
                    "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=contrast=1.1:saturation=1.2",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(seg_path_b2)
                ], check=True, capture_output=True)
                segments.append(seg_path_b2)
            else:
                img_duration += broll_duration / 2
        else:
            img_duration = seg_duration

        # 2. AI Image Segment (Visionary Flash with aggressive pan)
        seg_path_img = OUTPUT_DIR / f"dyn_seg_{i}_img.mp4"
        # Dynamic pan direction
        x_expr = "iw/2-(iw/zoom/2)"
        y_expr = f"ih/2-(ih/zoom/2)+({'100' if i%2==0 else '-100'}*t/d)"
        
        cmd_img = [
            "ffmpeg", "-y", "-loop", "1", "-i", str(img_path),
            "-t", str(img_duration),
            "-vf", f"scale=2000:-1,zoompan=z='1.1':x='{x_expr}':y='{y_expr}':d=1:s=1080x1920:fps=30,"
                   f"vignette=angle=0.3,unsharp=5:5:1.0:5:5:0.0",
            "-pix_fmt", "yuv420p", "-c:v", "libx264", "-r", "30",
            str(seg_path_img)
        ]
        subprocess.run(cmd_img, check=True, capture_output=True)
        segments.append(seg_path_img)

    # Concat
    concat_file = OUTPUT_DIR / "dyn_concat.txt"
    with open(concat_file, "w") as f:
        for seg in segments:
            f.write(f"file '{seg.name}'\n")
            
    video_no_audio = OUTPUT_DIR / "temp_dynamic_video.mp4"
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c", "copy", str(video_no_audio)
    ], check=True, capture_output=True, cwd=str(OUTPUT_DIR))
    
    # Final merge with audio
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

def run_no_face_pipeline(text: str, lang: str = "ru", output_name: str = "no_face_video", scenes: List[Dict] = None):
    """Run pipeline without face usage"""
    print(f"\n🚀 Starting ENHANCED NO-FACE Pipeline (lang={lang})")
    
    # 1. Audio
    audio_path = INPUT_DIR / f"{output_name}_audio.wav"
    if not generate_audio(text, audio_path, lang):
        return None
        
    # 2. Visuals
    final_video = OUTPUT_DIR / f"{output_name}_final.mp4"
    raw_video = OUTPUT_DIR / f"{output_name}_raw.mp4"
    
    if scenes:
        assemble_hybrid_video(audio_path, scenes, raw_video)
    else:
        # Fallback to simple B-Roll logic if no scenes provided
        clips = semantic_search_broll(text, BROLL_DIR, num_clips=5)
        if clips:
            assemble_broll_only_video(audio_path, clips, raw_video)
        else:
            print("❌ No visual assets found.")
            return None
    
    # 3. Subtitles
    if not add_subtitles(raw_video, final_video, lang):
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
    
    # Selecting the best 15 images and defining keywords for B-roll
    scene_data = [
        {"image": "ai_scene_1_network", "keyword": "neural network digital"},
        {"image": "ai_scene_2_economy", "keyword": "world economy growth"},
        {"image": "ai_scene_3_content_gen", "keyword": "digital content creation"},
        {"image": "ai_future_bg_3", "keyword": "science laboratory future"},
        {"image": "ai_future_bg_4", "keyword": "human brain digital"},
        {"image": "ai_scene_6_code_matter", "keyword": "coding developer matrix"},
        {"image": "ai_future_bg_1", "keyword": "robot automation factory"},
        {"image": "ai_scene_8_art_exhibit", "keyword": "modern art digital gallery"},
        {"image": "ai_scene_9_edu_tutor", "keyword": "education future technology"},
        {"image": "ai_fact_3_medical", "keyword": "medical technology robot"},
        {"image": "ai_scene_11_green_city", "keyword": "smart city green energy"},
        {"image": "ai_scene_12_ethics_safety", "keyword": "cyber security ethics"},
        {"image": "ai_fact_1_robot", "keyword": "human robot handshake"},
        {"image": "ai_scene_14_global_net_earth", "keyword": "global network earth space"},
        {"image": "ai_scene_15_sunrise_digital", "keyword": "sunrise future city horizon"}
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
        print(f"❌ Not enough images found ({len(selected_images)}/15). Check generation.")
