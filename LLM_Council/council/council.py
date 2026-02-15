"""
LLM Council - Main orchestration logic.
Coordinates multiple LLMs through deliberation stages.
"""

import asyncio
import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from .providers import (
    BaseProvider,
    GeminiProvider,
    GitHubCopilotProvider,
    NVIDIANIMProvider,
    OpenAIProvider,
    ProviderResponse,
)
from .providers.base import PeerReview

logger = logging.getLogger(__name__)


@dataclass
class CouncilSession:
    """Represents a council deliberation session."""

    session_id: str
    query: str
    timestamp: datetime = field(default_factory=datetime.now)
    stage1_responses: list[ProviderResponse] = field(default_factory=list)
    stage2_reviews: list[PeerReview] = field(default_factory=list)
    stage3_consensus: Optional[str] = None
    chairman_provider: str = ""

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "query": self.query,
            "timestamp": self.timestamp.isoformat(),
            "stage1_responses": [r.to_dict() for r in self.stage1_responses],
            "stage2_reviews": [
                {
                    "reviewer": r.reviewer,
                    "reviewee": r.reviewee,
                    "score": r.score,
                    "strengths": r.strengths,
                    "weaknesses": r.weaknesses,
                    "commentary": r.commentary,
                }
                for r in self.stage2_reviews
            ],
            "stage3_consensus": self.stage3_consensus,
            "chairman_provider": self.chairman_provider,
        }

    def save(self, path: Path):
        """Save session to JSON file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)


class LLMCouncil:
    """
    Multi-LLM Council for deliberative AI responses.

    Stages:
    1. Individual Responses - Each LLM answers independently
    2. Peer Review - LLMs evaluate each other's responses
    3. Consensus - Chairman synthesizes final answer
    """

    def __init__(
        self,
        providers: list[BaseProvider],
        chairman: Optional[BaseProvider] = None,
        enable_peer_review: bool = True,
        history_dir: Optional[str] = None,
    ):
        self.providers = providers
        self.chairman = chairman or (providers[0] if providers else None)
        self.enable_peer_review = enable_peer_review
        self.history_dir = Path(history_dir) if history_dir else None
        self._session_counter = 0

    @classmethod
    def from_env(cls, env_path: str = ".env") -> "LLMCouncil":
        """Create council from environment variables."""
        from dotenv import load_dotenv

        load_dotenv(env_path, override=True)

        providers = []

        # OpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "sk-your-key-here":
            providers.append(
                OpenAIProvider(
                    api_key=openai_key,
                    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
                    store=os.getenv("OPENAI_STORE", "false").lower() == "true",
                )
            )
            logger.info("✓ OpenAI provider initialized")

        # GitHub Copilot
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token and github_token != "ghp_your-token-here":
            providers.append(
                GitHubCopilotProvider(api_key=github_token, model=os.getenv("GITHUB_COPILOT_MODEL", "gpt-4o"))
            )
            logger.info("✓ GitHub Copilot provider initialized")

        # NVIDIA NIM
        nvidia_key = os.getenv("NVIDIA_API_KEY")
        if nvidia_key and nvidia_key != "nvapi-your-key-here":
            providers.append(
                NVIDIANIMProvider(api_key=nvidia_key, model=os.getenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct"))
            )
            logger.info("✓ NVIDIA NIM provider initialized")

        # Gemini
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if gemini_key:
            providers.append(
                GeminiProvider(
                    api_key=gemini_key,
                    model=os.getenv("GEMINI_TEXT_MODEL", "models/gemini-2.0-flash"),
                )
            )
            logger.info("✓ Gemini provider initialized")

        if not providers:
            raise ValueError("No valid API keys found. Check your .env file.")

        # Provider ordering + chairman selection
        order_raw = os.getenv("COUNCIL_PROVIDER_ORDER", "gemini,openai,github,nvidia")
        order = [v.strip().lower() for v in order_raw.split(",") if v.strip()]
        if order:
            ordered = []
            remaining = providers[:]
            for name in order:
                for p in list(remaining):
                    if p.name == name or name in p.name:
                        ordered.append(p)
                        remaining.remove(p)
            ordered.extend(remaining)
            providers = ordered

        chairman_provider = os.getenv("CHAIRMAN_PROVIDER")
        chairman = None
        if chairman_provider:
            for p in providers:
                if p.name == chairman_provider or chairman_provider in p.name:
                    chairman = p
                    break
        if chairman is None and providers:
            chairman = providers[0]

        return cls(
            providers=providers,
            chairman=chairman,
            enable_peer_review=os.getenv("ENABLE_PEER_REVIEW", "true").lower() == "true",
            history_dir=os.getenv("HISTORY_DIR"),
        )

    @classmethod
    def from_token_broker(cls, broker, tier: Optional[str] = None) -> "LLMCouncil":
        """Create council using keys from TokenBroker."""
        providers = []

        # Gemini
        gemini_key = broker.get_key("gemini", tier=tier)
        if gemini_key:
            providers.append(
                GeminiProvider(
                    api_key=gemini_key,
                    model=os.getenv("GEMINI_TEXT_MODEL", "models/gemini-2.0-flash"),
                )
            )
            logger.info(f"✓ Gemini provider initialized via TokenBroker (Tier: {tier})")
        else:
            logger.warning(f"TokenBroker returned no key for Gemini (Tier: {tier})")

        # OpenAI (fallback)
        openai_key = broker.get_key("openai", tier=tier)
        if openai_key:
            providers.append(
                OpenAIProvider(
                    api_key=openai_key,
                    model="gpt-4o",  # Default high quality
                    store=False,
                )
            )
            logger.info(f"✓ OpenAI provider initialized via TokenBroker (Tier: {tier})")
        else:
            logger.warning(f"TokenBroker returned no key for OpenAI (Tier: {tier})")

        if not providers:
            raise ValueError("TokenBroker returned no valid keys for supported providers.")

        # Provider ordering + chairman selection
        order_raw = os.getenv("COUNCIL_PROVIDER_ORDER", "gemini,openai,github,nvidia")
        order = [v.strip().lower() for v in order_raw.split(",") if v.strip()]
        if order:
            ordered = []
            remaining = providers[:]
            for name in order:
                for p in list(remaining):
                    if p.name == name or name in p.name:
                        ordered.append(p)
                        remaining.remove(p)
            ordered.extend(remaining)
            providers = ordered

        chairman_provider = os.getenv("CHAIRMAN_PROVIDER")
        chairman = None
        if chairman_provider:
            for p in providers:
                if p.name == chairman_provider or chairman_provider in p.name:
                    chairman = p
                    break
        if chairman is None and providers:
            chairman = providers[0]

        return cls(providers=providers, chairman=chairman, enable_peer_review=True)

    async def deliberate(self, query: str, system_prompt: str = "", verbose: bool = False) -> CouncilSession:
        """
        Run full council deliberation on a query.

        Returns CouncilSession with all stages' results.
        """
        self._session_counter += 1
        session = CouncilSession(
            session_id=f"council-{self._session_counter}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            query=query,
        )

        if verbose:
            logger.info(f"\n{'=' * 60}")
            logger.info(f"🏛️ COUNCIL SESSION: {session.session_id}")
            logger.info(f"📝 Query: {query[:100]}...")
            logger.info(f"{'=' * 60}\n")

        # ===== STAGE 1: Individual Responses =====
        if verbose:
            logger.info("📊 STAGE 1: Gathering individual responses...")

        session.stage1_responses = await self._stage1_individual_responses(query, system_prompt, verbose)

        # ===== STAGE 2: Peer Review =====
        if self.enable_peer_review and len(session.stage1_responses) > 1:
            if verbose:
                logger.info("\n🔍 STAGE 2: Peer review in progress...")

            session.stage2_reviews = await self._stage2_peer_review(query, session.stage1_responses, verbose)

        # ===== STAGE 3: Chairman Consensus =====
        if verbose:
            logger.info("\n👑 STAGE 3: Chairman synthesizing consensus...")

        session.stage3_consensus = await self._stage3_consensus(query, session, verbose)
        session.chairman_provider = self.chairman.name if self.chairman else "none"

        # Save history
        if self.history_dir:
            session.save(self.history_dir / f"{session.session_id}.json")

        return session

    async def _stage1_individual_responses(
        self, query: str, system_prompt: str, verbose: bool
    ) -> list[ProviderResponse]:
        """Stage 1: Get independent responses from all providers."""

        async def get_response(provider: BaseProvider) -> ProviderResponse:
            if verbose:
                logger.info(f"  → Querying {provider.name} ({provider.model})...")
            response = await provider.generate(query, system_prompt)
            if verbose:
                status = "✓" if response.success else "✗"
                logger.info(f"  {status} {provider.name}: {len(response.content)} chars, {response.latency_ms:.0f}ms")
            return response

        # Query all providers in parallel
        tasks = [get_response(p) for p in self.providers]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # Filter out exceptions
        valid_responses = []
        for r in responses:
            if isinstance(r, ProviderResponse):
                valid_responses.append(r)
            elif isinstance(r, Exception):
                logger.error(f"Provider error: {r}")

        return valid_responses

    async def _stage2_peer_review(
        self, query: str, responses: list[ProviderResponse], verbose: bool
    ) -> list[PeerReview]:
        """Stage 2: Each provider reviews the others' responses."""
        reviews = []

        for reviewer in self.providers:
            for response in responses:
                if response.provider_name != reviewer.name:
                    if verbose:
                        logger.info(f"  → {reviewer.name} reviewing {response.provider_name}...")

                    try:
                        review = await reviewer.peer_review(query, response, [r for r in responses if r != response])
                        reviews.append(review)
                        if verbose:
                            logger.info(f"    Score: {review.score}/10")
                    except Exception as e:
                        logger.error(f"Review failed: {e}")

        return reviews

    async def _stage3_consensus(self, query: str, session: CouncilSession, verbose: bool) -> str:
        """Stage 3: Chairman synthesizes consensus from all responses and reviews."""
        if not self.chairman:
            # Fallback: return best-scored response
            if session.stage2_reviews:
                scores = {}
                for review in session.stage2_reviews:
                    scores[review.reviewee] = scores.get(review.reviewee, []) + [review.score]
                avg_scores = {k: sum(v) / len(v) for k, v in scores.items()}
                best = max(avg_scores, key=avg_scores.get)
                for r in session.stage1_responses:
                    if r.provider_name == best:
                        return r.content
            return session.stage1_responses[0].content if session.stage1_responses else ""

        # Build synthesis prompt
        synthesis_prompt = self._build_synthesis_prompt(query, session)

        if verbose:
            logger.info(f"  → {self.chairman.name} synthesizing final response...")

        response = await self.chairman.generate(
            synthesis_prompt,
            system_prompt="""You are the Chairman of an LLM Council. Your role is to:
1. Analyze all council members' responses
2. Consider peer review feedback
3. Synthesize the best possible comprehensive answer
4. Resolve any conflicts or contradictions
5. Provide a clear, well-structured final response

Output ONLY the final synthesized answer, not meta-commentary about the process.""",
        )

        return response.content

    def _build_synthesis_prompt(self, query: str, session: CouncilSession) -> str:
        """Build the synthesis prompt for the Chairman."""
        prompt = f"""# COUNCIL DELIBERATION SYNTHESIS

## Original Query
{query}

## Council Member Responses
"""

        for i, response in enumerate(session.stage1_responses, 1):
            prompt += f"""
### Response {i} (from {response.provider_name}, {response.model})
{response.content}

"""

        if session.stage2_reviews:
            prompt += "\n## Peer Review Summary\n"

            # Group reviews by reviewee
            by_reviewee = {}
            for review in session.stage2_reviews:
                if review.reviewee not in by_reviewee:
                    by_reviewee[review.reviewee] = []
                by_reviewee[review.reviewee].append(review)

            for reviewee, reviews in by_reviewee.items():
                avg_score = sum(r.score for r in reviews) / len(reviews)
                prompt += f"\n**{reviewee}** - Average Score: {avg_score:.1f}/10\n"
                for r in reviews:
                    prompt += f"- {r.reviewer}: {r.score}/10\n"
                    if r.strengths:
                        prompt += f"  Strengths: {', '.join(r.strengths[:2])}\n"
                    if r.weaknesses:
                        prompt += f"  Weaknesses: {', '.join(r.weaknesses[:2])}\n"

        prompt += """
## Your Task
Synthesize a comprehensive final answer that:
1. Incorporates the best insights from all responses
2. Addresses any weaknesses identified in reviews
3. Resolves any contradictions
4. Provides a clear, actionable response

Provide the final answer now:"""

        return prompt

    async def health_check(self) -> dict[str, bool]:
        """Check health of all providers."""
        results = {}
        for provider in self.providers:
            results[provider.name] = await provider.health_check()
        return results

    async def close(self):
        """Cleanup all providers."""
        for provider in self.providers:
            await provider.close()
