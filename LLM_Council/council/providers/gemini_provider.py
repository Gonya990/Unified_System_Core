"""
Gemini Provider for LLM Council using the modern google-genai SDK.
Supports Gemini 2.0 Flash, Pro, and experimental models.
"""

import asyncio
import logging
import os
from typing import Optional
from google import genai
from google.genai import types

from .base import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


class GeminiProvider(BaseProvider):
    """Google Gemini API provider (Gemini 2.0 Flash, Pro)."""

    name = "gemini"

    def __init__(self, api_key: str, model: str = "models/gemini-2.0-flash", base_url: Optional[str] = None):
        super().__init__(api_key, model, base_url)
        self._model_name = model
        self._client = genai.Client(api_key=api_key)

    async def generate(self, prompt: str, system_prompt: str = "") -> ProviderResponse:
        """Generate response with fallback logic for models."""
        models_to_try = [
            self._model_name,
            "gemini-2.0-flash",
            "gemini-2.0-pro-exp-02-05", # Newest Pro Experimental
            "gemini-2.0-flash-lite-preview-02-05", # Newest Flash Lite
            "gemini-1.5-pro",
            "gemini-1.5-flash",
        ]

        last_error = None
        for m_name in models_to_try:
            # Ensure model name format is correct for the SDK (stripping /models if present for candidates)
            exec_model = m_name.replace("models/", "")
            
            with self._measure_time() as timer:
                try:
                    loop = asyncio.get_event_loop()
                    
                    config = types.GenerateContentConfig(
                        system_instruction=system_prompt if system_prompt else None,
                        temperature=0.7,
                    )

                    response = await loop.run_in_executor(
                        None,
                        lambda: self._client.models.generate_content(
                            model=exec_model,
                            contents=prompt,
                            config=config
                        ),
                    )
                    
                    content = getattr(response, "text", None)
                    if not content and getattr(response, "candidates", None):
                        # Extract from candidates if .text is missing/blocked
                        candidate = response.candidates[0]
                        if candidate.content and candidate.content.parts:
                            content = "".join([part.text for part in candidate.content.parts if part.text])

                    if not content:
                        raise ValueError("Empty response from Gemini")

                    return ProviderResponse(
                        provider_name=self.name,
                        model=exec_model,
                        content=content.strip(),
                        latency_ms=timer.elapsed_ms,
                        tokens_used=0, # SDK doesn't always expose this easily without extra calls
                        metadata={
                            "requested_model": self._model_name,
                            "actual_model": exec_model,
                            "finish_reason": str(response.candidates[0].finish_reason) if response.candidates else "unknown"
                        },
                    )
                except Exception as e:
                    last_error = e
                    err_str = str(e).lower()
                    if "429" in err_str or "quota" in err_str:
                        logger.warning(f"Gemini {exec_model} rate limited, trying next...")
                        continue
                    elif "404" in err_str or "not found" in err_str:
                        logger.warning(f"Gemini {exec_model} not found, trying next...")
                        continue
                    else:
                        logger.error(f"Gemini {exec_model} error: {last_error}")
                        continue

        return ProviderResponse(
            provider_name=self.name,
            model=self.model,
            content="",
            latency_ms=0,
            error=str(last_error) or "All Gemini models failed",
        )

    async def health_check(self) -> bool:
        """Check if Gemini API is reachable."""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._client.models.generate_content(
                    model=self._model_name.replace("models/", ""),
                    contents="ping",
                    config=types.GenerateContentConfig(max_output_tokens=1),
                ),
            )
            return True
        except Exception as e:
            logger.warning(f"Gemini health check failed: {e}")
            return False

    async def close(self):
        """Cleanup resources."""
        pass

