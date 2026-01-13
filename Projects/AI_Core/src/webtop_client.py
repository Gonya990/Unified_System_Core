import logging
import os
import requests
from typing import Any, Optional, List, Dict

logger = logging.getLogger(__name__)


class WebtopClient:
    """
    Client for Webtop (SmartSchool) school management system.
    Authentication via pre-authenticated token from Webtop.
    """

    BASE_URL = "https://webtop.smartschool.co.il"

    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("WEBTOP_TOKEN")
        self.session = requests.Session()
        self.student_id = None

        if self.token:
            self._setup_session()

    def is_valid(self) -> bool:
        """Check if client has a token."""
        return bool(self.token)

    def _setup_session(self):
        """Configure session with auth headers/cookies."""
        self.session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "X-Requested-With": "XMLHttpRequest",  # Crucial for some IIS/ASP.NET APIs
            }
        )
        # Set auth cookie
        self.session.cookies.set("SmartSchool-Auth", self.token, domain="webtop.smartschool.co.il")

    def check_auth(self) -> bool:
        """Verify authentication by accessing the dashboard."""
        try:
            res = self.session.get(f"{self.BASE_URL}/dashboard")
            # If redirected to login, auth is invalid
            if "login" in res.url.lower():
                return False
            return res.status_code == 200
        except Exception as e:
            logger.error(f"Webtop auth check failed: {e}")
            return False

    def fetch_homework(self) -> Optional[list[dict[str, Any]]]:
        """Fetch homework assignments."""
        if not self.is_valid():
            return None

        # Based on successful verification, the Dashboard is accessible.
        # However, external scripts showed /api/Student/GetHomework returns HTML.
        # This implies it might require specific headers or extracting from Dashboard HTML.
        # For a robust solution, we'll try the API with X-Requested-With first.

        try:
            # Try 1: Standard API with X-Requested-With
            url = f"{self.BASE_URL}/api/Student/GetHomework"
            res = self.session.get(url)

            if res.status_code == 200:
                try:
                    return res.json()
                except ValueError:
                    pass  # Not JSON

            # Try 2: Mobile API?
            # url = f"{self.BASE_URL}/api/mobile/GetStudentHomework"
            # res = self.session.get(url)
            # ...

            # If we reach here, we couldn't get JSON.
            # We might just report "Check Webtop" for now until we can parse the HTML SPA state.
            return []

        except Exception as e:
            logger.error(f"Fetch homework failed: {e}")
            return None

    def fetch_grades(self) -> Optional[list[dict[str, Any]]]:
        """Fetch grades."""
        if not self.is_valid():
            return None

        try:
            url = f"{self.BASE_URL}/api/Student/GetGrades"
            res = self.session.get(url)
            if res.status_code == 200:
                try:
                    return res.json()
                except ValueError:
                    return []
            return None
        except Exception as e:
            logger.error(f"Fetch grades failed: {e}")
            return None
