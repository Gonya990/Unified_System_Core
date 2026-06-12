import hashlib
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# Import NEW Google GenAI SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai library not found.")
    genai = None

from src.video.ai_video_generator import VideoGenerator

# =============================================================================
#                           CONFIGURATION
# =============================================================================

SRC_DIR = Path(__file__).parent.parent.parent.resolve()  # Projects/Content_Factory
ROOT_DIR = SRC_DIR.parent.parent.resolve()  # Unified_System_Core
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR_OVERRIDE", str(SRC_DIR / "outputs")))
INPUT_DIR = SRC_DIR / "inputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(ROOT_DIR / ".env", override=True)  # Root .env
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=True)  # AI Core .env
load_dotenv(SRC_DIR / ".env", override=True)  # Content Factory .env

GCS_BUCKET = "content-factory-outputs-435112"

# =============================================================================
#                           AUDIO GENERATION
# =============================================================================


def _tts_rotation_order(text: str) -> list[str]:
    provider = (os.getenv("TTS_PROVIDER") or "").strip().lower()
    if provider:
        providers = [provider]
    else:
        rotation = os.getenv("TTS_ROTATION", "elevenlabs,edge")
        providers = [p.strip().lower() for p in rotation.split(",") if p.strip()]

    allow_openai = os.getenv("ALLOW_OPENAI_TTS", "false").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if not allow_openai:
        providers = [p for p in providers if p != "openai"]

    if not providers:
        providers = ["edge"]

    rotate_order = os.getenv("TTS_ROTATE_ORDER", "false").strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )
    if rotate_order and len(providers) > 1 and text:
        h = hashlib.sha256(text.encode("utf-8")).hexdigest()
        shift = int(h, 16) % len(providers)
        providers = providers[shift:] + providers[:shift]
    return providers


def _select_eleven_voice_id(lang: str, text: str) -> str:
    lang_key = f"ELEVENLABS_VOICE_ID_{lang.upper()}"
    voice_id = (os.getenv(lang_key) or os.getenv("ELEVENLABS_VOICE_ID") or "").strip()
    voices = os.getenv("ELEVENLABS_VOICE_IDS", "").strip()
    rotation_mode = os.getenv("ELEVENLABS_VOICE_ROTATION", "random").strip().lower()
    if voices:
        ids = [v.strip() for v in voices.split(",") if v.strip()]
        if ids:
            if rotation_mode == "hash":
                if text:
                    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
                    voice_id = ids[int(h, 16) % len(ids)]
                else:
                    voice_id = ids[0]
            else:
                voice_id = random.choice(ids)
    if not voice_id:
        voice_id = "pNInz6obpgDQGcFmaJgB"
    return voice_id


def generate_audio_elevenlabs(text, output_path, api_key, lang: str = "en"):
    """Generate audio using ElevenLabs API (preferred)."""
    print("🎤 Generating ElevenLabs Audio...")
    try:
        if not api_key:
            return False
        headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
        data = {
            "text": text,
            "model_id": os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
        voice_id = _select_eleven_voice_id(lang, text)
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        if resp.status_code != 200:
            print(f"❌ ElevenLabs Failed: {resp.status_code}")
            return False
        tmp_mp3 = output_path.with_suffix(".mp3")
        with open(tmp_mp3, "wb") as f:
            f.write(resp.content)
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(tmp_mp3),
                "-ar",
                "44100",
                "-ac",
                "2",
                "-b:a",
                "192k",
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )
        tmp_mp3.unlink(missing_ok=True)
        print("✅ ElevenLabs Success!")
        return True
    except Exception as e:
        print(f"❌ ElevenLabs Exception: {e}")
        return False


def generate_audio_openai(text, output_path, voice="alloy"):
    """Generate audio using OpenAI TTS."""
    print(f"🎤 Generating OpenAI Audio ({voice})...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False


def generate_audio_edge(text, output_path, lang: str = "en") -> bool:
    """Generate audio using Edge-TTS (free fallback)."""
    voice_map = {
        "ru": "ru-RU-DmitryNeural",
        "en": "en-US-EmmaNeural",
        "he": "he-IL-AvriNeural",
    }
    voice = voice_map.get(lang, "en-US-EmmaNeural")
    
    # Force use venv edge-tts
    venv_bin = Path(sys.executable).parent
    cmd = str(venv_bin / "edge-tts")
    if not Path(cmd).exists():
        cmd = "edge-tts" # fallback
    try:
        subprocess.run(
            [
                cmd,
                "--voice",
                voice,
                "--text",
                text,
                "--write-media",
                str(output_path),
            ],
            check=True,
            capture_output=True,
        )
        print(f"✅ Edge-TTS Success ({voice})")
        return True
    except Exception as e:
        print(f"❌ Edge-TTS Error: {e}")
        return False
    try:
        from openai import OpenAI

        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            return False
            
        client = OpenAI(api_key=openai_key)
        response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
        response.stream_to_file(output_path)
        print("✅ OpenAI Success!")
        return True
    except Exception as e:
        print(f"❌ OpenAI TTS Error: {e}")
        return False


# =============================================================================
#                           GCS UPLOAD
# =============================================================================


def upload_to_gcs(file_path: Path, bucket_name: str):
    """Uploads a file to Google Cloud Storage."""
    print(f"☁️ Uploading to GCS: {file_path.name}...")
    try:
        from google.cloud import storage

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        if not bucket.exists():
            print(f"⚠️ Bucket {bucket_name} not found. Attempting to create it...")
            try:
                bucket = client.create_bucket(bucket_name, location="US")
            except Exception as e_create:
                print(f"⚠️ Could not create bucket: {e_create}. Skipping GCS upload.")
                return False
        blob = bucket.blob(file_path.name)
        blob.upload_from_filename(str(file_path))
        print(f"✅ GCS Success: gs://{bucket_name}/{file_path.name}")
        return True
    except Exception as e:
        print(f"❌ GCS Upload Failed: {e}")
        return False


# =============================================================================
#                           DALL-E 3 FALLBACK
# =============================================================================


def generate_image_dalle3(prompt, output_path):
    """Generate image using OpenAI DALL-E 3."""
    print(f"🎨 Falling back to DALL-E 3 for: {prompt}...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return False
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1792",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        img_data = requests.get(image_url).content
        with open(output_path, "wb") as f:
            f.write(img_data)
        print("✅ DALL-E 3 Success!")
        return True
    except Exception as e:
        print(f"❌ DALL-E 3 Error: {e}")
        return False


# =============================================================================
#                           VISUAL ASSETS (IMAGEN 4.0 & VEO 2.0)
# =============================================================================


def generate_image_imagen4(prompt, output_path):
    print(f"🎨 Generating Imagen 4.0 Image: {prompt}...")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or not genai:
        print("⚠️ Gemini Key/SDK missing, trying DALL-E 3...")
        return generate_image_dalle3(prompt, output_path)

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="9:16"),
        )
        if response.generated_images:
            img = response.generated_images[0]
            with open(output_path, "wb") as f:
                f.write(img.image.image_bytes)
            print("✅ Imagen 4.0 Success!")
            return True
        else:
            print("⚠️ Imagen 4.0 returned no images, trying DALL-E 3...")
            return generate_image_dalle3(prompt, output_path)
    except Exception as e:
        print(f"❌ Imagen 4 Error: {e}. Trying DALL-E 3...")
        return generate_image_dalle3(prompt, output_path)


def fetch_pexels_video(keyword, output_path, api_key):
    print(f"🔍 Searching Pexels for: {keyword}...")
    try:
        if not api_key:
            return False
        headers = {"Authorization": api_key}
        url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=1&orientation=portrait&size=medium"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("videos"):
                video_files = data["videos"][0]["video_files"]
                best_link = next(
                    (vf["link"] for vf in video_files if vf["width"] >= 720),
                    video_files[0]["link"],
                )
                with open(output_path, "wb") as f:
                    f.write(requests.get(best_link, timeout=30).content)
                print(f"✅ Pexels Success: {keyword}")
                return True
        return False
    except Exception as e:
        print(f"❌ Pexels Exception: {e}")
        return False


# =============================================================================
#                           MAIN PIPELINE
# =============================================================================


def run_advanced_pipeline(
    text: str,
    lang: str = "ru",
    output_name: str = "video_v4",
    scenes: list[dict] = None,
    style: str = "impact",
):
    print(f"\n🚀 Starting ORCHESTRATOR V4.1 (IRONCLAD VISUALS - style={style})")

    if not text:
        return

    # 1. AUDIO
    audio_path = INPUT_DIR / f"{output_name}_audio.wav"
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    providers = _tts_rotation_order(text)
    print(f"🎛️ TTS provider order: {', '.join(providers)}")

    audio_ok = False
    for provider in providers:
        if provider == "elevenlabs":
            if eleven_key and generate_audio_elevenlabs(text, audio_path, eleven_key, lang=lang):
                audio_ok = True
                break
        elif provider == "edge":
            if generate_audio_edge(text, audio_path, lang=lang):
                audio_ok = True
                break
        elif provider == "openai":
            if generate_audio_openai(text, audio_path):
                audio_ok = True
                break

    if not audio_ok:
        print("❌ All TTS providers failed.")

    # 2. DURATION
    if not audio_path.exists():
        print(f"⚠️ Audio File NOT found: {audio_path}. Failsafe duration 10s.")
        audio_duration = 10.0
    else:
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
            print(f"🎵 Audio Duration: {audio_duration}s")
        except Exception as e:
            print(f"⚠️ FFProbe Error: {e}. Defaulting to 10s.")
            audio_duration = 10.0

    total_video_duration = audio_duration + 2.0
    if not scenes:
        scenes = [{"keyword": "futuristic technology"}]
    scene_duration = total_video_duration / len(scenes)

    # 3. VISUALS
    clips = []
    pexels_key = os.getenv("PEXELS_API_KEY")
    video_provider = os.getenv("VIDEO_PROVIDER", "luma")
    try:
        vid_gen = VideoGenerator(provider=video_provider)
        ai_video_enabled = True
    except Exception as e:
        print(f"⚠️ VideoGenerator Init Error: {e}")
        ai_video_enabled = False

    FPS = 30

    def process_scene(i, scene):
        print(f"🎬 Processing Scene {i + 1}/{len(scenes)}...")
        keyword = scene.get("keyword", "abstract futuristic")
        clip_final = OUTPUT_DIR / f"{output_name}_seg_{i}.mp4"
        clip_raw = OUTPUT_DIR / f"{output_name}_raw_seg_{i}.mp4"

        success = False

        # A0) Pre-generated Asset (from generate_vision_assets)
        pre_gen = scene.get("image")
        if pre_gen and Path(pre_gen).exists():
            pre_gen_path = Path(pre_gen)
            print(f"🎬 Using pre-generated asset: {pre_gen_path.name}")
            if pre_gen_path.suffix.lower() in [".mp4", ".mov", ".webm"]:
                # Just copy/use as raw clip
                shutil.copy2(pre_gen_path, clip_raw)
                success = True
            else:
                # It's an image, do the zoom animation
                print(f"🎬 Animating pre-generated image...")
                temp_scaled = OUTPUT_DIR / f"{output_name}_scaled_{i}.png"
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-i",
                        str(pre_gen_path),
                        "-vf",
                        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                        str(temp_scaled),
                    ],
                    capture_output=True,
                )

                cmd = [
                    "ffmpeg",
                    "-y",
                    "-loop",
                    "1",
                    "-i",
                    str(temp_scaled),
                    "-t",
                    str(scene_duration),
                    "-vf",
                    "zoompan=z='min(zoom+0.0015,1.5)':d=125:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920",
                    "-c:v",
                    "libx264",
                    "-pix_fmt",
                    "yuv420p",
                    "-r",
                    "30",
                    str(clip_raw),
                ]
                res = subprocess.run(cmd, capture_output=True, text=True)
                if res.returncode != 0:
                    print(f"❌ FFMPEG Animation Failed: {res.stderr}")
                    subprocess.run(["ffmpeg", "-y", "-loop", "1", "-i", str(temp_scaled), "-t", str(scene_duration), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", str(clip_raw)], capture_output=True)
                success = True

        # A) Pexels (Stock Video)
        if not success and pexels_key and fetch_pexels_video(keyword, clip_raw, pexels_key):
            success = True

        # B) AI Image Generation (ComfyUI Local SDXL -> Imagen 4)
        img_path = OUTPUT_DIR / f"{output_name}_gen_{i}.png"
        if not success:
            if img_path.exists():
                print(f"🎨 Found existing Initial Image for scene {i}, reusing...")
                success_image = True
            else:
                print(f"🎨 Generating Initial Image for scene {i}...")
                from src.video import comfyui_client
                if comfyui_client.generate_image_sdxl(keyword + " cinematic, high detail, 8k", str(img_path)):
                    success_image = True
                elif generate_image_imagen4(keyword + " cinematic, high detail, 8k", img_path):
                    print(f"⚠️ ComfyUI Failed. Fallback to Imagen 4.")
                    success_image = True
                else:
                    success_image = False

        # C) AI Video Generation (ComfyUI Local SVD -> Luma / Runway / Kling) from Image
        if not success and success_image and ai_video_enabled:
            vid_path = OUTPUT_DIR / f"ai_video_scene_{i}.mp4"
            print(f"🎬 Generating AI Video via ComfyUI SVD for scene {i} using generated image...")
            from src.video import comfyui_client
            if comfyui_client.generate_video_svd(str(img_path), str(vid_path)):
                shutil.copy2(vid_path, clip_raw)
                success = True
                print(f"✅ AI Video Success (ComfyUI SVD) for scene {i}!")
            else:
                print(f"⚠️ ComfyUI SVD failed. Falling back to {video_provider.upper()}...")
                vid_path_fallback = vid_gen.generate_video(
                    prompt=keyword, 
                    output_path=OUTPUT_DIR / f"ai_video_scene_{i}_fallback.mp4", 
                    duration=5,
                    image_path=img_path
                )
                if vid_path_fallback and Path(vid_path_fallback).exists():
                    shutil.copy2(vid_path_fallback, clip_raw)
                    success = True
                    print(f"✅ AI Video Success ({video_provider.upper()}) for scene {i}!")
                else:
                    print(f"⚠️ AI Video failed or API key missing. Falling back to Image/Zoom.")

        # D) Fallback: Animate Image (Zoom) if video failed
        if not success and success_image:
            print(f"🎬 Animating image for scene {i} (Video Generation Failed/Disabled)...")
            from src.video.cinematic_animator import generate_cinematic_animation
            success = generate_cinematic_animation(img_path, clip_raw, scene_duration, FPS)

        # D) FINAL FAILSAFE: Generic Cinematic Video (No more stubs!)
        if not success:
            print(f"⚠️ Heavy Failsafe: Fetching random cinematic video for scene {i}")
            failsafe_keywords = [
                "galaxy space",
                "ocean waves cinematic",
                "forest aerial view",
                "urban city night",
            ]
            fetch_pexels_video(random.choice(failsafe_keywords), clip_raw, pexels_key)
            success = True

        # Normalize clip to 1080x1920, exact duration, and 30fps
        cmd_norm = [
            "ffmpeg",
            "-y",
            "-i",
            str(clip_raw),
            "-t",
            str(scene_duration),
            "-vf",
            ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-r",
            "30",
            "-an",
            str(clip_final),
        ]
        subprocess.run(cmd_norm, capture_output=True, check=False)
        return clip_final

    import concurrent.futures
    clips_array = [None] * len(scenes)
    print("🚀 Starting parallel scene processing with 3 workers...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(process_scene, i, scene): i for i, scene in enumerate(scenes)}
        for future in concurrent.futures.as_completed(futures):
            idx = futures[future]
            try:
                clips_array[idx] = future.result()
                print(f"✅ Scene {idx + 1} processing complete.")
            except Exception as e:
                import traceback
                print(f"❌ Scene {idx + 1} failed: {e}")
                traceback.print_exc()
                clips_array[idx] = None
    
    clips = [c for c in clips_array if c is not None]

    # 4. CONCAT & MIX
    concat_list = OUTPUT_DIR / f"{output_name}_concat.txt"
    with open(concat_list, "w") as f:
        for clip in clips:
            f.write(f"file '{clip.absolute()}'\n")

    video_no_audio = OUTPUT_DIR / f"{output_name}_video.mp4"
    final_video = OUTPUT_DIR / f"{output_name}_final.mp4"

    # Concat clips
    print(f"🎞️ Concatenating {len(clips)} segments...")
    subprocess.run(
        [
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
        ],
        capture_output=True,
        check=True,
    )

    # Merge audio and video
    if audio_path.exists():
        print("🔊 Mixing Audio and Video...")
        # Use -filter_complex for better merging if needed, or simple mix
        subprocess.run(
            [
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
                "-shortest",
                "-movflags",
                "+faststart",
                str(final_video),
            ],
            capture_output=True,
            check=True,
        )
    else:
        print("⚠️ No audio found, renaming video_no_audio to final...")
        video_no_audio.rename(final_video)

    print(f"✨ DONE: {final_video}")

    # 5. PREVIEW & NOTIFY
    # upload_to_gcs(final_video, GCS_BUCKET) # Disabled upload for now as requested
    
    # Открываем видео для предпросмотра на Mac
    print("🎬 Opening Preview...")
    if sys.platform == "darwin":
        subprocess.run(["open", str(final_video)])
    elif sys.platform == "win32":
        os.startfile(str(final_video))
    
    return final_video


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            run_advanced_pipeline(sys.argv[1], output_name="cli_test")
        else:
            print("No arguments provided. Usage: python orchestrator_v4_advanced.py \"Your script text here\"")
    except Exception as e:
        import traceback
        print(f"❌ Фатальная ошибка в оркестраторе: {e}")
        traceback.print_exc()
    finally:
        input("\nНажмите Enter для выхода из оркестратора (чтобы окно не закрылось)...")
