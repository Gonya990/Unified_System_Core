import os
import subprocess
import logging
from pathlib import Path
import shutil

# Setup logging
logger = logging.getLogger(__name__)


class LivePortraitController:
    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Default: Projects/Content_Factory/src/live_portrait
            self.base_dir = Path("Projects/Content_Factory/src/live_portrait").resolve()

        self.output_dir = Path("Projects/Content_Factory/outputs/live_portrait")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Default driving video (from the repo examples)
        self.default_driving = self.base_dir / "assets/examples/driving/d0.mp4"

    def animate(self, source_path: str, driving_path: str = None, output_filename: str = None) -> str:
        """
        Runs LivePortrait inference.

        Args:
            source_path: Path to the source image (avatar).
            driving_path: Path to the driving video (optional, uses default if None).
            output_filename: Optional filename for the final video.

        Returns:
            Path to the generated video file.
        """
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file not found: {source_path}")

        driving = driving_path if driving_path else str(self.default_driving)
        if not os.path.exists(driving):
            # Try relative to repo if not absolute
            driving = str(self.base_dir / driving)
            if not os.path.exists(driving):
                raise FileNotFoundError(f"Driving video not found: {driving}")

        # LivePortrait output is saved in 'animations/' within the repo working dir by default
        # We will move it to our output folder afterwards

        # Prepare environment
        env = os.environ.copy()
        env["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

        cmd = [
            "python3",
            "inference.py",
            "-s",
            str(Path(source_path).resolve()),
            "-d",
            str(Path(driving).resolve()),
            "--flag_crop_driving_video",  # Recommended for stability
        ]

        logger.info(f"🚀 Starting LivePortrait: {source_path} using {driving}")

        try:
            subprocess.run(cmd, cwd=str(self.base_dir), check=True, env=env)

            # Find the output. LivePortrait usually names it source--driving_concat.mp4 or similar
            # We look in the 'animations' directory inside live_portrait
            anim_dir = self.base_dir / "animations"
            generated_files = list(anim_dir.glob("*.mp4"))

            if not generated_files:
                logger.error("LivePortrait finished but animations/ folder is empty.")
                return None

            # Get the most recent file
            latest_video = max(generated_files, key=os.path.getmtime)

            if not output_filename:
                output_filename = f"{Path(source_path).stem}_animated.mp4"

            final_path = self.output_dir / output_filename
            shutil.move(str(latest_video), str(final_path))

            logger.info(f"✅ LivePortrait Success: {final_path}")
            return str(final_path)

        except subprocess.CalledProcessError as e:
            logger.error(f"LivePortrait failed with exit code {e.returncode}")
            raise RuntimeError("LivePortrait inference failed.") from e


# CLI test
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="LivePortrait Controller CLI")
    parser.add_argument("--source", required=True, help="Path to avatar image/video")
    parser.add_argument("--driving", help="Path to driving video (optional)")
    args = parser.parse_args()

    controller = LivePortraitController()
    result = controller.animate(args.source, args.driving)
    if result:
        print(f"Animation saved to: {result}")
