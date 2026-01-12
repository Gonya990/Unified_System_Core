"""
Chairman Module - The synthesis leader of the LLM Council.

The Chairman is responsible for:
1. Analyzing all council member responses
2. Weighing peer review feedback
3. Synthesizing the final consensus
4. Resolving conflicts between different perspectives
"""

import logging
from dataclasses import dataclass
from typing import Optional

from .providers import BaseProvider, ProviderResponse

logger = logging.getLogger(__name__)


@dataclass
class ConsensusResult:
    """Result of chairman synthesis."""

    final_response: str
    confidence_score: float  # 0-1
    key_insights: list[str]
    resolved_conflicts: list[str]
    sources_used: list[str]  # Which providers contributed


class Chairman:
    """
    👑 Chairman LLM - Leads the council and synthesizes consensus.

    The Chairman role is typically filled by the most capable model
    (e.g., GPT-4o, Claude-3.5) to ensure high-quality synthesis.
    """

    SYNTHESIS_SYSTEM_PROMPT = """You are the Chairman of an LLM Council - a panel of AI experts deliberating on user queries.

Your responsibilities:
1. ANALYZE all council member responses objectively
2. WEIGH the peer review feedback to identify strengths and weaknesses
3. SYNTHESIZE a comprehensive answer that combines the best elements
4. RESOLVE any conflicts or contradictions between responses
5. ENHANCE with any additional insights you can provide

Guidelines:
- Give more weight to responses with higher peer review scores
- Don't just pick one response - create a synthesis
- Be direct and actionable in your final answer
- Maintain a professional but approachable tone
- If council members disagree on facts, acknowledge the uncertainty
- Add your own expertise where it enhances the answer

Output format: Provide ONLY the final synthesized answer. Do not include meta-commentary about the council process unless specifically asked."""

    def __init__(self, provider: BaseProvider):
        """Initialize chairman with a provider."""
        self.provider = provider
        self.name = f"Chairman ({provider.name})"

    async def synthesize(
        self,
        query: str,
        responses: list[ProviderResponse],
        reviews: Optional[list] = None,
        detailed: bool = False
    ) -> ConsensusResult:
        """
        Synthesize final consensus from council responses.

        Args:
            query: Original user query
            responses: List of responses from council members
            reviews: Optional peer review data
            detailed: Whether to include detailed breakdown

        Returns:
            ConsensusResult with final response and metadata
        """
        # Build synthesis prompt
        prompt = self._build_prompt(query, responses, reviews, detailed)

        logger.info(f"👑 {self.name} synthesizing consensus...")

        # Generate synthesis
        result = await self.provider.generate(
            prompt,
            system_prompt=self.SYNTHESIS_SYSTEM_PROMPT
        )

        if not result.success:
            logger.error(f"Chairman synthesis failed: {result.error}")
            # Fallback to best response
            return ConsensusResult(
                final_response=self._fallback_response(responses, reviews),
                confidence_score=0.5,
                key_insights=[],
                resolved_conflicts=[],
                sources_used=[responses[0].provider_name] if responses else []
            )

        # Extract insights if detailed mode
        insights = []
        conflicts = []
        if detailed:
            insights, conflicts = self._extract_meta(result.content)

        return ConsensusResult(
            final_response=result.content,
            confidence_score=self._calculate_confidence(responses, reviews),
            key_insights=insights,
            resolved_conflicts=conflicts,
            sources_used=[r.provider_name for r in responses if r.success]
        )

    def _build_prompt(
        self,
        query: str,
        responses: list[ProviderResponse],
        reviews: Optional[list],
        detailed: bool
    ) -> str:
        """Build the synthesis prompt."""

        prompt = f"""# COUNCIL DELIBERATION

## User Query
{query}

## Council Member Responses
"""

        for _i, resp in enumerate(responses, 1):
            status = "✓" if resp.success else "✗"
            prompt += f"""
### [{status}] Response from {resp.provider_name} ({resp.model})
{resp.content if resp.success else f"[Error: {resp.error}]"}
"""

        if reviews:
            prompt += "\n## Peer Review Scores\n"
            # Aggregate scores per provider
            scores = {}
            for r in reviews:
                if r.reviewee not in scores:
                    scores[r.reviewee] = []
                scores[r.reviewee].append(r.score)

            for provider, provider_scores in scores.items():
                avg = sum(provider_scores) / len(provider_scores)
                prompt += f"- **{provider}**: {avg:.1f}/10 (from {len(provider_scores)} reviewers)\n"

        if detailed:
            prompt += """

## Additional Instructions
In your synthesis, please also briefly note:
1. Key insights that emerged from multiple responses
2. Any conflicts you resolved and how
"""

        prompt += "\n## Synthesize your final answer now:"

        return prompt

    def _fallback_response(
        self,
        responses: list[ProviderResponse],
        reviews: Optional[list]
    ) -> str:
        """Get best response as fallback when synthesis fails."""
        successful = [r for r in responses if r.success]
        if not successful:
            return "[Council Error: No valid responses received]"

        if reviews:
            # Pick highest-scored response
            scores = {}
            for r in reviews:
                if r.reviewee not in scores:
                    scores[r.reviewee] = []
                scores[r.reviewee].append(r.score)

            avg_scores = {k: sum(v)/len(v) for k, v in scores.items()}
            best_provider = max(avg_scores, key=avg_scores.get)

            for resp in successful:
                if resp.provider_name == best_provider:
                    return resp.content

        return successful[0].content

    def _calculate_confidence(
        self,
        responses: list[ProviderResponse],
        reviews: Optional[list]
    ) -> float:
        """Calculate confidence score for the consensus."""
        if not responses:
            return 0.0

        success_rate = len([r for r in responses if r.success]) / len(responses)

        if not reviews:
            return success_rate * 0.7  # Lower confidence without reviews

        # Factor in review scores
        all_scores = [r.score for r in reviews]
        if all_scores:
            avg_score = sum(all_scores) / len(all_scores) / 10  # Normalize to 0-1
            return (success_rate * 0.4) + (avg_score * 0.6)

        return success_rate * 0.7

    def _extract_meta(self, content: str) -> tuple[list[str], list[str]]:
        """Extract key insights and resolved conflicts from response."""
        insights = []
        conflicts = []

        # Simple extraction (could be enhanced with structured output)
        lines = content.split("\n")
        in_insights = False
        in_conflicts = False

        for line in lines:
            line_lower = line.lower()
            if "key insight" in line_lower or "important point" in line_lower:
                in_insights = True
                in_conflicts = False
            elif "conflict" in line_lower or "disagreement" in line_lower:
                in_conflicts = True
                in_insights = False
            elif line.strip().startswith("-") or line.strip().startswith("•"):
                if in_insights:
                    insights.append(line.strip().lstrip("-•").strip())
                elif in_conflicts:
                    conflicts.append(line.strip().lstrip("-•").strip())

        return insights[:5], conflicts[:3]
