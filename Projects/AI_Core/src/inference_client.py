"""
Unified Inference Client for AI Telegram Bot.
Supports Ollama, OpenAI-compatible, Gemini, and custom endpoints.
"""
import logging
from pathlib import Path
from typing import Optional

import aiohttp

try:
    from .config_manager import ConfigManager
    from .modules.swarm_manager import SwarmManager
except ImportError:
    from config_manager import ConfigManager
    try:
        from modules.swarm_manager import SwarmManager
    except ImportError:
        # Fallback for direct testing
        SwarmManager = None

logger = logging.getLogger(__name__)

# Lazy import for Gemini
_gemini_client = None
_gemini_client_key = None

# Lazy import for VAPI
VAPI_AVAILABLE = False
try:
    from .vapi_client import VAPIClient

    VAPI_AVAILABLE = True
except ImportError:
    VAPI_AVAILABLE = False
    logger.debug("VAPIClient not available")


def _get_gemini_client(api_key: str):
    """Lazy load and configure Gemini client using new SDK."""
    global _gemini_client, _gemini_client_key
    try:
        from google import genai
        # from google.genai.types import GenerateContentConfig

        if not _gemini_client or _gemini_client_key != api_key:
            _gemini_client = genai.Client(api_key=api_key)
            _gemini_client_key = api_key
        return _gemini_client
    except ImportError:
        logger.error("google-genai not installed. Run: pip install google-genai")
        return None
    except Exception as e:
        logger.error(f"Failed to configure Gemini: {e}")
        return None

class InferenceClient:
    """Unified client for multiple AI inference providers."""

    def __init__(self, config: ConfigManager):
        self.config = config
        self.provider = config.get("INFERENCE_PROVIDER", "ollama")
        self.model = config.get("OLLAMA_MODEL", config.get("MODEL_NAME", "llama3.2"))
        self.endpoint = config.get("OLLAMA_BASE_URL", config.get("INFERENCE_BASE_URL", "http://localhost:11434"))
        self.api_key = config.get("INFERENCE_API_KEY", "")

        # Load resources for swarm
        resources_path = Path(__file__).parent.parent / "config" / "resources.yaml"
        self.swarm = SwarmManager(resources_path) if SwarmManager else None

        # Initialize VAPI client for voice features
        self.vapi = None
        if VAPI_AVAILABLE:
            vapi_key = config.get("VAPI_API_KEY")
            if vapi_key:
                try:
                    self.vapi = VAPIClient(vapi_key)
                    if self.vapi and self.vapi.is_valid():
                        logger.info("VAPI voice client initialized")
                    else:
                        self.vapi = None
                except Exception as e:
                    logger.warning(f"Failed to initialize VAPI client: {e}")
                    self.vapi = None

    async def chat(self, messages: list, system_prompt: Optional[str] = None, branch_id: str = "HOME_HQ", project_context: str = "PERSONAL"):
        """Routed chat request with branch awareness."""
        provider = self.config.get("INFERENCE_PROVIDER", self.provider)

        if provider == "gemini":
            return await self._chat_gemini(messages, system_prompt, branch_id, project_context)
        elif provider == "openai":
            return await self._chat_openai(messages, system_prompt)
        elif provider == "openrouter":
            return await self._chat_openrouter(messages, system_prompt)
        else:
            return await self._chat_ollama(messages, system_prompt)

    async def _chat_gemini(self, messages: list, system_prompt: Optional[str] = None, branch_id: str = "HOME_HQ", project_context: str = "PERSONAL"):
        """Gemini SDK integration with Swarm support and branch isolation."""
        api_key = self.api_key

        # Priority: Swarm Key -> Config Key
        if self.swarm:
            swarm_key = self.swarm.get_gemini_key(branch_id=branch_id, project_context=project_context)
            if swarm_key:
                api_key = swarm_key

        client = _get_gemini_client(api_key)
        if not client:
            return "Error: Gemini client not configured.", {}

        try:
            # Prepare contents
            contents = []
            if system_prompt:
                # The new genai SDK handles system prompt in config
                pass

            for m in messages:
                contents.append({
                    "role": "user" if m["role"] == "user" else "model",
                    "parts": [{"text": m["content"]}]
                })

            # Call Gemini
            model_name = self.config.get("GEMINI_MODEL", "gemini-2.0-flash-exp")

            # Use asyncio loop for blocking SDK call
            import asyncio
            loop = asyncio.get_event_loop()

            def call_sdk():
                from google.genai.types import GenerateContentConfig
                return client.models.generate_content(
                    model=model_name,
                    contents=contents,
                    config=GenerateContentConfig(
                        system_instruction=system_prompt if system_prompt else None
                    )
                )

            response = await loop.run_in_executor(None, call_sdk)

            # Parse usage
            usage = {
                "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
            }

            return response.text, usage

        except Exception as e:
            logger.error(f"Gemini Chat Error: {e}")

            # If 429, mark key as failed in swarm
            if "429" in str(e) and self.swarm:
                self.swarm.mark_key_failed("gemini", api_key)
                # Failover to next key could be implemented here with recursion

            return f"Error: {e}", {}

    async def _chat_ollama(self, messages: list, system_prompt: Optional[str] = None):
        """Ollama API request."""
        endpoint = self.config.get("OLLAMA_BASE_URL", self.endpoint)
        model = self.config.get("OLLAMA_MODEL", self.model)

        url = f"{endpoint}/api/chat"
        payload = {
            "model": model,
            "messages": messages,
            "stream": False
        }
        if system_prompt:
            payload["messages"].insert(0, {"role": "system", "content": system_prompt})

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("message", {}).get("content", ""), {
                            "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0)
                        }
                    return f"Error: Ollama status {resp.status}", {}
        except Exception as e:
            return f"Ollama Connection Error: {e}", {}

    async def _chat_openai(self, messages: list, system_prompt: Optional[str] = None):
        """OpenAI API request."""
        api_key = self.config.get("OPENAI_API_KEY")
        base_url = self.config.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        model = self.config.get("OPENAI_MODEL", "gpt-4o")

        if not api_key:
            return "Error: OpenAI API key not set.", {}

        url = f"{base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}"}

        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        payload_messages.extend(messages)

        payload = {
            "model": model,
            "messages": payload_messages,
            "stream": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        usage = data.get("usage", {})
                        return content, usage
                    return f"Error: OpenAI status {resp.status}", {}
        except Exception as e:
            return f"OpenAI Connection Error: {e}", {}

    async def _chat_openrouter(self, messages: list, system_prompt: Optional[str] = None):
        """OpenRouter API request."""
        api_key = self.config.get("OPENROUTER_API_KEY")
        base_url = self.config.get("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        model = self.config.get("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")

        if not api_key:
            return "Error: OpenRouter API key not set.", {}

        url = f"{base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "https://github.com/Unified-system-Core/AI_Core",
            "X-Title": "Unified AI Bot"
        }

        payload_messages = []
        if system_prompt:
            payload_messages.append({"role": "system", "content": system_prompt})
        payload_messages.extend(messages)

        payload = {
            "model": model,
            "messages": payload_messages,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
                        usage = data.get("usage", {})
                        return content, usage
                    return f"Error: OpenRouter status {resp.status} - {await resp.text()}", {}
        except Exception as e:
            return f"OpenRouter Connection Error: {e}", {}

    async def list_models(self):
        """List available models for the current provider."""
        provider = self.config.get("INFERENCE_PROVIDER", self.provider)

        if provider == "ollama":
            url = f"{self.endpoint}/api/tags"
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            data = await resp.json()
                            return [m['name'] for m in data.get('models', [])]
            except Exception as e:
                logger.error(f"Failed to list Ollama models: {e}")
            return ["llama3.2", "mistral", "gemma"] # Fallbacks

        elif provider == "gemini":
            # Return standard Gemini models
            return [
                "gemini-2.0-flash-exp",
                "gemini-1.5-flash",
                "gemini-1.5-pro"
            ]

        return [self.model]

    async def analyze_multimodal(self, file_path: str, prompt: str, mime_type: str = "image/jpeg"):
        """Analyze image or audio using vision/audio-capable models."""
        provider = self.config.get("INFERENCE_PROVIDER", self.provider)

        if provider == "gemini":
            api_key = self.api_key
            if self.swarm:
                swarm_key = self.swarm.get_gemini_key(branch_id="HOME_HQ", project_context="PERSONAL")
                if swarm_key:
                    api_key = swarm_key

            client = _get_gemini_client(api_key)
            if not client:
                return "Error: Gemini provider not configured."

            try:
                import asyncio
                from google.genai.types import Part

                with open(file_path, "rb") as f:
                    file_data = f.read()

                def call_sdk():
                    return client.models.generate_content(
                        model=self.config.get("GEMINI_MODEL", "gemini-2.0-flash-exp"),
                        contents=[
                            Part.from_bytes(data=file_data, mime_type=mime_type),
                            prompt
                        ]
                    )

                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, call_sdk)
                return response.text
            except Exception as e:
                logger.error(f"Gemini Multimodal Error: {e}")
                return f"Error analyzing media: {e}"

        return "Multimodal analysis is currently only supported via Gemini provider."

    async def analyze_image(self, image_path: str, prompt: str):
        """Analyze image using vision-capable models."""
        return await self.analyze_multimodal(image_path, prompt, mime_type="image/jpeg")

    async def transcribe_audio(self, audio_path: str):
        """
        Transcribe audio to text.
        Tries VAPI first (dedicated STT), falls back to Gemini (multimodal).
        """
        # Try VAPI first (dedicated speech-to-text)
        if self.vapi and self.vapi.is_valid():
            try:
                transcript = await self.vapi.transcribe_audio(audio_path)
                if transcript:
                    logger.debug("VAPI transcription successful")
                    return transcript
            except Exception as e:
                logger.debug(f"VAPI transcription failed, falling back to Gemini: {e}")

        # Fallback to Gemini (multimodal)
        provider = self.config.get("INFERENCE_PROVIDER", self.provider)
        if provider == "gemini":
            # Detect mime type based on extension
            mime_type = "audio/ogg" # Default for Telegram
            if audio_path.endswith(".mp3"): mime_type = "audio/mpeg"
            elif audio_path.endswith(".wav"): mime_type = "audio/wav"
            elif audio_path.endswith(".m4a"): mime_type = "audio/mp4"

            return await self.analyze_multimodal(audio_path, "Transcribe this audio exactly.", mime_type=mime_type)

        return "Audio transcription not available (configure VAPI or Gemini provider)."

    async def health_check(self) -> bool:
        """Check if the inference service is reachable."""
        provider = self.config.get("INFERENCE_PROVIDER", self.provider)
        if provider == "ollama":
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.endpoint}/api/tags", timeout=5) as resp:
                        return resp.status == 200
            except Exception:
                return False
        return True # Assume others are OK if configured

    async def generate_speech(self, text: str, voice_id: Optional[str] = None) -> Optional[bytes]:
        """
        Generate speech from text using VAPI TTS.

        Args:
            text: Text to synthesize
            voice_id: Voice ID override (default from VAPI config)

        Returns:
            Audio bytes (OGG format for Telegram) or None on failure
        """
        if not self.vapi or not self.vapi.is_valid():
            logger.warning("VAPI not configured for TTS")
            return None

        try:
            voice = voice_id or self.config.get("VAPI_VOICE_ID", "rachel")
            audio_data = await self.vapi.generate_speech(text, voice)
            return audio_data
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            return None
