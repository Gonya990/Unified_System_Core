#!/usr/bin/env python3
"""
YouTube Thumbnail Generator — UnifiedCore Content Factory
Generates clickable thumbnails using DALL-E 3 / Gemini Imagen
and overlays text with Pillow for brand consistency.
"""

import os
import sys
import textwrap
from io import BytesIO
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Setup paths
PIPELINE_DIR = Path(__file__).parent.resolve()
SRC_DIR = PIPELINE_DIR.parent
FACTORY_DIR = SRC_DIR.parent
ROOT_DIR = FACTORY_DIR.parent.parent

load_dotenv(FACTORY_DIR / ".env")
load_dotenv(ROOT_DIR / "Projects/AI_Core/.env", override=False)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Brand colors (Megaforma palette)
BRAND = {
    "bg_dark": (10, 10, 20),           # Deep space black
    "accent_purple": (138, 43, 226),   # Electric purple
    "accent_cyan": (0, 220, 255),      # Neon cyan
    "text_white": (255, 255, 255),
    "text_yellow": (255, 220, 0),      # Highlight yellow
    "gradient_start": (20, 0, 50),
    "gradient_end": (0, 50, 80),
}

# Thumbnail sizes
SIZES = {
    "longform": (1280, 720),    # Standard YouTube thumbnail
    "shorts": (1080, 1920),     # YouTube Shorts thumbnail
}


def _generate_bg_image_dalle(prompt: str, size: tuple) -> Optional[bytes]:
    """Generate background image using DALL-E 3."""
    try:
        import requests
        dalle_size = "1792x1024" if size[0] > size[1] else "1024x1792"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": dalle_size,
            "quality": "hd",
            "n": 1,
        }
        r = requests.post("https://api.openai.com/v1/images/generations",
                          headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        img_url = r.json()["data"][0]["url"]

        # Download image
        img_r = requests.get(img_url, timeout=30)
        img_r.raise_for_status()
        return img_r.content
    except Exception as e:
        print(f"⚠️ DALL-E thumbnail failed: {e}")
        return None


def _create_gradient_bg(size: tuple, style: str = "tech") -> "Image":
    """Create a gradient background as fallback."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return None

    img = Image.new("RGB", size, BRAND["bg_dark"])
    draw = ImageDraw.Draw(img)

    # Draw gradient rectangles
    w, h = size
    for i in range(h):
        ratio = i / h
        r = int(BRAND["gradient_start"][0] * (1 - ratio) + BRAND["gradient_end"][0] * ratio)
        g = int(BRAND["gradient_start"][1] * (1 - ratio) + BRAND["gradient_end"][1] * ratio)
        b = int(BRAND["gradient_start"][2] * (1 - ratio) + BRAND["gradient_end"][2] * ratio)
        draw.line([(0, i), (w, i)], fill=(r, g, b))

    # Add grid lines (tech aesthetic)
    for x in range(0, w, w // 12):
        draw.line([(x, 0), (x, h)], fill=(30, 30, 60), width=1)
    for y in range(0, h, h // 8):
        draw.line([(0, y), (w, y)], fill=(30, 30, 60), width=1)

    # Add accent corner glow
    for r_size in range(200, 0, -10):
        alpha = int(80 * (1 - r_size / 200))
        draw.ellipse(
            [w - r_size, -r_size // 2, w + r_size // 2, r_size],
            fill=(*BRAND["accent_purple"], alpha) if len(BRAND["accent_purple"]) == 3 else BRAND["accent_purple"]
        )

    return img


def _add_text_overlay(img, title: str, subtitle: str = "", thumbnail_type: str = "longform") -> "Image":
    """Add text overlay with brand styling."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("⚠️ Pillow not installed. Install with: pip install Pillow")
        return img

    draw = ImageDraw.Draw(img, "RGBA")
    w, h = img.size

    # Try to load system fonts
    font_paths = [
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/System/Library/Fonts/SFPro-Display-Black.otf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/Library/Fonts/Arial Bold.ttf",
    ]

    def get_font(size: int):
        for fp in font_paths:
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
        return ImageFont.load_default()

    if thumbnail_type == "shorts":
        title_size = 90
        subtitle_size = 50
        title_y = h * 0.55
        padding = 60
    else:
        title_size = 72
        subtitle_size = 38
        title_y = h * 0.55
        padding = 60

    title_font = get_font(title_size)
    subtitle_font = get_font(subtitle_size)

    # Wrap title
    max_chars = 20 if thumbnail_type == "shorts" else 28
    wrapped = textwrap.wrap(title, width=max_chars)[:3]

    # Draw dark overlay behind text for readability
    overlay_top = int(title_y) - 30
    overlay_bottom = min(h - 20, int(title_y) + title_size * (len(wrapped) + 1) + 60)
    draw.rectangle(
        [(0, overlay_top), (w, overlay_bottom)],
        fill=(0, 0, 0, 160)
    )

    # Draw accent left bar
    draw.rectangle(
        [(padding - 15, overlay_top + 10), (padding - 5, overlay_bottom - 10)],
        fill=BRAND["accent_cyan"]
    )

    # Draw title lines
    y = int(title_y)
    for i, line in enumerate(wrapped):
        # Shadow
        draw.text((padding + 4, y + 4), line, font=title_font, fill=(0, 0, 0, 200))
        # Main text (alternating colors for visual interest)
        color = BRAND["text_yellow"] if i == 0 else BRAND["text_white"]
        draw.text((padding, y), line, font=title_font, fill=color)
        y += title_size + 8

    # Draw subtitle
    if subtitle:
        draw.text((padding, y + 10), subtitle[:50], font=subtitle_font,
                  fill=BRAND["accent_cyan"])

    # Channel watermark
    channel_font = get_font(28)
    watermark = "MEGAFORMA"
    draw.text((w - 200, 20), watermark, font=channel_font, fill=(255, 255, 255, 180))

    return img


def generate_thumbnail(
    title: str,
    topic: str,
    output_path: Path,
    thumbnail_type: str = "longform",  # "longform" | "shorts"
    subtitle: str = "",
    use_ai_bg: bool = True,
) -> Optional[Path]:
    """
    Generate a YouTube thumbnail.
    Returns path to generated thumbnail or None on failure.
    """
    try:
        from PIL import Image
    except ImportError:
        print("❌ Pillow not installed. Run: pip install Pillow")
        return None

    size = SIZES.get(thumbnail_type, SIZES["longform"])
    print(f"🖼️  Generating {thumbnail_type} thumbnail ({size[0]}x{size[1]})...")

    img = None

    # 1. Try AI background
    if use_ai_bg and OPENAI_API_KEY:
        dalle_prompt = (
            f"Cinematic, dramatic thumbnail background for YouTube video about: {topic}. "
            f"Dark, moody, futuristic aesthetic. Deep purple and cyan neon accents. "
            f"NO TEXT. Professional, high quality. Megaforma tech channel style."
        )
        print("  🎨 Generating AI background (DALL-E)...")
        bg_bytes = _generate_bg_image_dalle(dalle_prompt, size)

        if bg_bytes:
            img = Image.open(BytesIO(bg_bytes)).convert("RGB")
            img = img.resize(size, Image.LANCZOS)
            print("  ✅ AI background ready")

    # 2. Fallback: gradient background
    if img is None:
        print("  📐 Using gradient background...")
        img = _create_gradient_bg(size)

    if img is None:
        img = Image.new("RGB", size, BRAND["bg_dark"])

    # 3. Add text overlay
    img = _add_text_overlay(img, title, subtitle=subtitle, thumbnail_type=thumbnail_type)

    # 4. Save
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save as JPEG for smaller size (YouTube max 2MB)
    img.save(str(output_path), "JPEG", quality=92, optimize=True)
    size_kb = output_path.stat().st_size // 1024
    print(f"  💾 Saved: {output_path} ({size_kb}KB)")

    return output_path


def generate_thumbnail_pair(
    title: str,
    topic: str,
    output_dir: Path,
    use_ai_bg: bool = True,
) -> dict:
    """Generate both Long-form and Shorts thumbnails."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(c for c in title[:30] if c.isalnum() or c in " -").strip().replace(" ", "_")

    result = {}

    # Long-form thumbnail
    lf_path = output_dir / f"{safe_name}_thumbnail_lf.jpg"
    lf_result = generate_thumbnail(title, topic, lf_path, "longform", use_ai_bg=use_ai_bg)
    if lf_result:
        result["longform"] = lf_result

    # Shorts thumbnail (cheaper - no AI BG)
    sh_path = output_dir / f"{safe_name}_thumbnail_shorts.jpg"
    sh_result = generate_thumbnail(title, topic, sh_path, "shorts", use_ai_bg=False)
    if sh_result:
        result["shorts"] = sh_result

    return result


# ─────────────────────────────────────────────
#  CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="YouTube Thumbnail Generator")
    parser.add_argument("--title", required=True)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--output", default="/tmp/thumbnail.jpg")
    parser.add_argument("--type", default="longform", choices=["longform", "shorts"])
    parser.add_argument("--no-ai", action="store_true", help="Skip AI background generation")
    args = parser.parse_args()

    result = generate_thumbnail(
        title=args.title,
        topic=args.topic,
        output_path=Path(args.output),
        thumbnail_type=args.type,
        use_ai_bg=not args.no_ai,
    )
    if result:
        print(f"\n✅ Thumbnail ready: {result}")
    else:
        print("❌ Thumbnail generation failed")
