"""
NVIDIA NIM Provider for LLM Council.
Supports Llama, Mixtral, Nemotron via NVIDIA's API.
"""

import logging
from typing import Optional

from openai import AsyncOpenAI

from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class NVIDIANIMProvider(BaseProvider):
    """NVIDIA NIM API provider (Llama, Mixtral, Nemotron)."""

    name = "nvidia_nim"

    # NVIDIA NIM API is OpenAI-compatible
    DEFAULT_BASE_URL = "https://integrate.api.nvidia.com/v1"

    # Popular NVIDIA NIM models
    AVAILABLE_MODELS = [
        "meta/llama-3.1-70b-instruct",
        "meta/llama-3.1-8b-instruct",
        "meta/llama-3.2-3b-instruct",
        "mistralai/mixtral-8x7b-instruct-v0.1",
        "mistralai/mistral-7b-instruct-v0.3",
        "nvidia/nemotron-4-340b-instruct",
        "google/gemma-2-27b-it",
    ]

    def __init__(
        self,
        api_key: str,
        model: str = "meta/llama-3.1-70b-instruct",
        base_url: Optional[str] = None
    ):
        super().__init__(api_key, model, base_url or self.DEFAULT_BASE_URL)

        # Use OpenAI client since NVIDIA NIM is OpenAI-compatible
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=self.base_url
        )

    async def generate(self, prompt: str, system_prompt: str = "") -> ProviderResponse:
        """Generate response using NVIDIA NIM API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        with self._measure_time() as timer:
            try:
                response = await self._client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2000,
                )

                content = response.choices[0].message.content or ""
                tokens = response.usage.total_tokens if response.usage else 0

                return ProviderResponse(
                    provider_name=self.name,
                    model=self.model,
                    content=content,
                    latency_ms=timer.elapsed_ms,
                    tokens_used=tokens,
                    metadata={
                        "completion_id": response.id,
                        "finish_reason": response.choices[0].finish_reason,
                    }
                )

            except Exception as e:
                logger.error(f"NVIDIA NIM error: {e}")
                return ProviderResponse(
                    provider_name=self.name,
                    model=self.model,
                    content="",
                    latency_ms=getattr(timer, 'elapsed_ms', 0),
                    error=str(e)
                )

    async def health_check(self) -> bool:
        """Check if NVIDIA NIM API is reachable."""
        try:
            # Test with a simple completion
            await self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.warning(f"NVIDIA NIM health check failed: {e}")
            return False

    @classmethod
    def list_available_models(cls) -> list[str]:
        """List known NVIDIA NIM models."""
        return cls.AVAILABLE_MODELS.copy()

    async def close(self):
        """Close the client."""
        await self._client.close()
