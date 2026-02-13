"""
Agent Orchestrator - Manages specialized AI agents for code tasks.
Integrates with .claude/agents/ definitions and InferenceClient.
"""

import asyncio
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for a single agent."""

    name: str
    description: str
    system_prompt: str
    category: str
    color: str = "blue"
    tools: list[str] = field(default_factory=list)
    skills: list[str] = field(default_factory=list)
    time_budget: int = 30  # seconds

    @property
    def short_description(self) -> str:
        """First line of description."""
        return self.description.split("\n")[0].strip()


class AgentOrchestrator:
    """
    Orchestrates specialized AI agents loaded from .claude/agents/ directory.
    Supports single agent execution, pipelines, and parallel execution.
    """

    AGENTS_DIR = Path(__file__).parent.parent.parent.parent / ".claude" / "agents"

    # Category mappings for quick lookup
    CATEGORIES = {
        "discovery": ["code-explorer", "api-discoverer", "dependency-mapper"],
        "architecture": ["code-architect", "hexagonal-architecture-guardian", "performance-optimizer"],
        "implementation": ["implementer", "bug-fixer"],
        "review": ["code-reviewer"],
        "testing": ["tdd-cycle-driver"],
        "workflow": ["feedback-loop-optimizer"],
        "coordination": ["code-quality-coordinator", "devops-workflow-orchestrator"],
        "devops": ["performance-optimization-worker", "security-hardening-worker"],
        "ui-ux": ["senior-ui-ux-designer"],
    }

    def __init__(self, inference_client):
        """
        Initialize orchestrator with inference client.

        Args:
            inference_client: InferenceClient instance for LLM calls
        """
        self.inference = inference_client
        self.agents: dict[str, AgentConfig] = {}
        self._load_agents()

    def _load_agents(self) -> None:
        """Load all agent configurations from .claude/agents/ directory."""
        if not self.AGENTS_DIR.exists():
            logger.warning(f"Agents directory not found: {self.AGENTS_DIR}")
            return

        for md_file in self.AGENTS_DIR.rglob("*.md"):
            if md_file.name == "README.md":
                continue

            try:
                agent = self._parse_agent_file(md_file)
                if agent:
                    self.agents[agent.name] = agent
                    logger.debug(f"Loaded agent: {agent.name}")
            except Exception as e:
                logger.error(f"Failed to load agent from {md_file}: {e}")

        logger.info(f"Loaded {len(self.agents)} agents from {self.AGENTS_DIR}")

    def _parse_agent_file(self, path: Path) -> Optional[AgentConfig]:
        """Parse agent markdown file with YAML frontmatter."""
        content = path.read_text(encoding="utf-8")

        # Extract YAML frontmatter
        frontmatter_match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
        if not frontmatter_match:
            logger.warning(f"No frontmatter found in {path}")
            return None

        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
            system_prompt = frontmatter_match.group(2).strip()
        except yaml.YAMLError as e:
            logger.error(f"YAML parse error in {path}: {e}")
            return None

        # Determine category from path
        category = path.parent.name if path.parent != self.AGENTS_DIR else "general"

        # Extract tools from system prompt
        tools = self._extract_tools(system_prompt)

        # Extract skills from system prompt
        skills = self._extract_skills(system_prompt)

        return AgentConfig(
            name=frontmatter.get("name", path.stem),
            description=frontmatter.get("description", ""),
            system_prompt=system_prompt,
            category=category,
            color=frontmatter.get("color", "blue"),
            tools=tools,
            skills=skills,
        )

    def _extract_tools(self, prompt: str) -> list[str]:
        """Extract allowed tools from agent prompt."""
        tools = []
        # Look for tools section
        if "✓ Read" in prompt:
            tools.append("Read")
        if "✓ Grep" in prompt:
            tools.append("Grep")
        if "✓ Glob" in prompt:
            tools.append("Glob")
        if "✓ Bash" in prompt:
            tools.append("Bash")
        if "✓ Write" in prompt or "✓ Edit" in prompt:
            tools.append("Write")
        return tools

    def _extract_skills(self, prompt: str) -> list[str]:
        """Extract activated skills from agent prompt."""
        # Look for skill references
        skill_pattern = r"\*\*`([a-z-]+)`\*\*"
        matches = re.findall(skill_pattern, prompt)
        return list(set(matches))

    def list_agents(self) -> str:
        """Return formatted list of available agents."""
        lines = ["**Available Agents:**\n"]

        for category, agent_names in self.CATEGORIES.items():
            category_agents = [self.agents[name] for name in agent_names if name in self.agents]
            if category_agents:
                lines.append(f"\n**{category.title()}:**")
                for agent in category_agents:
                    lines.append(f"  `{agent.name}` - {agent.short_description[:60]}...")

        return "\n".join(lines)

    def get_agent(self, name: str) -> Optional[AgentConfig]:
        """Get agent by name."""
        return self.agents.get(name)

    def find_agent_for_task(self, task: str) -> Optional[str]:
        """Find best agent for a given task description."""
        task_lower = task.lower()

        # Simple keyword matching
        keywords_to_agents = {
            ("explore", "find", "search", "understand", "analyze"): "code-explorer",
            ("api", "endpoint", "route"): "api-discoverer",
            ("dependency", "import", "module"): "dependency-mapper",
            ("architect", "design", "structure"): "code-architect",
            ("hexagonal", "layer", "boundary"): "hexagonal-architecture-guardian",
            ("performance", "optimize", "slow", "fast"): "performance-optimizer",
            ("implement", "create", "add", "build"): "implementer",
            ("bug", "fix", "error", "issue"): "bug-fixer",
            ("review", "check", "quality"): "code-reviewer",
            ("test", "tdd", "coverage"): "tdd-cycle-driver",
            ("ui", "ux", "design", "interface"): "senior-ui-ux-designer",
            ("security", "vulnerability", "secure"): "security-hardening-worker",
        }

        for keywords, agent_name in keywords_to_agents.items():
            if any(kw in task_lower for kw in keywords):
                if agent_name in self.agents:
                    return agent_name

        return "code-explorer"  # Default fallback

    async def run(self, agent_name: str, task: str, context: str = "") -> str:
        """
        Execute a task using specified agent.

        Args:
            agent_name: Name of the agent to use
            task: Task description
            context: Optional additional context

        Returns:
            Agent's response
        """
        agent = self.agents.get(agent_name)
        if not agent:
            return f"Agent '{agent_name}' not found. Available: {', '.join(self.agents.keys())}"

        logger.info(f"[AGENT] Running {agent_name} with task: {task[:50]}...")

        # Build system prompt with agent instructions
        system_prompt = f"""
{agent.system_prompt}

---
CURRENT TASK: {task}

{f"ADDITIONAL CONTEXT: {context}" if context else ""}

Provide a focused, actionable response. Use code references (file:line) where applicable.
"""

        try:
            response, _ = await self.inference.chat([{"role": "user", "content": task}], system_prompt=system_prompt)
            logger.info(f"[AGENT] {agent_name} completed, response length: {len(response)}")
            return response
        except Exception as e:
            logger.error(f"[AGENT] {agent_name} failed: {e}")
            return f"Agent execution failed: {str(e)}"

    async def run_pipeline(self, tasks: list[tuple[str, str]], initial_context: str = "") -> dict[str, str]:
        """
        Run agents in sequence, passing context between them.

        Args:
            tasks: List of (agent_name, task_description) tuples
            initial_context: Starting context

        Returns:
            Dict mapping agent names to their responses
        """
        results = {}

        for agent_name, task in tasks:
            logger.info(f"[PIPELINE] Stage: {agent_name}")

            # Include previous results as context
            if results:
                context_summary = "\n\n".join([f"[{name}]: {resp[:500]}..." for name, resp in results.items()])
                full_context = f"{initial_context}\n\nPrevious agent results:\n{context_summary}"
            else:
                full_context = initial_context

            result = await self.run(agent_name, task, full_context)
            results[agent_name] = result

        return results

    async def run_parallel(self, tasks: list[tuple[str, str]], context: str = "") -> dict[str, str]:
        """
        Run multiple agents in parallel.

        Args:
            tasks: List of (agent_name, task_description) tuples
            context: Shared context for all agents

        Returns:
            Dict mapping agent names to their responses
        """
        logger.info(f"[PARALLEL] Running {len(tasks)} agents in parallel")

        async def run_single(agent_name: str, task: str) -> tuple[str, str]:
            result = await self.run(agent_name, task, context)
            return agent_name, result

        coroutines = [run_single(name, task) for name, task in tasks]
        results_list = await asyncio.gather(*coroutines, return_exceptions=True)

        results = {}
        for item in results_list:
            if isinstance(item, Exception):
                logger.error(f"[PARALLEL] Agent failed: {item}")
            else:
                agent_name, result = item
                results[agent_name] = result

        return results

    def format_results(self, results: dict[str, str], mode: str = "detailed") -> str:
        """Format agent results for display."""
        if mode == "summary":
            lines = ["**Agent Results Summary:**\n"]
            for agent_name, result in results.items():
                preview = result[:200].replace("\n", " ")
                lines.append(f"**{agent_name}**: {preview}...")
            return "\n".join(lines)
        else:
            lines = []
            for agent_name, result in results.items():
                lines.append(f"## {agent_name}\n")
                lines.append(result)
                lines.append("\n---\n")
            return "\n".join(lines)


# Predefined pipelines for common workflows
PIPELINES = {
    "feature": [
        ("code-explorer", "Understand existing patterns and architecture"),
        ("code-architect", "Design the implementation approach"),
        ("implementer", "Implement the feature with tests"),
        ("code-reviewer", "Review the implementation"),
    ],
    "bugfix": [
        ("code-explorer", "Find the bug location and understand context"),
        ("bug-fixer", "Fix the bug following TDD"),
        ("code-reviewer", "Review the fix"),
    ],
    "refactor": [
        ("code-explorer", "Analyze current implementation"),
        ("code-architect", "Design refactoring approach"),
        ("implementer", "Perform refactoring"),
        ("code-reviewer", "Review changes"),
    ],
    "security": [
        ("code-explorer", "Find security-sensitive code"),
        ("security-hardening-worker", "Identify vulnerabilities"),
        ("code-reviewer", "Review security improvements"),
    ],
}
