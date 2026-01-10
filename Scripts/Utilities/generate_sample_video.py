
import os
import sys
import asyncio
from pathlib import Path

# Add project root to path
sys.path.append(os.getcwd())

from Scripts.Utilities.token_broker import TokenBroker
from openai import OpenAI

async def generate_sample():
    print("🚀 Starting 3-Language Sample Generation...")
    
    desktop_path = Path(os.path.expanduser("~/Desktop"))
    output_file = desktop_path / "Unified_Sample_3Lang.mp4"
    
    broker = TokenBroker()
    openai_key = broker.get_key("openai", tier="paid")
    if not openai_key:
        print("❌ No OpenAI key found!")
        return

    client = OpenAI(api_key=openai_key)
    
    # Content Plan
    segments = [
        {
            "lang": "en",
            "text": "Welcome to the Unified System. We are operating at 120 percent capacity.",
            "voice": "onyx",
            "prompt": "Futuristic AI dashboard, hologram interface, blue and cyan neon, cinematic lighting, 8k"
        },
        {
            "lang": "he",
            "text": "המערכת פועלת כעת באופן אוטונומי מלא. כל המערכות תקינות.", # System operating autonomously...
            "voice": "onyx", # Onyx speaks Hebrew reasonably well
            "prompt": "High tech server room, cyber security concept, glowing hebrew letters in data stream, matrix style, 8k"
        },
        {
            "lang": "ru",
            "text": "Система синхронизирована. Мы готовы к запуску. Газ сто двадцать процентов.",
            "voice": "onyx",
            "prompt": "Russian futuristic city cyberpunk, dark atmosphere, red and white lights, cinematic, hyperrealistic"
        }
    ]
    
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        print(f"📂 Working in {temp_path}")
        
        clips = []
        
        from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate_videoclips
        
        for i, seg in enumerate(segments):
            print(f"🎬 Processing Segment {i+1} ({seg['lang']})...")
            
            # 1. Audio
            audio_path = temp_path / f"voice_{i}.mp3"
            response = client.audio.speech.create(
                model="tts-1",
                voice=seg['voice'],
                input=seg['text']
            )
            response.stream_to_file(audio_path)
            
            # 2. Image
            img_path = temp_path / f"image_{i}.png"
            print(f"🎨 Generating Image {i+1}...")
            try:
                img_res = client.images.generate(
                    model="dall-e-3",
                    prompt=seg['prompt'],
                    size="1024x1024",
                    quality="standard",
                    n=1
                )
                import requests
                img_data = requests.get(img_res.data[0].url).content
                with open(img_path, 'wb') as f:
                    f.write(img_data)
            except Exception as e:
                print(f"❌ Image failed: {e}")
                # Create dummy image
                from PIL import Image
                img = Image.new('RGB', (1024, 1024), color = 'black')
                img.save(img_path)

            # 3. Clip Assembly
            audio_clip = AudioFileClip(str(audio_path))
            duration = audio_clip.duration + 0.5
            
            img_clip = ImageClip(str(img_path)).set_duration(duration)
            
            # Subtitles (simple TextClip for now, requires ImageMagick)
            # We'll skip complex subtitles to ensure it runs on Mac without brew install imagemagick issues if possible
            # Or try basic
            
            try:
                txt_clip = TextClip(seg['text'], fontsize=50, color='white', font='Arial', method='caption', size=(1000, None))
                txt_clip = txt_clip.set_position(('center', 'bottom')).set_duration(duration)
                video_clip = CompositeVideoClip([img_clip, txt_clip])
            except Exception as e:
                print(f"Warning: TextClip failed ({e}), skipping subs")
                video_clip = img_clip
            
            video_clip = video_clip.set_audio(audio_clip)
            clips.append(video_clip)
            
        print("🎞️ Concatenating final video...")
        final = concatenate_videoclips(clips)
        final.write_videofile(str(output_file), fps=24)
        
    print(f"✅ Video saved to: {output_file}")

if __name__ == "__main__":
    asyncio.run(generate_sample())
