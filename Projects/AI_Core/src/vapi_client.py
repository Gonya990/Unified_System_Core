"""
VAPI.ai Voice Interface Client
Provides voice transcription, synthesis, and phone call capabilities.
Integrates with VAPI.ai platform for real-time voice conversations.
"""
import asyncio
import logging
import os
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

# Lazy import for VAPI SDK
VAPI_AVAILABLE = False
try:
    from vapi_python import Vapi

    VAPI_AVAILABLE = True
except ImportError:
    logger.warning("vapi-python not installed - voice features will be unavailable")


class VAPIClient:
    """Client for VAPI.ai voice services (transcription, synthesis, phone calls)."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize VAPI client with API key from environment or parameter.

        Args:
            api_key: VAPI API key (default: from VAPI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("VAPI_API_KEY")
        self.phone_number_id = os.getenv("VAPI_PHONE_NUMBER_ID")
        self.assistant_id = os.getenv("VAPI_ASSISTANT_ID")
        self.voice_id = os.getenv("VAPI_VOICE_ID", "rachel")

        self.client = None
        self.authenticated = False

        if not VAPI_AVAILABLE:
            logger.warning("VAPI SDK not available - install with: pip install vapi-python")
            return

        if not self.api_key:
            logger.warning("VAPI_API_KEY not set in environment")
            return

        try:
            self.client = Vapi(api_key=self.api_key)
            self.authenticated = True
            logger.info("VAPI client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize VAPI client: {e}")
            self.authenticated = False

    def is_valid(self) -> bool:
        """Check if client is properly initialized and authenticated."""
        return self.authenticated and self.client is not None

    async def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """
        Transcribe audio file using VAPI.

        Args:
            audio_path: Path to audio file (OGG, WAV, MP3, etc.)

        Returns:
            Transcribed text or None on failure
        """
        if not self.is_valid():
            logger.debug("VAPI transcription unavailable - client not valid")
            return None

        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return None

        try:
            # Run VAPI transcription in executor to avoid blocking async loop
            loop = asyncio.get_event_loop()
            transcript = await loop.run_in_executor(
                None, self._transcribe_sync, audio_path
            )
            if transcript:
                logger.debug(f"VAPI transcription successful ({len(transcript)} chars)")
            return transcript
        except Exception as e:
            logger.error(f"VAPI transcription failed: {e}")
            return None

    def _transcribe_sync(self, audio_path: str) -> Optional[str]:
        """
        Synchronous wrapper for VAPI transcription.
        Called from async context via run_in_executor.

        Args:
            audio_path: Path to audio file

        Returns:
            Transcribed text or None
        """
        try:
            # VAPI SDK would provide transcription via Whisper or similar
            # This is a placeholder for the actual SDK call
            # Implementation depends on VAPI SDK version and available methods

            with open(audio_path, "rb") as audio_file:
                # Example using VAPI's transcription API
                # Note: Actual implementation depends on VAPI SDK methods
                logger.debug(f"Transcribing audio from {audio_path}")

                # This would be replaced with actual VAPI transcription call
                # For now, return None to indicate fallback should be used
                return None
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return None

    async def generate_speech(
        self, text: str, voice_id: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Generate speech from text using VAPI TTS.

        Args:
            text: Text to synthesize
            voice_id: Voice ID (default: from config or 'rachel')

        Returns:
            Audio bytes (OGG format) or None on failure
        """
        if not self.is_valid():
            logger.debug("VAPI TTS unavailable - client not valid")
            return None

        if not text or not text.strip():
            logger.warning("Empty text provided to generate_speech")
            return None

        voice = voice_id or self.voice_id or "rachel"

        try:
            # Run VAPI TTS in executor to avoid blocking async loop
            loop = asyncio.get_event_loop()
            audio_data = await loop.run_in_executor(
                None, self._synthesize_sync, text, voice
            )
            if audio_data:
                logger.debug(f"VAPI TTS successful ({len(audio_data)} bytes)")
            return audio_data
        except Exception as e:
            logger.error(f"VAPI TTS failed: {e}")
            return None

    def _synthesize_sync(self, text: str, voice_id: str) -> Optional[bytes]:
        """
        Synchronous wrapper for VAPI text-to-speech.
        Called from async context via run_in_executor.

        Args:
            text: Text to synthesize
            voice_id: Voice ID (e.g., 'rachel', 'onyx')

        Returns:
            Audio bytes or None
        """
        try:
            logger.debug(f"Synthesizing speech: {voice_id}")

            # This would be replaced with actual VAPI TTS call
            # Example: using VAPI's TTS API with specified voice
            # The implementation depends on VAPI SDK's available methods

            # Placeholder - return None to indicate unavailable
            return None
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return None

    async def create_phone_call(
        self,
        phone_number: str,
        system_message: str,
        assistant_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Initiate outbound phone call using VAPI.

        Args:
            phone_number: Phone number in E.164 format (e.g., +972541234567)
            system_message: System prompt/context for the voice assistant
            assistant_id: Override default assistant (optional)

        Returns:
            Call info dict with 'id' and other metadata, or None on failure
        """
        if not self.is_valid():
            logger.error("VAPI client not configured for phone calls")
            return None

        if not self.phone_number_id:
            logger.error("VAPI_PHONE_NUMBER_ID not set - cannot make calls")
            return None

        if not phone_number or not phone_number.startswith("+"):
            logger.error(f"Invalid phone number format: {phone_number} (must be E.164)")
            return None

        assistant_to_use = assistant_id or self.assistant_id

        try:
            # Run VAPI call creation in executor
            loop = asyncio.get_event_loop()
            call_info = await loop.run_in_executor(
                None,
                self._create_call_sync,
                phone_number,
                system_message,
                assistant_to_use,
            )
            if call_info:
                call_id = call_info.get("id", "unknown")
                logger.info(f"Phone call initiated: {call_id} to {phone_number}")
            return call_info
        except Exception as e:
            logger.error(f"Failed to create phone call: {e}")
            return None

    def _create_call_sync(
        self, phone_number: str, system_message: str, assistant_id: Optional[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Synchronous wrapper for VAPI phone call creation.
        Called from async context via run_in_executor.

        Args:
            phone_number: E.164 format phone number
            system_message: System prompt for assistant
            assistant_id: Assistant to use for call

        Returns:
            Call info dict or None
        """
        try:
            logger.debug(f"Creating phone call to {phone_number}")

            # Build call parameters
            call_params = {
                "phone_number_id": self.phone_number_id,
                "customer": {"number": phone_number},
            }

            # Add assistant if specified
            if assistant_id:
                call_params["assistant_id"] = assistant_id

            # Add custom message context if available
            if system_message:
                call_params["system_prompt"] = system_message

            # Make the actual call via VAPI SDK
            # This would be: response = self.client.calls.create(**call_params)
            # Placeholder - return None to indicate unavailable
            logger.debug(f"Call params prepared: {list(call_params.keys())}")
            return None

        except Exception as e:
            logger.error(f"Call creation error: {e}")
            return None

    def get_call_status(self, call_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a phone call.

        Args:
            call_id: Call ID returned from create_phone_call

        Returns:
            Call status dict or None
        """
        if not self.is_valid():
            return None

        try:
            # Would use: response = self.client.calls.get(call_id)
            logger.debug(f"Getting status for call {call_id}")
            return None
        except Exception as e:
            logger.error(f"Failed to get call status: {e}")
            return None

    async def create_assistant(
        self,
        name: str,
        system_prompt: str,
        model: Optional[str] = None,
        voice_provider: Optional[str] = None,
        voice_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new voice assistant in VAPI.

        Args:
            name: Assistant name
            system_prompt: System instruction for the assistant
            model: LLM model (default: gpt-4o)
            voice_provider: Voice provider (default: 11labs)
            voice_id: Voice ID (default: rachel)

        Returns:
            Assistant info dict with 'id' or None
        """
        if not self.is_valid():
            logger.error("VAPI client not available")
            return None

        try:
            loop = asyncio.get_event_loop()
            assistant = await loop.run_in_executor(
                None,
                self._create_assistant_sync,
                name,
                system_prompt,
                model,
                voice_provider,
                voice_id,
            )
            return assistant
        except Exception as e:
            logger.error(f"Failed to create assistant: {e}")
            return None

    def _create_assistant_sync(
        self,
        name: str,
        system_prompt: str,
        model: Optional[str],
        voice_provider: Optional[str],
        voice_id: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        """Synchronous wrapper for assistant creation."""
        try:
            logger.debug(f"Creating assistant: {name}")

            # Build assistant config
            assistant_config = {
                "name": name,
                "model": {
                    "provider": "openai",
                    "model": model or "gpt-4o",
                    "messages": [{"role": "system", "content": system_prompt}],
                },
                "voice": {
                    "provider": voice_provider or "11labs",
                    "voiceId": voice_id or "rachel",
                },
            }

            # Would create: response = self.client.assistants.create(**assistant_config)
            logger.debug("Assistant config prepared")
            return None

        except Exception as e:
            logger.error(f"Assistant creation error: {e}")
            return None
