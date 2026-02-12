import os
import random
import subprocess
from pathlib import Path

from dotenv import load_dotenv

# Try to import for type checking, but handle import errors gracefully
try:
    import google.generativeai as genai
except ImportError:
    genai = None

# =============================================================================
#                           CONFIGURATION
# =============================================================================

# Define Root Paths
SRC_DIR = Path(
    __file__
).parent.parent.parent.resolve()  # src/pipeline/.. -> src -> Content_Factory
ROOT_DIR = SRC_DIR.parent
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR_OVERRIDE", str(ROOT_DIR / "outputs")))
INPUT_DIR = ROOT_DIR / "inputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load Environment Variables from multiple sources
load_dotenv(ROOT_DIR / ".env")
load_dotenv(ROOT_DIR.parent / "AI_Core" / ".env")

# Voice Constants
VOICE_RU = "ru-RU-DmitryNeural"
VOICE_EN = "en-US-ChristopherNeural"
OPENAI_VOICE_RU = "onyx"
OPENAI_VOICE_EN = "alloy"

# =============================================================================
#                           AUDIO GENERATION
# =============================================================================


def generate_audio_elevenlabs(text, output_path, api_key):
    """
    Generate audio using ElevenLabs API (Premium).
    Returns True if successful, False otherwise.
    """
    print("🎤 Generating ElevenLabs Audio...")
    try:
        import requests

        if not api_key:
            return False

        headers = {"xi-api-key": api_key, "Content-Type": "application/json"}

        # Using "Adam" or a deep narration voice
        # Voice ID: pNInz6obpgDQGcFmaJgB (Adam) - reliable professional male
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }

        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"

        response = requests.post(url, json=data, headers=headers, timeout=60)

        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print("✅ ElevenLabs Success!")
            return True
        else:
            print(f"❌ ElevenLabs Failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"❌ ElevenLabs Exception: {e}")
        return False


def generate_audio_openai(text, output_path, voice="alloy"):
    """
    Generate audio using OpenAI TTS (Secondary).
    """
    print(f"🎤 Generating OpenAI Audio ({voice})...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ OpenAI Key not found, skipping OpenAI TTS")
        return False
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
        response.stream_to_file(output_path)
        print("✅ OpenAI TTS Success!")
        return True
    except Exception as e:
        print(f"❌ OpenAI TTS Error: {e}")
        return False


def generate_audio_edge(text, output_path, voice):
    """
    Generate audio using EdgeTTS (Fallback).
    """
    print(f"🎤 Generating Edge-TTS Audio (voice={voice})...")
    import asyncio

    import edge_tts

    async def _gen():
        tts = edge_tts.Communicate(text, voice)
        await tts.save(str(output_path))

    try:
        asyncio.run(_gen())
        if output_path.exists() and output_path.stat().st_size > 1000:
            print("✅ Edge-TTS Success!")
            return True
        return False
    except Exception as e:
        print(f"❌ Edge-TTS Error: {e}")
        return False


# =============================================================================
#                           VISUAL ASSETS
# =============================================================================


def generate_image_imagen(prompt, output_path):
    """
    Generate image using Google Gemini (Imagen 3).
    """
    print(f"🎨 Generating Imagen 3 Image: {prompt}...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ Gemini Key not found, skipping Imagen.")
        return False

    if not genai:
        print("⚠️ google.generativeai not installed/imported.")
        return False

    try:
        genai.configure(api_key=api_key)
        # Check for model access helper or assume model name
        model = genai.GenerativeModel("imagen-3.0-generate-001")

        # Note: The API call might differ slightly based on specific version
        # This is a standard specialized generation call pattern
        images = model.generate_images(
            prompt=prompt,
            number_of_images=1,
            aspect_ratio="9:16",
            safety_filter_level="block_only_high",
            person_generation="allow_adult",
        )

        if images and images[0]:
            images[0].save(output_path)
            print("✅ Imagen Success!")
            return True
        return False
    except Exception as e:
        # Fallback to DALL-E 3 if Gemini fails or logic differs
        print(f"❌ Imagen Error (Trying DALL-E fallback): {e}")
        return generate_image_dalle(prompt, output_path)


def generate_image_dalle(prompt, output_path):
    """
    Generate image using DALL-E 3 (OpenAI).
    """
    print(f"🎨 Generating DALL-E 3 Image: {prompt}...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",  # Portrait-ish
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        import requests

        img_data = requests.get(image_url).content
        with open(output_path, "wb") as f:
            f.write(img_data)
        print("✅ DALL-E 3 Success!")
        return True
    except Exception as e:
        print(f"❌ DALL-E 3 Error: {e}")
        return False


def fetch_pexels_video(keyword, output_path, api_key):
    """
    Fetch stock video from Pexels (Primary Visual).
    """
    print(f"🔍 Searching Pexels for: {keyword}...")
    try:
        import requests

        if not api_key:
            return False

        headers = {"Authorization": api_key}
        url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=1&orientation=portrait&size=medium"

        resp = requests.get(url, headers=headers, timeout=10)

        if resp.status_code == 200:
            data = resp.json()
            if data.get("videos"):
                # Get best quality link (usually first)
                video_files = data["videos"][0]["video_files"]
                # Prefer HD
                best_link = None
                for vf in video_files:
                    if vf["width"] >= 720:  # At least 720p
                        best_link = vf["link"]
                        break
                if not best_link:
                    best_link = video_files[0]["link"]

                print(f"⬇️ Downloading Pexels Clip: {best_link}")
                v_resp = requests.get(best_link, timeout=30)
                with open(output_path, "wb") as f:
                    f.write(v_resp.content)
                return True

        print(f"⚠️ Pexels not found for '{keyword}'")
        return False
    except Exception as e:
        print(f"❌ Pexels Exception: {e}")
        return False


# =============================================================================
#                           MAIN PIPELINE
# =============================================================================


def run_no_face_pipeline(
    text: str,
    lang: str = "ru",
    output_name: str = "no_face_video",
    scenes: list[dict] = None,
    style: str = "impact",
):

    print(f"\n🚀 Starting ENHANCED NO-FACE Pipeline (lang={lang}, style={style})")
    print(f"📂 Output Path: {OUTPUT_DIR / output_name}")

    if not text:
        print("❌ Error: No text provided.")
        return

    # 1. Generate Audio
    audio_path = INPUT_DIR / f"{output_name}_audio.wav"
    audio_generated = False

    # Try ElevenLabs FIRST
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    if eleven_key and generate_audio_elevenlabs(text, audio_path, eleven_key):
        audio_generated = True

    # Validations Fallback
    if not audio_generated:
        print("⚠️ Falling back to OpenAI/Edge-TTS...")
        voice_oai = OPENAI_VOICE_RU if lang == "ru" else OPENAI_VOICE_EN
        if not generate_audio_openai(text, audio_path, voice=voice_oai):
            voice_edge = VOICE_RU if lang == "ru" else VOICE_EN
            if not generate_audio_edge(text, audio_path, voice_edge):
                print("❌ All audio generation failed.")
                return

    print(f"✅ Audio Ready: {audio_path}")

    # 2. Analyze Audio Duration (CRITICAL: Correct Length Calculation)
    try:
        probe = subprocess.check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(audio_path),
            ]
        )
        audio_duration = float(probe.strip())
    except Exception:
        audio_duration = 10.0  # fallback

    print(f"⏱️ Audio Duration: {audio_duration:.2f}s")

    # Make video slightly longer than audio to prevent cutoff
    total_video_duration = audio_duration + 2.0

    # Calculate Scene Duration
    if not scenes:
        scenes = [{"keyword": "digital abstract background"}]
    num_scenes = len(scenes)
    scene_duration = total_video_duration / num_scenes

    print(f"⏱️ Scene Duration: {scene_duration:.2f}s (x{num_scenes} scenes)")

    # 3. Prepare Clips
    clips: list[Path] = []
    pexels_key = os.getenv("PEXELS_API_KEY")

    for i, scene in enumerate(scenes):
        print(f"🎬 Processing Scene {i+1}/{num_scenes}...")

        keyword = scene.get("keyword", "abstract")
        clip_name = f"{output_name}_seg_{i}.mp4"
        clip_raw = OUTPUT_DIR / f"{output_name}_raw_seg_{i}.mp4"
        clip_final = OUTPUT_DIR / clip_name

        success = False

        # A) Try Pexels (Motion)
        if pexels_key and fetch_pexels_video(keyword, clip_raw, pexels_key):
            success = True

        # B) Try AI Image Gen (Static -> Video) if Pexels failed
        if not success:
            img_path = OUTPUT_DIR / f"{output_name}_gen_{i}.png"
            if generate_image_imagen(
                keyword + " cinematic, photorealistic, 8k", img_path
            ):
                # Convert Image to Video
                cmd = [
                    "ffmpeg",
                    "-y",
                    "-loop",
                    "1",
                    "-i",
                    str(img_path),
                    "-t",
                    str(scene_duration),
                    "-vf",
                    "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-r",
                    "30",
                    str(clip_raw),
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                success = True

        # C) Fallback Color
        if not success:
            print(f"🎨 Generating fallback for scene {i}")
            color = random.choice(["black", "blue", "red"])
            cmd = [
                "ffmpeg",
                "-y",
                "-f",
                "lavfi",
                "-i",
                f"color=c={color}:s=1080x1920:d={scene_duration}",
                "-vf",
                f"drawtext=text='{keyword}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2",
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-r",
                "30",
                str(clip_raw),
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        # Normalize Clip (Resize/Crop/Time)
        # We ensure every clip is EXACTLY scene_duration
        cmd_norm = [
            "ffmpeg",
            "-y",
            "-i",
            str(clip_raw),
            "-t",
            str(scene_duration),
            "-vf",
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-r",
            "30",
            "-an",  # No audio in segments
            str(clip_final),
        ]
        subprocess.run(cmd_norm, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        clips.append(clip_final)

    # 4. Concatenate Clips
    concat_list = OUTPUT_DIR / f"{output_name}_concat.txt"
    with open(concat_list, "w") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    video_no_audio = OUTPUT_DIR / f"{output_name}_video.mp4"
    print("🎬 Concatenating...")

    cmd_concat = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list),
        "-c",
        "copy",
        str(video_no_audio),
    ]
    try:
        subprocess.run(
            cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
    except Exception as e:
        print(f"❌ Concat failed: {e}")
        return

    # 5. Final Mix (Audio + Music + Video)
    final_video = OUTPUT_DIR / f"{output_name}_final.mp4"
    print("🔊 Mixing Final Audio & Video...")

    # Simple placeholder music synthesis (nullsrc) or file check
    # In future: download or generate music to music.mp3
    # For now: We use a filter to keep audio length correct

    cmd_mix = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_no_audio),
        "-i",
        str(audio_path),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",  # Cut video if it is longer than audio (it shouldn't be much longer due to +2s buffer)
        "-fflags",
        "+shortest",
        str(final_video),
    ]

    try:
        subprocess.run(
            cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
        print(f"\n✨ DONE: {final_video}")
    except Exception as e:
        print(f"❌ Final mix failed: {e}")


if __name__ == "__main__":
    # Test run
    scenes = [
        {"keyword": "cyberpunk city"},
        {"keyword": "artificial intelligence brain"},
        {"keyword": "space travel mars"},
    ]
    run_no_face_pipeline(
        "This is a test of the fully operational video system.",
        lang="en",
        output_name="test_system_v3",
        scenes=scenes,
    )
