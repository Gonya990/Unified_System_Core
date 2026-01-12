
import logging
import time
from pathlib import Path
from typing import Optional

import aiohttp

logger = logging.getLogger(__name__)

class ImageGenerator:
    """
    Handles image generation requests.
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
        api_key = self.config.get("OPENAI_API_KEY", self.config.get("INFERENCE_API_KEY"))
        if not api_key:
            raise ValueError("OpenAI API key not set. Use /setapikey")

        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "dall-e-3",
            "prompt": prompt,
            "size": "1024x1024",
            "quality": "standard",
            "n": 1,
        }

        logger.info(f"Generating image via OpenAI for user {user_id}: {prompt[:50]}...")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    logger.error(f"OpenAI Image Error: {text}")
                    raise Exception(f"OpenAI Error: {text}")

                data = await resp.json()
                image_url = data['data'][0]['url']

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
