#!/usr/bin/env python3
"""
Voice Cloning and Emotional TTS using ElevenLabs
"""

import logging
import os
from pathlib import Path
from typing import Optional

import requests

logger = logging.getLogger(__name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_BASE_URL = "https://api.elevenlabs.io/v1"


class VoiceGenerator:
    """Generate voiceovers using ElevenLabs TTS with emotion control."""

    def __init__(self):
        self.api_key = ELEVENLABS_API_KEY
        self.voices_cache = {}

        if not self.api_key:
            logger.warning("ElevenLabs API key not set. Voice generation disabled.")

    def generate_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        voice_name: str = "Antoni",
        emotion: str = "neutral",
        output_path: Optional[Path] = None,
    ) -> Optional[Path]:
        """
        Generate speech from text.

        Args:
            text: Text to convert to speech
            voice_id: ElevenLabs voice ID (if known)
            voice_name: Voice name (Antoni, Bella, Rachel, etc.)
            emotion: Emotion/style (neutral, excited, sad, angry, mysterious)
            output_path: Where to save audio

        Returns:
            Path to generated audio file
        """
        if not self.api_key:
            logger.error("ElevenLabs not configured. Cannot generate speech.")
            return None

        try:
            # Get voice ID if not provided
            if not voice_id:
                voice_id = self._get_voice_id(voice_name)

            # Generate speech
            headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}

            # Map emotion to voice settings
            voice_settings = self._get_voice_settings(emotion)

            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2",  # Supports multiple languages
                "voice_settings": voice_settings,
            }

            logger.info(f"🎤 ElevenLabs: Generating {len(text)} chars with {emotion} emotion...")

            response = requests.post(
                f"{ELEVENLABS_BASE_URL}/text-to-speech/{voice_id}",
                json=payload,
                headers=headers,
                timeout=60,
            )
            response.raise_for_status()

            if not output_path:
                import hashlib

                text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
                output_path = Path(f"/tmp/elevenlabs_{voice_name}_{text_hash}.mp3")

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(response.content)

            logger.info(f"✅ ElevenLabs speech saved: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"ElevenLabs generation failed: {e}")
            return None

    def _get_voice_id(self, voice_name: str) -> str:
        """Get voice ID by name from ElevenLabs API."""
        if voice_name in self.voices_cache:
            return self.voices_cache[voice_name]

        headers = {"xi-api-key": self.api_key}

        response = requests.get(f"{ELEVENLABS_BASE_URL}/voices", headers=headers, timeout=10)
        response.raise_for_status()

        voices = response.json().get("voices", [])

        for voice in voices:
            if voice["name"].lower() == voice_name.lower():
                voice_id = voice["voice_id"]
                self.voices_cache[voice_name] = voice_id
                return voice_id

        # Default to first voice if not found
        logger.warning(f"Voice '{voice_name}' not found. Using default.")
        default_id = voices[0]["voice_id"] if voices else "21m00Tcm4TlvDq8ikWAM"
        self.voices_cache[voice_name] = default_id
        return default_id

    def _get_voice_settings(self, emotion: str) -> dict:
        """Map emotion to ElevenLabs voice settings."""
        # Base settings
        settings = {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True,
        }

        # Emotion-specific adjustments
        emotion_map = {
            "excited": {"stability": 0.3, "style": 0.8},
            "calm": {"stability": 0.7, "style": 0.3},
            "dramatic": {"stability": 0.4, "style": 0.9},
            "mysterious": {"stability": 0.6, "style": 0.7},
            "sad": {"stability": 0.6, "style": 0.4},
            "angry": {"stability": 0.3, "style": 0.9},
        }

        if emotion in emotion_map:
            settings.update(emotion_map[emotion])

        return settings

    def clone_voice(self, name: str, audio_files: list[Path], description: str = "") -> Optional[str]:
        """
        Clone a voice from audio samples.

        Args:
            name: Name for the cloned voice
            audio_files: List of audio file paths (1-25 samples, 30s-5min each)
            description: Description of the voice

        Returns:
            Voice ID of cloned voice
        """
        if not self.api_key:
            logger.error("ElevenLabs not configured.")
            return None

        headers = {"xi-api-key": self.api_key}

        files = []
        for _i, audio_path in enumerate(audio_files):
            if not audio_path.exists():
                logger.warning(f"Audio file not found: {audio_path}")
                continue

            files.append(("files", (audio_path.name, open(audio_path, "rb"), "audio/mpeg")))

        if not files:
            logger.error("No valid audio files for voice cloning")
            return None

        data = {"name": name, "description": description or f"Cloned voice: {name}"}

        logger.info(f"🎭 Cloning voice '{name}' from {len(files)} samples...")

        try:
            response = requests.post(
                f"{ELEVENLABS_BASE_URL}/voices/add",
                headers=headers,
                data=data,
                files=files,
                timeout=120,
            )
            response.raise_for_status()

            voice_id = response.json()["voice_id"]
            logger.info(f"✅ Voice cloned successfully: {voice_id}")

            # Close file handles
            for _, (_, fp, _) in files:
                fp.close()

            return voice_id

        except Exception as e:
            logger.error(f"Voice cloning failed: {e}")

            # Close file handles on error
            for _, (_, fp, _) in files:
                fp.close()

            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    gen = VoiceGenerator()

    # Test speech generation
    audio = gen.generate_speech(
        text="Welcome to the future of AI voice synthesis. This is a demonstration of emotional text-to-speech.",
        voice_name="Antoni",
        emotion="excited",
    )

    if audio:
        print(f"Generated speech: {audio}")
