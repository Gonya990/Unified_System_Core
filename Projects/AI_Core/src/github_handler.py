import logging

import aiohttp

logger = logging.getLogger(__name__)

class GitHubHandler:
    """Helper to interact with GitHub API (create issues, etc.)."""

    def __init__(
        self,
        token: str,
        repo: str = "Unified-system-Core/Unified_System_Core"
    ):
        self.token = token
        self.repo = repo
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def create_issue(self, title: str, body: str, labels: list = None) -> bool:
        """Create a new issue in the repository."""
        if not self.token:
            logger.warning("No GITHUB_TOKEN provided, skipping issue creation.")
            return False

        url = f"{self.base_url}/repos/{self.repo}/issues"
        payload = {
            "title": title,
            "body": body,
            "labels": labels or ["bug", "self-healing"]
        }

        try:
            async with aiohttp.ClientSession(headers=self.headers) as session:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 201:
                        data = await resp.json()
                        logger.info(f"Created GitHub Issue: {data.get('html_url')}")
                        return True
                    else:
                        text = await resp.text()
                        logger.error(
                            f"Failed to create GitHub Issue: {resp.status} - {text}"
                        )
                        return False
        except Exception as e:
            logger.error(f"Error communicating with GitHub: {e}")
            return False
