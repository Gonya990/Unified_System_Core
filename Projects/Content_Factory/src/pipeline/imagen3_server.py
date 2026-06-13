import os
import logging
import asyncio
from google.cloud import aiplatform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Imagen3Server")

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "unified-system-413119")
LOCATION = os.environ.get("VERTEX_LOCATION", "us-central1")

class Imagen3Client:
    def __init__(self):
        self.project_id = PROJECT_ID
        self.location = LOCATION
        # Init Vertex AI
        aiplatform.init(project=self.project_id, location=self.location)
    
    async def generate_image(self, prompt: str, output_path: str, aspect_ratio: str = "16:9"):
        """Generates an image using Imagen 3 via Vertex AI endpoint."""
        logger.info(f"Generating image with Imagen 3 for prompt: '{prompt}'")
        from vertexai.preview.vision_models import ImageGenerationModel
        
        # We use the preview vision_models for Imagen 3 for now
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        
        try:
            response = await asyncio.to_thread(
                model.generate_images,
                prompt=prompt,
                number_of_images=1,
                aspect_ratio=aspect_ratio,
                output_mime_type="image/png"
            )
            
            if response and len(response) > 0:
                image = response[0]
                image.save(output_path)
                logger.info(f"Image successfully saved to {output_path}")
                return output_path
            else:
                logger.error("No images returned from Imagen 3.")
                return None
        except Exception as e:
            logger.error(f"Imagen 3 Generation failed: {e}")
            return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
        out = sys.argv[2] if len(sys.argv) > 2 else "imagen3_output.png"
        client = Imagen3Client()
        asyncio.run(client.generate_image(prompt, out))
    else:
        logger.info("Usage: python imagen3_server.py <prompt> [output_path]")
