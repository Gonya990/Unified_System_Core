
import os
import sys
import random
import requests
import subprocess
import requests
from pathlib import Path
from dotenv import load_dotenv

# Import NEW Google GenAI SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai library not found.")
    genai = None

# =============================================================================
#                           CONFIGURATION
# =============================================================================

SRC_DIR = Path(__file__).parent.parent.parent.resolve()  # Projects/Content_Factory
ROOT_DIR = SRC_DIR.parent.parent.resolve()              # Unified_System_Core
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR_OVERRIDE", str(SRC_DIR / "outputs")))
INPUT_DIR = SRC_DIR / "inputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(ROOT_DIR / ".env")                   # Root .env
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env")  # AI Core .env

GCS_BUCKET = "content-factory-outputs-435112"

# =============================================================================
#                           AUDIO GENERATION
# =============================================================================

def generate_audio_elevenlabs(text, output_path, api_key):
    """Generate audio using ElevenLabs API (Premium)."""
    print("🎤 Generating ElevenLabs Audio...")
    try:
        if not api_key: return False
        headers = {'xi-api-key': api_key, 'Content-Type': 'application/json'}
        data = {
            'text': text, 
            'model_id': 'eleven_multilingual_v2', 
            'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}
        }
        url = 'https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB'
        resp = requests.post(url, json=data, headers=headers, timeout=60)
        if resp.status_code == 200:
            with open(output_path, 'wb') as f: f.write(resp.content)
            print("✅ ElevenLabs Success!")
            return True
        print(f"❌ ElevenLabs Failed: {resp.status_code}")
        return False
    except Exception as e:
        print(f"❌ ElevenLabs Exception: {e}"); return False

def generate_audio_openai(text, output_path, voice="alloy"):
    """Generate audio using OpenAI TTS."""
    print(f"🎤 Generating OpenAI Audio ({voice})...")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key: return False
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
        response.stream_to_file(output_path)
        print("✅ OpenAI Success!")
        return True
    except Exception as e:
        print(f"❌ OpenAI TTS Error: {e}"); return False

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
    if not api_key: return False
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
        with open(output_path, 'wb') as f:
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
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio="9:16")
        )
        if response.generated_images:
            img = response.generated_images[0]
            with open(output_path, 'wb') as f: f.write(img.image.image_bytes)
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
        if not api_key: return False
        headers = {'Authorization': api_key}
        url = f"https://api.pexels.com/videos/search?query={keyword}&per_page=1&orientation=portrait&size=medium"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get('videos'):
                video_files = data['videos'][0]['video_files']
                best_link = next(
                    (vf['link'] for vf in video_files if vf['width'] >= 720),
                    video_files[0]['link']
                )
                with open(output_path, "wb") as f: 
                    f.write(requests.get(best_link, timeout=30).content)
                print(f"✅ Pexels Success: {keyword}")
                return True
        return False
    except Exception as e:
        print(f"❌ Pexels Exception: {e}"); return False

# =============================================================================
#                           MAIN PIPELINE
# =============================================================================

def run_advanced_pipeline(text: str, lang: str = "ru", output_name: str = "video_v4", scenes: list[dict] = None, style: str = "impact"):
    print(f"\n🚀 Starting ORCHESTRATOR V4.1 (IRONCLAD VISUALS - style={style})")
    
    if not text: return

    # 1. AUDIO
    audio_path = INPUT_DIR / f"{output_name}_audio.wav"
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    
    if not (eleven_key and generate_audio_elevenlabs(text, audio_path, eleven_key)):
        generate_audio_openai(text, audio_path)

    # 2. DURATION
    if not audio_path.exists():
        print(f"⚠️ Audio File NOT found: {audio_path}. Failsafe duration 10s.")
        audio_duration = 10.0
    else:
        try:
            probe = subprocess.check_output([
                "ffprobe", "-v", "error", "-show_entries", "format=duration", 
                "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
            ])
            audio_duration = float(probe.strip())
            print(f"🎵 Audio Duration: {audio_duration}s")
        except Exception as e:
            print(f"⚠️ FFProbe Error: {e}. Defaulting to 10s.")
            audio_duration = 10.0
    
    total_video_duration = audio_duration + 2.0 
    if not scenes: scenes = [{"keyword": "futuristic technology"}]
    scene_duration = total_video_duration / len(scenes)

    # 3. VISUALS
    clips = []
    pexels_key = os.getenv("PEXELS_API_KEY")
    FPS = 30
    
    for i, scene in enumerate(scenes):
        print(f"🎬 Processing Scene {i+1}/{len(scenes)}...")
        keyword = scene.get("keyword", "abstract futuristic")
        clip_final = OUTPUT_DIR / f"{output_name}_seg_{i}.mp4"
        clip_raw = OUTPUT_DIR / f"{output_name}_raw_seg_{i}.mp4"
        
        success = False
        
        # A) Pexels (Stock Video)
        if pexels_key and fetch_pexels_video(keyword, clip_raw, pexels_key):
            success = True
            
        # B) AI Image Gen (Imagen 4 -> DALL-E 3)
        if not success:
            img_path = OUTPUT_DIR / f"{output_name}_gen_{i}.png"
            if generate_image_imagen4(keyword + " cinematic, high detail, 8k", img_path):
                # Animate (Zoom) - Calculate d based on scene_duration and FPS
                d_frames = int(scene_duration * FPS)
                zoom_speed = 0.0015
                cmd = [
                    "ffmpeg", "-y", "-loop", "1", "-i", str(img_path), 
                    "-t", str(scene_duration),
                    "-vf", (
                        f"scale=-1:1920,zoompan=z='min(zoom+{zoom_speed},1.5)':"
                        f"d={d_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':"
                        f"s=1080x1920,fps={FPS}"
                    ),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(FPS), str(clip_raw)
                ]
                subprocess.run(cmd, capture_output=True, check=False)
                success = True
        
        # C) FINAL FAILSAFE: Generic Cinematic Video (No more stubs!)
        if not success:
            print(f"⚠️ Heavy Failsafe: Fetching random cinematic video for scene {i}")
            failsafe_keywords = [
                "galaxy space", "ocean waves cinematic", 
                "forest aerial view", "urban city night"
            ]
            fetch_pexels_video(random.choice(failsafe_keywords), clip_raw, pexels_key)
            success = True 

        # Normalize clip to 1080x1920, exact duration, and 30fps
        cmd_norm = [
            "ffmpeg", "-y", "-i", str(clip_raw), "-t", str(scene_duration),
            "-vf", (
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920,fps=30"
            ),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-an", str(clip_final)
        ]
        subprocess.run(cmd_norm, capture_output=True, check=False)
        clips.append(clip_final)

    # 4. CONCAT & MIX
    concat_list = OUTPUT_DIR / f"{output_name}_concat.txt"
    with open(concat_list, "w") as f:
        for clip in clips:
            f.write(f"file '{clip.absolute()}'\n")

    video_no_audio = OUTPUT_DIR / f"{output_name}_video.mp4"
    final_video = OUTPUT_DIR / f"{output_name}_final.mp4"

    # Concat clips
    print(f"🎞️ Concatenating {len(clips)} segments...")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_list), 
        "-c", "copy", str(video_no_audio)
    ], capture_output=True, check=True)
    
    # Merge audio and video
    if audio_path.exists():
        print(f"🔊 Mixing Audio and Video...")
        # Use -filter_complex for better merging if needed, or simple mix
        subprocess.run([
            "ffmpeg", "-y", "-i", str(video_no_audio), "-i", str(audio_path),
            "-c:v", "copy", "-c:a", "aac", "-map", "0:v:0", "-map", "1:a:0", 
            "-shortest", "-movflags", "+faststart", str(final_video)
        ], capture_output=True, check=True)
    else:
        print("⚠️ No audio found, renaming video_no_audio to final...")
        video_no_audio.rename(final_video)

    print(f"✨ DONE: {final_video}")

    # 5. UPLOAD & NOTIFY
    upload_to_gcs(final_video, GCS_BUCKET)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_advanced_pipeline(sys.argv[1], output_name="cli_test")

