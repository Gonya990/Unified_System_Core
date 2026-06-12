import subprocess
import random
from pathlib import Path

def generate_cinematic_animation(image_path: Path, output_path: Path, duration: float, fps: int = 30) -> bool:
    """
    Creates a highly cinematic pseudo-video from a static image using advanced FFmpeg filters.
    Includes subtle Ken Burns effects (zoom + pan) tailored to the image dimensions.
    """
    try:
        frames = int(duration * fps)
        
        # Determine random effect
        effect = random.choice([
            "zoom_in_center",
            "zoom_in_top",
            "pan_right_slow",
            "pan_left_slow",
            "zoom_out_center"
        ])
        
        # Default fallback values
        z_expr = "1.0"
        x_expr = "0"
        y_expr = "0"
        
        if effect == "zoom_in_center":
            z_expr = "min(zoom+0.0015,1.5)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif effect == "zoom_out_center":
            # Start at 1.3, zoom out slowly
            z_expr = "max(1.3-0.0015*in, 1.0)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif effect == "pan_right_slow":
            z_expr = "1.2"
            x_expr = "x+1"
            y_expr = "ih/2-(ih/zoom/2)"
        elif effect == "pan_left_slow":
            z_expr = "1.2"
            x_expr = "max(iw-1-x,0)"
            y_expr = "ih/2-(ih/zoom/2)"
        elif effect == "zoom_in_top":
            z_expr = "min(zoom+0.0015,1.5)"
            x_expr = "iw/2-(iw/zoom/2)"
            y_expr = "0"
            
        print(f"🎬 Applying Cinematic Effect [{effect}] to {image_path.name}")
        
        cmd = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-t", str(duration),
            "-vf", 
            (
                f"scale=-1:1920,zoompan=z='{z_expr}':"
                f"d={frames}:x='{x_expr}':y='{y_expr}':"
                f"s=1080x1920,fps={fps}"
            ),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", str(fps),
            str(output_path),
        ]
        
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"❌ Cinematic Animation failed: {res.stderr}")
            return False
            
        return True
    except Exception as e:
        print(f"❌ Exception in cinematic animation: {e}")
        return False
