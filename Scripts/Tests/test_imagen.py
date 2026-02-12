import asyncio
import sys
from pathlib import Path

# Fix relative imports
PROJECT_ROOT = Path("/Users/igorgoncharenko/Documents/Unified_System_Core")
AI_CORE_SRC = PROJECT_ROOT / "Projects/AI_Core/src"
if str(AI_CORE_SRC) not in sys.path:
    sys.path.append(str(AI_CORE_SRC))

from image_generator import ImageGenerator  # noqa: E402
from inference_client import ConfigManager  # noqa: E402


async def test_imagen():
    print("Testing Imagen 3 Integration...")

    # Setup config
    config = ConfigManager()
    # Explicitly set provider for test
    config.set("IMAGE_PROVIDER", "vertex")
    config.set("GCP_PROJECT_ID", "gen-lang-client-0982257437")

    generator = ImageGenerator(config)

    prompt = (
        "Cinematic shot of a robotic chimpanzee typing on a transparent "
        "keyboard, neon lights, 8k resolution, photorealistic"
    )
    user_id = 999

    try:
        path = await generator.generate(prompt, user_id)
        if path and path.exists():
            print(f"SUCCESS: Image generated at {path}")
            # Log to tracking DB
            try:
                from Scripts.Maintenance.tracking_db import log_task

                log_task(
                    "Imagen 3 Test",
                    "Success",
                    f"Generated image for prompt: {prompt[:30]}",
                )
            except ImportError:
                pass
        else:
            print("FAILED: Image path not returned or does not exist")
    except Exception as e:
        print(f"ERROR: {e}")
        try:
            from Scripts.Maintenance.tracking_db import log_task

            log_task("Imagen 3 Test", "Failed", str(e))
        except ImportError:
            pass


if __name__ == "__main__":
    asyncio.run(test_imagen())
