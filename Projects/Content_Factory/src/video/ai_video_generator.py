#!/usr/bin/env python3
"""
AI Video Generator - B-roll clips using Runway ML Gen-3, Luma AI, Kling
"""

import logging
import os
import time
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

# API Keys
RUNWAY_API_KEY = os.getenv("RUNWAY_API_KEY")
LUMA_API_KEY = os.getenv("LUMA_API_KEY")
KLING_API_KEY = os.getenv("KLING_API_KEY")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "5KikfJFyT75Rlibf2u829q4qZOTm0FVfttKCb5znbJSYqb96qAKarEDY")

RUNWAY_BASE_URL = "https://api.runwayml.com/v1"
LUMA_BASE_URL = "https://api.lumalabs.ai/dream-machine/v1"
KLING_BASE_URL = "https://api.kling.ai/v1"
PEXELS_BASE_URL = "https://api.pexels.com/videos"


class VideoGenerator:
    """Generate AI video clips for B-roll."""

    def __init__(self, provider: str = "runway"):
        """
        Args:
            provider: 'runway', 'luma', 'kling', or 'pexels'
        """
        self.provider = provider.lower()
        self.api_key = None
        self.base_url = None

        if self.provider == "runway" and RUNWAY_API_KEY:
            self.api_key = RUNWAY_API_KEY
            self.base_url = RUNWAY_BASE_URL
        elif self.provider == "luma" and LUMA_API_KEY:
            self.api_key = LUMA_API_KEY
            self.base_url = LUMA_BASE_URL
        elif self.provider == "kling" and KLING_API_KEY:
            self.api_key = KLING_API_KEY
            self.base_url = KLING_BASE_URL
        elif self.provider == "pexels" and PEXELS_API_KEY:
            self.api_key = PEXELS_API_KEY
            self.base_url = PEXELS_BASE_URL
        else:
            if self.provider == "pexels" and not PEXELS_API_KEY:
                logger.error("Pexels API key missing.")
            logger.warning(f"Provider '{provider}' not configured. Video generation disabled.")

    def generate_video(
        self,
        prompt: str,
        duration: int = 4,
        style: str = "realistic",
        output_path: Optional[Path] = None,
    ) -> Optional[Path]:
        """
        Generate AI video clip.

        Args:
            prompt: Text description of the video
            duration: Duration in seconds (4-10s typical)
            style: Visual style (realistic, cinematic, cartoon, anime)
            output_path: Where to save video

        Returns:
            Path to generated video or None if failed
        """
        if not self.api_key:
            logger.error(f"No API key for {self.provider}. Cannot generate video.")
            return None

        try:
            if self.provider == "runway":
                return self._generate_runway(prompt, duration, style, output_path)
            elif self.provider == "luma":
                return self._generate_luma(prompt, duration, style, output_path)
            elif self.provider == "kling":
                return self._generate_kling(prompt, duration, style, output_path)
            elif self.provider == "pexels":
                return self._generate_pexels(prompt, duration, style, output_path)
        except Exception as e:
            logger.error(f"Video generation failed ({self.provider}): {e}")
            return None

    def _generate_pexels(self, prompt: str, duration: int, style: str, output_path: Optional[Path]) -> Path:
        """Fetch high-quality stock video from Pexels."""
        headers = {"Authorization": self.api_key}
        # Extract keywords for better search
        keywords = prompt.split(",")[0]
        
        url = f"{self.base_url}/search?query={keywords}&per_page=1&orientation=portrait&size=medium"
        
        logger.info(f"🎞️ Pexels Search: {keywords}")
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        
        data = response.json()
        videos = data.get("videos", [])
        
        if not videos:
            logger.warning(f"No Pexels videos found for: {keywords}")
            # Fallback to general nature/business search
            response = requests.get(f"{self.base_url}/search?query=cinematic&per_page=1", headers=headers)
            videos = response.json().get("videos", [])
            if not videos: raise ValueError("Pexels returned zero results even for fallback")

        # Pick the best file (highest resolution but within limits)
        video = videos[0]
        video_files = video.get("video_files", [])
        # Preferred: 1080p or 720p
        best_file = next((f for f in video_files if f.get("width") == 1080), video_files[0])
        video_url = best_file.get("link")

        logger.info(f"⬇️ Downloading Pexels video: {video_url}")
        video_response = requests.get(video_url, timeout=60)
        video_response.raise_for_status()

        if not output_path:
            output_path = Path(f"/tmp/pexels_{video['id']}.mp4")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(video_response.content)
        
        logger.info(f"✅ Pexels video saved: {output_path}")
        return output_path

    def _generate_runway(self, prompt: str, duration: int, style: str, output_path: Optional[Path]) -> Path:
        """Generate video using Runway ML Gen-3."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # Enhance prompt with style
        full_prompt = f"{prompt}, {style} style, high quality, professional cinematography"

        payload = {
            "text_prompt": full_prompt,
            "duration": duration,
            "aspect_ratio": "16:9",
            "model": "gen3",
        }

        logger.info(f"🎬 Runway Gen-3: {prompt[:50]}...")

        # Step 1: Create generation task
        response = requests.post(f"{self.base_url}/generate", json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        task_id = response.json()["id"]
        logger.info(f"Task ID: {task_id}")

        # Step 2: Poll for completion
        max_wait = 300  # 5 minutes
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status_response = requests.get(f"{self.base_url}/tasks/{task_id}", headers=headers, timeout=10)
            status_response.raise_for_status()

            status_data = status_response.json()
            status = status_data.get("status")

            if status == "SUCCEEDED":
                video_url = status_data.get("output", {}).get("url")
                if not video_url:
                    raise ValueError("No video URL in response")

                # Download video
                video_response = requests.get(video_url, timeout=60)
                video_response.raise_for_status()

                if not output_path:
                    output_path = Path(f"/tmp/runway_{task_id}.mp4")

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(video_response.content)

                logger.info(f"✅ Runway video saved: {output_path}")
                return output_path

            elif status == "FAILED":
                raise RuntimeError(f"Runway task failed: {status_data}")

            time.sleep(5)

        raise TimeoutError("Runway generation timed out")

    def _generate_luma(self, prompt: str, duration: int, style: str, output_path: Optional[Path]) -> Path:
        """Generate video using Luma AI Dream Machine."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "prompt": f"{prompt}, {style}",
            "aspect_ratio": "16:9",
            "loop": False,
        }

        logger.info(f"🌙 Luma AI: {prompt[:50]}...")

        response = requests.post(f"{self.base_url}/generations", json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        generation_id = response.json()["id"]

        # Poll for completion
        max_wait = 300
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status_response = requests.get(
                f"{self.base_url}/generations/{generation_id}",
                headers=headers,
                timeout=10,
            )
            status_response.raise_for_status()

            data = status_response.json()
            state = data.get("state")

            if state == "completed":
                video_url = data["video"]["url"]

                video_response = requests.get(video_url, timeout=60)
                video_response.raise_for_status()

                if not output_path:
                    output_path = Path(f"/tmp/luma_{generation_id}.mp4")

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(video_response.content)

                logger.info(f"✅ Luma video saved: {output_path}")
                return output_path

            elif state == "failed":
                raise RuntimeError("Luma generation failed")

            time.sleep(5)

        raise TimeoutError("Luma generation timed out")

    def _generate_kling(self, prompt: str, duration: int, style: str, output_path: Optional[Path]) -> Path:
        """Generate video using Kling AI."""
        # Kling API implementation (placeholder - adapt to actual API)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "prompt": f"{prompt}, {style} style",
            "duration": duration,
            "resolution": "1080p",
        }

        logger.info(f"🎥 Kling AI: {prompt[:50]}...")

        response = requests.post(f"{self.base_url}/text2video", json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        task_id = response.json()["task_id"]

        # Poll (simplified)
        max_wait = 300
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status_response = requests.get(f"{self.base_url}/task/{task_id}", headers=headers, timeout=10)
            status_response.raise_for_status()

            data = status_response.json()

            if data["status"] == "completed":
                video_url = data["result_url"]

                video_response = requests.get(video_url, timeout=60)
                video_response.raise_for_status()

                if not output_path:
                    output_path = Path(f"/tmp/kling_{task_id}.mp4")

                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(video_response.content)

                logger.info(f"✅ Kling video saved: {output_path}")
                return output_path

            time.sleep(5)

        raise TimeoutError("Kling generation timed out")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    gen = VideoGenerator(provider="runway")

    # Test generation
    video_path = gen.generate_video(
        prompt="A futuristic cityscape at sunset, flying cars in the sky, neon lights",
        duration=5,
        style="cinematic",
    )

    if video_path:
        print(f"Generated video: {video_path}")
