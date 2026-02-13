import os
import random
import subprocess
import time
from pathlib import Path

from dotenv import load_dotenv

# Try to import GenAI (Optional)
try:
    import google.generativeai as genai
except ImportError:
    pass

# Internal imports (TokenBroker)
try:
    from src.security.token_broker_v2 import TokenBroker as TokenBroker
except ImportError:

    class TokenBroker:
        @staticmethod
        def get_token(name):
            return os.getenv(name)


ROOT_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR_OVERRIDE", str(ROOT_DIR / "outputs")))
INPUT_DIR = ROOT_DIR / "inputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
INPUT_DIR.mkdir(parents=True, exist_ok=True)

# Voices
VOICE_RU = "ru-RU-DmitryNeural"
VOICE_EN = "en-US-ChristopherNeural"


def generate_audio_elevenlabs(text, output_path, api_key):
    print("🎤 Generating ElevenLabs Audio...")
    try:
        import requests

        if not api_key:
            return False
        headers = {"xi-api-key": api_key, "Content-Type": "application/json"}
        data = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.5, "similarity_boost": 0.75},
        }
        # Adam Voice ID or other
        url = "https://api.elevenlabs.io/v1/text-to-speech/pNInz6obpgDQGcFmaJgB"
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print("✅ ElevenLabs Success!")
            return True
        else:
            print(f"❌ ElevenLabs Error: {response.text}")
            return False
    except Exception as e:
        print(f"❌ ElevenLabs Exception: {e}")
        return False


def generate_audio_edge(text: str, output_path: Path, voice: str) -> bool:
    print(f"🎤 Generating Enhanced Edge-TTS Audio (voice={voice})...")
    import asyncio

    import edge_tts

    async def _gen():
        tts = edge_tts.Communicate(text, voice)
        await tts.save(str(output_path))

    try:
        asyncio.run(_gen())
        if output_path.exists() and output_path.stat().st_size > 1000:
            return True
        return False
    except Exception as e:
        print(f"❌ Edge-TTS Error: {e}")
        return False


def generate_audio_openai(text: str, output_path: Path, voice: str = "alloy") -> bool:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️ OpenAI Key not found, skipping OpenAI TTS")
        return False
    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.audio.speech.create(model="tts-1", voice=voice, input=text)
        response.stream_to_file(output_path)
        return True
    except Exception as e:
        print(f"❌ OpenAI TTS Error: {e}")
        return False


def run_no_face_pipeline(
    text: str,
    lang: str = "ru",
    output_name: str = "no_face_video",
    scenes: list[dict] = None,
    style: str = "impact",
):
    # Load ENV again to be sure
    load_dotenv(ROOT_DIR / ".env")

    print(f"\n🚀 Starting ENHANCED NO-FACE Pipeline (lang={lang}, style={style})")

    # 1. Generate Audio
    audio_path = INPUT_DIR / f"{output_name}_audio.wav"

    # Try ElevenLabs FIRST (Premium)
    eleven_key = os.getenv("ELEVENLABS_API_KEY")
    audio_generated = False

    if eleven_key:
        if generate_audio_elevenlabs(text, audio_path, eleven_key):
            audio_generated = True

    if not audio_generated:
        print("⚠️ Falling back to OpenAI/Edge-TTS...")
        # Try OpenAI
        if not generate_audio_openai(text, audio_path, voice="onyx" if lang == "en" else "alloy"):
            # Fallback to Edge
            voice = VOICE_RU if lang == "ru" else VOICE_EN
            if not generate_audio_edge(text, audio_path, voice):
                print("❌ All audio generation failed.")
                return

    print(f"✅ Audio Ready: {audio_path}")

    # 2. Analyze Audio Duration
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
        total_duration = float(probe.strip())
    except Exception:
        total_duration = 10.0  # fallback

    scene_count = len(scenes) if scenes else 1
    SCENE_DURATION = total_duration / scene_count
    print(f"⏱️ Scene Duration: {SCENE_DURATION:.2f}s (Total: {total_duration:.2f}s)")

    # 3. Prepare Clips
    clips: list[Path] = []

    # Pexels Key
    pexels_key = os.getenv("PEXELS_API_KEY")
    if not pexels_key:
        print("⚠️ Warn: PEXELS_API_KEY Missing")

    for i, scene in enumerate(scenes or []):
        print(f"🎬 Processing Scene {i}...")
        time.sleep(1)

        keyword = scene.get("keyword", "abstract")
        image_path = scene.get("image")

        clip_name = f"{output_name}_raw_seg_{i}.mp4"
        clip_out = OUTPUT_DIR / clip_name

        # A) Use Static Image provided in scenes
        if image_path and os.path.exists(image_path):
            print(f"✅ Using provided image: {image_path}")
            # convert image to video
            cmd = [
                "ffmpeg",
                "-y",
                "-loop",
                "1",
                "-i",
                str(image_path),
                "-t",
                str(SCENE_DURATION),
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-pix_fmt",
                "yuv420p",
                "-c:v",
                "libx264",
                "-r",
                "30",
                str(clip_out),
            ]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                clips.append(clip_out)
                continue
            except Exception as e:
                print(f"❌ FFmpeg error: {e}")

        # B) Try Pexels (Video B-Roll)
        success = False
        if pexels_key:
            print(f"🔍 Searching Pexels for: {keyword}...")
            try:
                import requests

                headers = {"Authorization": pexels_key}
                # Request 1 video, portrait, medium size
                url = (
                    f"https://api.pexels.com/videos/search?query={keyword}&per_page=1&orientation=portrait&size=medium"
                )
                resp = requests.get(url, headers=headers)

                if resp.status_code == 200 and resp.json().get("videos"):
                    video_files = resp.json()["videos"][0]["video_files"]
                    # Find best match for 1080x1920 or closest
                    # Simple strategy: take first
                    video_url = video_files[0]["link"]

                    print(f"⬇️ Downloading Pexels Clip: {video_url}")
                    v_resp = requests.get(video_url)
                    with open(clip_out, "wb") as f:
                        f.write(v_resp.content)
                    success = True
                else:
                    print(f"⚠️ Pexels not found or API error: {resp.status_code}")
                    if resp.status_code == 401:
                        print("❌ Pexels Unauthorized (Check Key!)")
            except Exception as e:
                print(f"❌ Pexels Exception: {e}")

        if success:
            # Resize/Crop downloaded clip to 1080x1920 just in case
            processed_clip = OUTPUT_DIR / f"{output_name}_proc_seg_{i}.mp4"
            cmd = [
                "ffmpeg",
                "-y",
                "-i",
                str(clip_out),
                "-t",
                str(SCENE_DURATION),
                "-vf",
                "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
                "-c:v",
                "libx264",
                "-c:a",
                "none",
                str(processed_clip),
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            clips.append(processed_clip)
            continue

        # C) FALLBACK: Colored Placeholder
        print(f"🎨 Generating fallback B-Roll for scene {i}")
        color = random.choice(["blue", "red", "green", "purple", "orange", "black"])
        cmd = [
            "ffmpeg",
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={color}:s=1080x1920:d={SCENE_DURATION}",
            "-vf",
            f"drawtext=text='Scene {i} - {keyword}':fontcolor=white:fontsize=64:x=(w-text_w)/2:y=(h-text_h)/2",
            "-pix_fmt",
            "yuv420p",
            "-c:v",
            "libx264",
            "-r",
            "30",
            str(clip_out),
        ]
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            clips.append(clip_out)
        except Exception as e:
            print(f"❌ Fallback generation failed: {e}")

    print(f"✅ Prepared {len(clips)} clips")

    # 4. Concat Clips
    concat_list_path = OUTPUT_DIR / f"{output_name}_concat.txt"
    with open(concat_list_path, "w") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    raw_video = OUTPUT_DIR / f"{output_name}_raw.mp4"
    print("🎬 Concatenating...")

    cmd_concat = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list_path),
        "-c",
        "copy",
        str(raw_video),
    ]
    try:
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    except Exception:
        print("❌ Concat failed.")
        return

    # 5. Final Mix (Audio + Video)
    final_video = OUTPUT_DIR / f"{output_name}_final.mp4"
    print("🔊 Mixing Final Audio...")

    cmd_mix = [
        "ffmpeg",
        "-y",
        "-i",
        str(raw_video),
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
        str(final_video),
    ]
    try:
        subprocess.run(cmd_mix, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        print(f"\n✨ DONE: {final_video}")
    except Exception:
        print("❌ Final mix failed.")
