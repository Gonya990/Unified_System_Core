"""
Linear API Client for Task Management
Integrates with Linear.app for professional issue tracking.
"""

import logging
import os
from typing import Optional

import requests

logger = logging.getLogger(__name__)


class LinearClient:
    """Client for Linear GraphQL API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("LINEAR_API_KEY")
        self.endpoint = "https://api.linear.app/graphql"
        self.headers = {"Authorization": self.api_key, "Content-Type": "application/json"}
        self.team_id = None  # Will be fetched on first use

    def _query(self, query: str, variables: Optional[dict] = None) -> dict:
        """Execute GraphQL query."""
        try:
            response = requests.post(
                self.endpoint, json={"query": query, "variables": variables or {}}, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                logger.error(f"Linear API errors: {data['errors']}")
                return None

            return data.get("data")
        except Exception as e:
            logger.error(f"Linear API request failed: {e}")
            return None

    def get_viewer(self) -> Optional[dict]:
        """Get current user info."""
        query = """
        query {
            viewer {
                id
                name
                email
            }
        }
        """
        result = self._query(query)
        return result.get("viewer") if result else None

    def get_teams(self) -> list[dict]:
        """Get all teams."""
        query = """
        query {
            teams {
                nodes {
                    id
                    name
                    key
                }
            }
        }
        """
        result = self._query(query)
        if result and "teams" in result:
            return result["teams"]["nodes"]
        return []

    def _ensure_team_id(self):
        """Ensure we have a team ID."""
        if not self.team_id:
            teams = self.get_teams()
            if teams:
                self.team_id = teams[0]["id"]  # Use first team
                logger.info(f"Using Linear team: {teams[0]['name']}")

    def create_issue(self, title: str, description: str = "", priority: int = 0) -> Optional[dict]:
        """
        Create a new issue.

        Args:
            title: Issue title
            description: Issue description
            priority: Priority (0=None, 1=Urgent, 2=High, 3=Normal, 4=Low)
        """
        self._ensure_team_id()

        if not self.team_id:
            logger.error("No team ID available")
            return None

        query = """
        mutation IssueCreate($input: IssueCreateInput!) {
            issueCreate(input: $input) {
                success
                issue {
                    id
                    identifier
                    title
                    url
                }
            }
        }
        """

        variables = {
            "input": {"teamId": self.team_id, "title": title, "description": description, "priority": priority}
        }

        result = self._query(query, variables)
        if result and result.get("issueCreate", {}).get("success"):
            return result["issueCreate"]["issue"]
        return None

    def get_my_issues(self, limit: int = 10) -> list[dict]:
        """Get issues assigned to current user."""
        query = (
            """
        query {
            viewer {
                assignedIssues(first: %d, filter: { state: { type: { nin: ["completed", "canceled"] } } }) {
                    nodes {
                        id
                        identifier
                        title
                        priority
                        state {
                            name
                        }
                        url
                    }
                }
            }
        }
        """
            % limit
        )

        result = self._query(query)
        if result and "viewer" in result:
            return result["viewer"]["assignedIssues"]["nodes"]
        return []

    def update_issue_state(self, issue_id: str, state_id: str) -> bool:
        """Update issue state (e.g., mark as done)."""
        query = """
        mutation IssueUpdate($id: String!, $stateId: String!) {
            issueUpdate(id: $id, input: { stateId: $stateId }) {
                success
            }
        }
        """

        variables = {"id": issue_id, "stateId": state_id}
        result = self._query(query, variables)
        return result and result.get("issueUpdate", {}).get("success", False)
