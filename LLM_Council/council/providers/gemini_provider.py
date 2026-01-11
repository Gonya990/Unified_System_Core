"""
Gemini Provider for LLM Council.
Supports Gemini 2.0 Flash (Nana Banana), Pro, etc.
"""

import logging
import asyncio
from typing import Optional
import google.generativeai as genai

from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)

class GeminiProvider(BaseProvider):
    """Google Gemini API provider (Gemini 2.0 Flash, Pro)."""
    
    name = "gemini"
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "models/gemini-2.0-flash",
        base_url: Optional[str] = None
    ):
        super().__init__(api_key, model, base_url)
        genai.configure(api_key=api_key)
        self._model_name = model
        self._setup_model(model)

    def _setup_model(self, model_name: str):
        """Configure the generative model."""
        self._model = genai.GenerativeModel(model_name)

    async def generate(self, prompt: str, system_prompt: str = "") -> ProviderResponse:
        """Generate response with fallback logic, prioritizing Nana Banana."""
        models_to_try = [
            "models/nano-banana-pro-preview", 
            self._model_name,
            "models/gemini-2.5-pro",
            "models/gemini-2.5-flash",
            "models/gemini-2.0-flash",
            "models/gemini-flash-latest",
            "models/gemini-pro-latest"
        ]
        
        last_error = None
        for m_name in models_to_try:
            with self._measure_time() as timer:
                try:
                    # Setup model if it's a fallback
                    model = genai.GenerativeModel(m_name)
                    
                    full_prompt = prompt
                    if system_prompt:
                        full_prompt = f"SYSTEM: {system_prompt}\n\nUSER: {prompt}"

                    loop = asyncio.get_event_loop()
                    response = await loop.run_in_executor(
                        None, 
                        lambda: model.generate_content(full_prompt)
                    )
                    
                    if not response.text:
                        raise ValueError("Empty response from Gemini")

                    return ProviderResponse(
                        provider_name=self.name,
                        model=m_name,
                        content=response.text,
                        latency_ms=timer.elapsed_ms,
                        tokens_used=0,
                        metadata={
                            "finish_reason": str(response.candidates[0].finish_reason) if response.candidates else "unknown",
                            "requested_model": self._model_name,
                            "actual_model": m_name
                        }
                    )
                except Exception as e:
                    last_error = e
                    if "429" in str(e) or "quota" in str(e).lower():
                        logger.warning(f"Gemini {m_name} rate limited/quota hit, trying next...")
                        continue
                    else:
                        logger.error(f"Gemini {m_name} error: {last_error}")
                        # If it's not a rate limit, maybe try next model anyway? 
                        # Some models might not be enabled.
                        continue

        return ProviderResponse(
            provider_name=self.name,
            model=self.model,
            content="",
            latency_ms=0,
            error=str(last_error) or "All Gemini models failed"
        )

    async def health_check(self) -> bool:
        """Check if Gemini API is reachable."""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._model.generate_content("ping", generation_config={"max_output_tokens": 1})
            )
            return True
        except Exception as e:
            logger.warning(f"Gemini health check failed: {e}")
            return False

    async def close(self):
        """Cleanup resources."""
        pass
