import logging
import time
from pathlib import Path
from typing import Optional

import aiohttp

# Internal imports
try:
    from .inference_client import ConfigManager
except ImportError:
    from inference_client import ConfigManager

# Fix relative imports
PROJECT_ROOT = Path("/Users/igorgoncharenko/Documents/Unified_System_Core")

logger = logging.getLogger(__name__)

class ImageGenerator:
    """
    Handles image generation requests.
    Currently supports OpenAI DALL-E 3.
    """
    def __init__(self, config_manager: ConfigManager, provider="openai"):
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
        provider = self.config.get("IMAGE_PROVIDER", self.provider)

        if provider == "openai":
            return await self._openai_image(prompt, user_id)
        elif provider == "vertex" or provider == "google":
            return await self._vertex_imagen(prompt, user_id)
        else:
            raise ValueError(f"Unsupported image provider: {provider}")

    async def _openai_image(self, prompt: str, user_id: int) -> Path:
        api_key = self.config.get(
            "OPENAI_API_KEY", self.config.get("INFERENCE_API_KEY")
        )
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

        logger.info(
            f"Generating image via OpenAI for user {user_id}: {prompt[:50]}..."
        )

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
    async def _vertex_imagen(self, prompt: str, user_id: int) -> Path:
        """Generate high-quality cinematic image via Vertex AI Imagen 3."""
        try:
            from google import genai
            from google.genai import types

            project = self.config.get(
                "GCP_PROJECT_ID", "gen-lang-client-0982257437"
            )
            client = genai.Client(
                vertexai=True, project=project, location="us-central1"
            )

            logger.info(
                f"Generating Imagen 3 (Vertex) for user {user_id}: "
                f"{prompt[:50]}..."
            )

            response = client.models.generate_images(
                model='imagen-3.0-generate-001',
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    output_mime_type='image/png'
                )
            )

            img_data = response.generated_images[0].image.image_bytes

            output_dir = Path("images")
            output_dir.mkdir(exist_ok=True)

            filename = f"vertex_{user_id}_{int(time.time())}.png"
            output_path = output_dir / filename
            output_path.write_bytes(img_data)

            logger.info(f"Imagen 3 saved to {output_path}")
            return output_path

        except ImportError:
            logger.error("google-genai not installed. Run: pip install google-genai")
            raise Exception("Imagen 3 requires google-genai SDK")
        except Exception as e:
            logger.error(f"Vertex Imagen Error: {e}")
            raise e
