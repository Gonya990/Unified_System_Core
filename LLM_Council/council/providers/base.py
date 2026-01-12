"""
Base Provider Interface for LLM Council.
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ProviderResponse:
    """Response from an LLM provider."""

    provider_name: str
    model: str
    content: str
    latency_ms: float = 0.0
    tokens_used: int = 0
    error: Optional[str] = None
    metadata: dict = field(default_factory=dict)

    @property
    def success(self) -> bool:
        return self.error is None and bool(self.content)

    def to_dict(self) -> dict:
        return {
            "provider": self.provider_name,
            "model": self.model,
            "content": self.content,
            "latency_ms": self.latency_ms,
            "tokens_used": self.tokens_used,
            "error": self.error,
            "success": self.success,
            "metadata": self.metadata,
        }


@dataclass
class PeerReview:
    """Peer review result from one LLM evaluating another's response."""

    reviewer: str  # Who reviewed
    reviewee: str  # Whose response was reviewed
    score: float   # 1-10
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    commentary: str = ""


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""

    name: str = "base"

    def __init__(self, api_key: str, model: str, base_url: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self._client = None

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = "") -> ProviderResponse:
        """Generate a response from the LLM."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the provider is reachable."""
        pass

    async def peer_review(
        self,
        original_query: str,
        response_to_review: ProviderResponse,
        other_responses: list[ProviderResponse]
    ) -> PeerReview:
        """
        Review another LLM's response.
        Default implementation uses generate() with a review prompt.
        """
        review_prompt = f"""You are reviewing an AI response to evaluate its quality.

ORIGINAL QUESTION:
{original_query}

RESPONSE TO REVIEW (from {response_to_review.provider_name}):
{response_to_review.content}

OTHER RESPONSES FOR COMPARISON:
"""
        for i, resp in enumerate(other_responses, 1):
            if resp.provider_name != response_to_review.provider_name:
                review_prompt += f"\n[Response {i} from {resp.provider_name}]:\n{resp.content[:500]}...\n"

        review_prompt += """

Evaluate the response to review. Provide:
1. SCORE: A number from 1-10 (10 = excellent)
2. STRENGTHS: List 2-3 strong points
3. WEAKNESSES: List 2-3 areas for improvement
4. COMMENTARY: Brief overall assessment

Format your response as:
SCORE: [number]
STRENGTHS:
- [point 1]
- [point 2]
WEAKNESSES:
- [point 1]
- [point 2]
COMMENTARY: [your assessment]
"""

        result = await self.generate(review_prompt, system_prompt="You are an expert AI evaluator.")

        # Parse the review (simplified parsing)
        review = PeerReview(
            reviewer=self.name,
            reviewee=response_to_review.provider_name,
            score=7.0,  # Default score
            commentary=result.content
        )

        # Try to extract score
        import re
        score_match = re.search(r"SCORE:\s*(\d+(?:\.\d+)?)", result.content)
        if score_match:
            review.score = float(score_match.group(1))

        # Extract strengths
        strengths_match = re.search(r"STRENGTHS:(.*?)(?:WEAKNESSES:|$)", result.content, re.DOTALL)
        if strengths_match:
            review.strengths = [s.strip().lstrip("- ") for s in strengths_match.group(1).strip().split("\n") if s.strip()]

        # Extract weaknesses
        weaknesses_match = re.search(r"WEAKNESSES:(.*?)(?:COMMENTARY:|$)", result.content, re.DOTALL)
        if weaknesses_match:
            review.weaknesses = [w.strip().lstrip("- ") for w in weaknesses_match.group(1).strip().split("\n") if w.strip()]

        return review

    def _measure_time(self):
        """Context manager for measuring response time."""
        return _TimeMeasure()

    async def close(self):
        """Cleanup resources."""
        if hasattr(self._client, 'close'):
            await self._client.close()


class _TimeMeasure:
    """Simple time measurement context manager."""

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    @property
    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self.start) * 1000

    def __exit__(self, *args):
        pass
