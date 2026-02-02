#!/usr/bin/env python3
"""
Suno AI Unofficial API Client
Uses your Pro subscription through cookies
"""
import logging
import os
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

class SunoAIClient:
    """Unofficial Suno AI client using session cookies."""

    def __init__(self, cookie: Optional[str] = None):
        """
        Initialize Suno client with your session cookie.

        Args:
            cookie: Your Suno session cookie from browser
        """
        self.cookie = cookie or os.getenv("SUNO_COOKIE")
        self.base_url = "https://studio-api.suno.ai"

        if not self.cookie:
            logger.warning("Suno cookie not set. Music generation disabled.")

    def generate_music(
        self,
        prompt: str,
        duration: int = 60,
        instrumental: bool = True,
        genre: str = "electronic",
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Generate music using your Suno Pro subscription.

        Args:
            prompt: Music description (mood + genre)
            duration: Duration in seconds
            instrumental: No vocals if True
            genre: Music genre
            output_path: Where to save MP3

        Returns:
            Path to generated music or None
        """
        if not self.cookie:
            logger.error("Suno cookie not configured")
            return None

        headers = {
            "Cookie": self.cookie,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        # Construct prompt
        full_prompt = f"{prompt}, {genre}, instrumental" if instrumental else f"{prompt}, {genre}"

        payload = {
            "prompt": full_prompt,
            "make_instrumental": instrumental,
            "wait_audio": True
        }

        try:
            logger.info(f"🎵 Suno AI (cookie): {full_prompt[:50]}...")

            # Generate
            response = requests.post(
                f"{self.base_url}/api/generate/v2/",
                json=payload,
                headers=headers,
                timeout=120
            )
            response.raise_for_status()

            result = response.json()

            if not result or len(result) == 0:
                raise ValueError("No music generated")

            # Get first clip
            clip = result[0]
            audio_url = clip.get("audio_url")

            if not audio_url:
                raise ValueError("No audio URL in response")

            # Download
            audio_response = requests.get(audio_url, timeout=60)
            audio_response.raise_for_status()

            if not output_path:
                output_path = Path(f"/tmp/suno_{clip['id']}.mp3")

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(audio_response.content)

            logger.info(f"✅ Suno music saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Suno generation failed: {e}")
            return None


if __name__ == "__main__":
    # Test
    logging.basicConfig(level=logging.INFO)

    # Set your cookie first!
    # SUNO_COOKIE="your_cookie_here"

    client = SunoAIClient()

    track = client.generate_music(
        prompt="upbeat energetic electronic background music",
        duration=30,
        instrumental=True
    )

    if track:
        print(f"Generated: {track}")
