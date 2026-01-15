"""
Image Generator with Retry Logic and Exponential Backoff

Handles image generation requests with robust error handling.
Currently supports OpenAI DALL-E 3.
"""

import asyncio
import logging
import random
import re
import time
from pathlib import Path
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)

# Retry configuration
MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_DELAY = 60.0
RETRYABLE_CODES = (429, 500, 502, 503, 504)


def sanitize_prompt(prompt: str, max_length: int = 4000) -> str:
    """
    Sanitize prompt for API calls to prevent 400 errors.
    """
    # Remove control characters except newlines and tabs
    prompt = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", prompt)
    # Truncate if too long
    if len(prompt) > max_length:
        prompt = prompt[:max_length] + "..."
    return prompt.strip()


def calculate_backoff(attempt: int, base_delay: float = BASE_DELAY, max_delay: float = MAX_DELAY) -> float:
    """Calculate delay with exponential backoff and jitter."""
    delay = min(base_delay * (2**attempt), max_delay)
    return delay * (0.5 + random.random())


class ImageGenerator:
    """
    Handles image generation requests with retry logic.
    Currently supports OpenAI DALL-E 3.
    """

    def __init__(self, config_manager, provider="openai"):
        self.config = config_manager
        self._provider = provider

    @property
    def provider(self):
        return self._provider

    async def generate(self, prompt: str, user_id: int) -> Optional[Path]:
        """
        Generate an image based on the prompt.
        Returns the path to the saved image file.
        """
        if self.provider == "openai":
            return await self._openai_image(prompt, user_id)
        else:
            raise ValueError(f"Unsupported image provider: {self.provider}")

    async def _openai_image(self, prompt: str, user_id: int) -> Path:
        """Generate image with OpenAI DALL-E 3 with retry logic."""
        api_key = self.config.get("OPENAI_API_KEY", self.config.get("INFERENCE_API_KEY"))
        if not api_key:
            raise ValueError("OpenAI API key not set. Use /setapikey")

        url = "https://api.openai.com/v1/images/generations"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        # Sanitize prompt to prevent 400 errors
        clean_prompt = sanitize_prompt(prompt)

        payload = {
            "model": "dall-e-3",
            "prompt": clean_prompt,
            "size": "1024x1024",
            "quality": "standard",
            "n": 1,
        }

        logger.info(f"Generating image via OpenAI for user {user_id}: {clean_prompt[:50]}...")

        last_error = None

        for attempt in range(MAX_RETRIES + 1):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, headers=headers) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            image_url = data["data"][0]["url"]

                            # Download image
                            async with session.get(image_url) as img_resp:
                                if img_resp.status != 200:
                                    raise Exception("Failed to download generated image")

                                img_data = await img_resp.read()

                                # Ensure images directory exists
                                output_dir = Path("images")
                                output_dir.mkdir(exist_ok=True)

                                filename = f"{user_id}_{int(time.time())}.png"
                                output_path = output_dir / filename

                                output_path.write_bytes(img_data)
                                logger.info(f"Image saved to {output_path}")
                                return output_path

                        # Handle retryable errors
                        if resp.status in RETRYABLE_CODES:
                            text = await resp.text()
                            last_error = Exception(f"HTTP {resp.status}: {text}")

                            if attempt < MAX_RETRIES:
                                delay = calculate_backoff(attempt)
                                logger.warning(
                                    f"[Retry] OpenAI image generation attempt {attempt + 1}/{MAX_RETRIES + 1} "
                                    f"failed with status {resp.status}. Retrying in {delay:.2f}s..."
                                )
                                await asyncio.sleep(delay)
                                continue

                        # Non-retryable error
                        text = await resp.text()
                        logger.error(f"OpenAI Image Error (status={resp.status}): {text}")
                        raise Exception(f"OpenAI Error: {text}")

            except aiohttp.ClientError as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    delay = calculate_backoff(attempt)
                    logger.warning(
                        f"[Retry] Network error on attempt {attempt + 1}/{MAX_RETRIES + 1}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)
                    continue
                raise

        if last_error:
            logger.error(f"All {MAX_RETRIES + 1} retry attempts exhausted for image generation")
            raise last_error

        raise Exception("Image generation failed unexpectedly")
