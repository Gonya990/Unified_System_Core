import sys
from pathlib import Path

# Add project root to path
sys.path.append("/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory")

from src.video import comfyui_client

print("Testing ComfyUI SDXL connection...")
out_img = "/Users/igorgoncharenko/Documents/Unified_System_Core/Projects/Content_Factory/test_sdxl.png"
success = comfyui_client.generate_image_sdxl("A futuristic neon city at night, high quality, 8k", out_img)

if success:
    print(f"Success! Image saved to {out_img}")
else:
    print("Failed to generate image via ComfyUI")
