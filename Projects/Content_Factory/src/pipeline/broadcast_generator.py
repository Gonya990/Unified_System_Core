import json
import logging
import subprocess
import sys
from pathlib import Path

import torch

# Add project root to sys.path
ROOT_DIR = Path(__file__).parent.parent.parent.parent.parent.resolve()
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from TTS.api import TTS  # noqa: E402
except ImportError:
    TTS = None

from Projects.Content_Factory.src.lip_sync.live_portrait_controller import LivePortraitController  # noqa: E402
from Projects.Content_Factory.src.lip_sync.wav2lip_controller import Wav2LipController  # noqa: E402

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def produce_broadcast(character_id="unit_x", text=None, output_filename=None):
    """
    Modular production function for AI Broadcasts.
    """
    # Load character config
    config_path = ROOT_DIR / "Projects/Content_Factory/config/character_profiles.json"
    with open(config_path) as f:
        profiles = json.load(f)

    if character_id not in profiles:
        raise ValueError(f"Character {character_id} not found in profiles.")

    char = profiles[character_id]

    # Defaults
    if not text:
        text = "Здравствуйте. Это тестовый выпуск новостей."

    output_dir = ROOT_DIR / "Projects/Content_Factory/outputs/production"
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / f"{character_id}_temp_audio.wav"
    avatar_path = ROOT_DIR / char["avatar_path"]
    ref_wav = ROOT_DIR / char["voice_ref_path"]

    # 1. Generate Audio
    if not TTS:
        logger.error("TTS not installed in current environment.")
        return None

    logger.info(f"🎙️ Generating Audio for {character_id}...")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
    tts = TTS(model_name).to(device)
    tts.tts_to_file(text=text, speaker_wav=str(ref_wav), language=char["primary_language"], file_path=str(audio_path))

    # 2. Generate Motion
    logger.info("🎬 Generating Motion (LivePortrait)...")
    lp_controller = LivePortraitController()
    lp_video_path = lp_controller.animate(str(avatar_path), output_filename=f"{character_id}_motion.mp4")

    if not lp_video_path:
        return None

    # 3. Loop Motion to match Audio
    looped_motion = output_dir / f"{character_id}_motion_looped.mp4"
    try:
        audio_dur = float(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    str(audio_path),
                ]
            ).strip()
        )
        video_dur = float(
            subprocess.check_output(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "format=duration",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    str(lp_video_path),
                ]
            ).strip()
        )

        loops = int(audio_dur / video_dur) + 1
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-stream_loop",
                str(loops - 1),
                "-i",
                str(lp_video_path),
                "-t",
                str(audio_dur),
                "-c",
                "copy",
                str(looped_motion),
            ],
            check=True,
            capture_output=True,
        )
        motion_for_sync = str(looped_motion)
    except Exception as e:
        logger.error(f"Looping failed: {e}")
        motion_for_sync = str(lp_video_path)

    # 4. Generate Lip-Sync
    logger.info("👄 Applying Lip-Sync (Wav2Lip)...")
    w2l_controller = Wav2LipController()
    final_video = w2l_controller.animate(
        face_path=motion_for_sync,
        audio_path=str(audio_path),
        output_filename=output_filename or f"broadcast_{character_id}.mp4",
    )

    return final_video


if __name__ == "__main__":
    # Test run
    produce_broadcast(character_id="unit_x", text="Это тест модульной системы.")
