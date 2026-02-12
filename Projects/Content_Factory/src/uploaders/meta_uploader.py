#!/usr/bin/env python3
"""
Meta (Instagram/Facebook) Video Uploader
Uses Instagrapi for Instagram, Selenium for Facebook
"""

import os
from pathlib import Path
from typing import Optional

# Try to import instagrapi for Instagram
try:
    from instagrapi import Client

    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False
    print("⚠️ instagrapi not installed. Run: pip install instagrapi")

# Instagram credentials
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME", "")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD", "")


def upload_reel_instagram(
    video_path: Path, caption: str, thumbnail_path: Optional[Path] = None
) -> bool:
    """
    Upload Reel to Instagram using Instagrapi

    Args:
        video_path: Path to video file
        caption: Reel caption
        thumbnail_path: Optional thumbnail image

    Returns:
        True if upload successful
    """
    if not INSTAGRAPI_AVAILABLE:
        print("❌ instagrapi not available")
        return False

    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        print("⚠️ Instagram credentials not set")
        print("Set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD environment variables")
        return False

    if not video_path.exists():
        print(f"❌ Video not found: {video_path}")
        return False

    print(f"📤 Uploading Reel to Instagram: {video_path}")

    try:
        client = Client()
        client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        print("✅ Instagram login successful")

        # Upload as Reel
        media = client.clip_upload(
            video_path, caption=caption, thumbnail=thumbnail_path
        )

        print(f"✅ Reel uploaded! Media ID: {media.pk}")
        return True

    except Exception as e:
        print(f"❌ Instagram upload error: {e}")
        return False


def upload_story_instagram(video_path: Path) -> bool:
    """Upload video as Instagram Story"""
    if not INSTAGRAPI_AVAILABLE:
        print("❌ instagrapi not available")
        return False

    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        print("⚠️ Instagram credentials not set")
        return False

    print(f"📤 Uploading Story to Instagram: {video_path}")

    try:
        client = Client()
        client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

        media = client.video_upload_to_story(video_path)
        print(f"✅ Story uploaded! Media ID: {media.pk}")
        return True

    except Exception as e:
        print(f"❌ Instagram Story error: {e}")
        return False


def upload_facebook_reels(video_path: Path, caption: str) -> bool:
    """
    Upload to Facebook Reels
    Note: Facebook API is more restricted, using Selenium as fallback
    """
    print("⚠️ Facebook Reels upload requires manual setup")
    print("Consider using Meta Business Suite for automated uploads")
    print(f"Video ready for manual upload: {video_path}")
    return False


if __name__ == "__main__":
    # Test upload (requires credentials)
    ROOT_DIR = Path(__file__).parent.resolve()
    test_video = ROOT_DIR / "outputs" / "igor_ru_final.mp4"
    test_caption = """
🤖 AI-Generated Content Demo

Created using:
- LivePortrait (Animation)
- Wav2Lip (Lip Sync)
- Edge-TTS (Voice)
- PyCaps (Subtitles)

#AI #ContentCreation #Automation #Tech
    """.strip()

    if test_video.exists():
        upload_reel_instagram(test_video, test_caption)
    else:
        print(f"Test video not found: {test_video}")
