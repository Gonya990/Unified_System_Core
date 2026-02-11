import os
import random
from pathlib import Path
import PIL.Image

if not hasattr(PIL.Image, 'ANTIALIAS'):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from moviepy.editor import ImageClip, CompositeVideoClip

# Paths
CURRENT_DIR = Path(__file__).resolve().parent
CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
AVATARS_DIR = CURRENT_DIR / "assets"
VIDEO_DIR = CONTEXT_DIR / "video_clips"

if not VIDEO_DIR.exists():
    VIDEO_DIR.mkdir(parents=True, exist_ok=True)

def create_directed_clip(image_path, output_path, duration=10.0, shot_type="medium"):
    """
    Creates a video clip from an image with dynamic movement based on shot type.
    """
    print(f"🎬 Generating {shot_type} motion clip for: {image_path.name}")
    
    # Load image
    clip = ImageClip(str(image_path)).set_duration(duration)
    w, h = clip.size

    # Define Crops and Zooms for "Director's Cut"
    if shot_type == "close":
        # 2x Zoom, focus on head
        zoom_start, zoom_end = 1.8, 2.0
    elif shot_type == "medium":
        # 1.3x Zoom
        zoom_start, zoom_end = 1.2, 1.4
    else: # wide
        # Subtle zoom
        zoom_start, zoom_end = 1.0, 1.1

    def resize_func(t):
        # Linear interpolation of zoom
        return zoom_start + (zoom_end - zoom_start) * (t / duration)

    # Apply Zoom and subtle rotation/pan for "premium" feel
    clip = clip.resize(resize_func)
    
    # Center the zoomed image
    final = CompositeVideoClip([clip.set_position("center")], size=(w, h))

    final.write_videofile(
        str(output_path), 
        fps=24, 
        codec="libx264", 
        audio=False,
        preset="medium",
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )
    print(f"✅ Saved directed clip: {output_path.name}")

def generate_angles():
    # Regular Avatars
    avatars = {
        "Rex": AVATARS_DIR / "dino_skeptic.png",
        "Trike": AVATARS_DIR / "dino_enthusiast.png"
    }

    angles = ["wide", "medium", "close"]

    for name, path in avatars.items():
        if not path.exists():
            print(f"⚠️ Avatar not found: {path}")
            continue
            
        for angle in angles:
            output = VIDEO_DIR / f"{name.lower()}_{angle}.mp4"
            create_directed_clip(path, output, duration=10.0, shot_type=angle)

    # B-roll Images (Cinematic Cutaways)
    broll_images = list(AVATARS_DIR.glob("broll_*.png"))
    for broll_path in broll_images:
        print(f"🎬 Found B-roll: {broll_path.name}")
        output = VIDEO_DIR / f"{broll_path.stem}_motion.mp4"
        create_directed_clip(broll_path, output, duration=10.0, shot_type="wide")

if __name__ == "__main__":
    generate_angles()
