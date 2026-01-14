import logging
import os
import subprocess
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)


class Wav2LipController:
    def __init__(self, base_dir: str = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Default: Projects/Content_Factory/src/lip_sync
            self.base_dir = Path(__file__).parent.resolve()

        self.wav2lip_root = self.base_dir / "Wav2Lip"
        self.checkpoints_dir = self.wav2lip_root / "checkpoints"
        self.output_dir = Path("Projects/Content_Factory/outputs/lip_sync")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Prefer GAN model for better visual quality
        self.checkpoint_path = self.checkpoints_dir / "wav2lip_gan.pth"

    def animate(self, face_path: str, audio_path: str, output_filename: str = None) -> str:
        """
        Runs Wav2Lip inference.

        Args:
            face_path: Path to the image (or video) of the face.
            audio_path: Path to the audio file.
            output_filename: Optional filename for the output video.

        Returns:
            Path to the generated video file.
        """
        if not os.path.exists(face_path):
            raise FileNotFoundError(f"Face file not found: {face_path}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if not output_filename:
            # Generate filename based on inputs
            face_name = Path(face_path).stem
            audio_name = Path(audio_path).stem
            output_filename = f"{face_name}_{audio_name}_lip_synced.mp4"

        output_path = self.output_dir / output_filename

        # Prepare command
        # python inference.py --checkpoint_path ... --face ... --audio ... --outfile ...
        cmd = [
            "python3",
            "inference.py",
            "--checkpoint_path",
            str(self.checkpoint_path.resolve()),
            "--face",
            str(Path(face_path).resolve()),
            "--audio",
            str(Path(audio_path).resolve()),
            "--outfile",
            str(output_path.resolve()),
            "--resize_factor",
            "1",
            "--nosmooth",
        ]

        logger.info(f"Starting Lip-Sync: {face_path} + {audio_path}")
        logger.info(f"Command: {' '.join(cmd)}")

        try:
            # Run inside the Wav2Lip directory to handle relative imports inside inference.py
            # Do NOT use capture_output=True for long-running processes with TQDM as it can hang the pipe
            subprocess.run(cmd, cwd=str(self.wav2lip_root), check=True)

            if output_path.exists():
                logger.info(f"Lip-Sync successfully generated: {output_path}")
                return str(output_path)
            else:
                logger.error("Wav2Lip finished but output file was not found.")
                return None

        except subprocess.CalledProcessError as e:
            logger.error(f"Wav2Lip failed with exit code {e.returncode}")
            raise RuntimeError("Lip-Sync inference failed. Check terminal output for details.") from e


# Simple CLI test
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Wav2Lip Controller CLI")
    parser.add_argument("--face", required=True, help="Path to face image/video")
    parser.add_argument("--audio", required=True, help="Path to audio file")
    args = parser.parse_args()

    controller = Wav2LipController()
    result = controller.animate(args.face, args.audio)
    if result:
        print(f"Result saved to: {result}")
