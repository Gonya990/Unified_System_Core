"""
OpenAI Provider for LLM Council.
Supports GPT-4o, GPT-4-turbo, o1, etc.
"""

import logging
from typing import Optional
from openai import AsyncOpenAI

from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseProvider):
    """OpenAI API provider (GPT-4o, GPT-4-turbo, o1)."""
    
    name = "openai"
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        store: bool = False
    ):
        super().__init__(api_key, model, base_url)
        self.store = store
        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
    
    async def generate(self, prompt: str, system_prompt: str = "") -> ProviderResponse:
        """Generate response using OpenAI Chat Completions API."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        with self._measure_time() as timer:
            try:
                # Build request params
                params = {
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 2000,
                }
                
                # Add store parameter if enabled (for conversation history)
                if self.store:
                    params["store"] = True
                
                response = await self._client.chat.completions.create(**params)
                
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
                logger.error(f"OpenAI error: {e}")
                return ProviderResponse(
                    provider_name=self.name,
                    model=self.model,
                    content="",
                    latency_ms=getattr(timer, 'elapsed_ms', 0),
                    error=str(e)
                )
    
    async def health_check(self) -> bool:
        """Check if OpenAI API is reachable."""
        try:
            # List models to verify API key works
            models = await self._client.models.list()
            return True
        except Exception as e:
            logger.warning(f"OpenAI health check failed: {e}")
            return False
    
    async def list_models(self) -> list[str]:
        """List available OpenAI models."""
        try:
            response = await self._client.models.list()
            return [m.id for m in response.data if "gpt" in m.id.lower()]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"]
    
    async def close(self):
        """Close the client."""
        await self._client.close()
