
import asyncio
import os
import random
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from Scripts.Utilities.token_broker import TokenBroker

# Try to import edge-tts
try:
    import edge_tts
except ImportError:
    print("❌ edge-tts not installed. Run: pip install edge-tts")
    sys.exit(1)

async def generate_sample():
    print("🚀 Starting 3-Language Sample Generation (FREE TIER MODE)...")

    desktop_path = Path(os.path.expanduser("~/Desktop"))
    output_file = desktop_path / "Unified_Sample_3Lang_Free.mp4"

    broker = TokenBroker()
    pexels_key = broker.get_key("pexels")
    if not pexels_key:
        print("⚠️ No Pexels key found. Will use color backgrounds.")

    # Content Plan (Edge TTS Voices)
    segments = [
        {
            "lang": "en",
            "text": "Welcome to the Unified System. We are operating at 120 percent capacity.",
            "voice": "en-US-ChristopherNeural",
            "query": "technology"
        },
        {
            "lang": "he",
            "text": "המערכת פועלת כעת באופן אוטונומי מלא. כל המערכות תקינות.",
            "voice": "he-IL-AvriNeural",
            "query": "cyber"
        },
        {
            "lang": "ru",
            "text": "Система синхронизирована. Мы готовы к запуску. Газ сто двадцать процентов.",
            "voice": "ru-RU-DmitryNeural",
            "query": "future city"
        }
    ]

    import tempfile

    import requests
    from PIL import Image
    if not hasattr(Image, 'ANTIALIAS'):
        Image.ANTIALIAS = Image.LANCZOS

    from moviepy.editor import AudioFileClip, ColorClip, ImageClip, concatenate_videoclips

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"📂 Working in {temp_path}")

        clips = []

        for i, seg in enumerate(segments):
            print(f"🎬 Processing Segment {i+1} ({seg['lang']})...")

            # 1. Audio (Edge TTS)
            audio_path = temp_path / f"voice_{i}.mp3"
            communicate = edge_tts.Communicate(seg['text'], seg['voice'])
            await communicate.save(str(audio_path))

            # 2. Image (Pexels or Color)
            img_path = temp_path / f"image_{i}.jpg"
            found_image = False

            if pexels_key:
                try:
                    print(f"🔍 Searching Pexels for '{seg['query']}'...")
                    headers = {"Authorization": pexels_key}
                    url = f"https://api.pexels.com/v1/search?query={seg['query']}&per_page=1&orientation=landscape"
                    res = requests.get(url, headers=headers, timeout=5)
                    if res.status_code == 200:
                        data = res.json()
                        if data['photos']:
                            img_url = data['photos'][0]['src']['large']
                            img_data = requests.get(img_url).content
                            with open(img_path, 'wb') as f:
                                f.write(img_data)
                            found_image = True
                except Exception as e:
                    print(f"⚠️ Pexels error: {e}")

            # 3. Clip Assembly
            audio_clip = AudioFileClip(str(audio_path))
            duration = audio_clip.duration + 0.5

            if found_image:
                video_clip = ImageClip(str(img_path)).set_duration(duration)
            else:
                # Fallback Color
                color = (random.randint(0,50), random.randint(0,50), random.randint(50,150))
                video_clip = ColorClip(size=(1280, 720), color=color).set_duration(duration)

            # Subtitles (simple logic)
            # Try to add text, if fails return clean clip
            try:
                # Basic text placement
                # Note: moviepy TextClip usually requires ImageMagick. If failing, we skip.
                # Use a specific valid font if possible, or None to let it find one.
                # Hebrew might need special font handling.
                pass
            except:
                pass

            video_clip = video_clip.set_audio(audio_clip)
            video_clip = video_clip.resize(width=1280) # Ensure size consistency
            clips.append(video_clip)

        print("🎞️ Concatenating final video...")
        final = concatenate_videoclips(clips, method="compose")
        final.write_videofile(str(output_file), fps=24)

    print(f"✅ Video saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(generate_sample())
