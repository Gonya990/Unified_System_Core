"""
Mashov Integration Client
Provides access to Israeli school management system (Mashov) for homework and grades.
Handles authentication, session caching, and data retrieval with graceful degradation.
"""

import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)

MASHOV_URL = "https://web.mashov.info/api"
YEAR = 2026


class MashovClient:
    """
    Client for Mashov Israeli school management system.
    Provides homework, grades, and student data retrieval with session caching.
    """

    # In-memory session cache with TTL
    _session_cache = {}

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        school_id: Optional[int] = None,
    ):
        """
        Initialize Mashov client with credentials from parameters or environment.

        Args:
            username: Mashov user ID (default: from MASHOV_USER env var)
            password: Mashov password (default: from MASHOV_PASS env var)
            school_id: School symbol/ID (default: from MASHOV_SCHOOL env var)
        """
        self.username = username or os.getenv("MASHOV_USER")
        self.password = password or os.getenv("MASHOV_PASS")
        self.school_id = school_id or self._parse_school_id(os.getenv("MASHOV_SCHOOL"))
        self.session = None
        self.student_data = None
        self.authenticated = False

        logger.debug(
            f"MashovClient initialized: username={'***' if self.username else 'None'}, school_id={self.school_id}"
        )

    @staticmethod
    def _parse_school_id(school_id_str: Optional[str]) -> Optional[int]:
        """Parse school ID from string, return None if invalid."""
        if not school_id_str or school_id_str == "0":
            return None
        try:
            return int(school_id_str)
        except (ValueError, TypeError):
            return None

    def is_valid(self) -> bool:
        """Check if client has required credentials configured."""
        has_creds = bool(self.username and self.password and self.school_id)
        logger.debug(
            f"is_valid() → {has_creds} "
            f"(user={'✓' if self.username else '✗'}, "
            f"pass={'✓' if self.password else '✗'}, "
            f"school={'✓' if self.school_id else '✗'})"
        )
        return has_creds

    async def login(self) -> bool:
        """
        Authenticate with Mashov API.

        Returns:
            True if login successful, False otherwise
        """
        if not self.is_valid():
            logger.warning("Cannot login: missing credentials")
            return False

        # Check cache first
        cached_session = self._get_cached_session(self.username)
        if cached_session:
            self.session = cached_session
            self.authenticated = True
            logger.info(f"Using cached session for {self.username}")
            return True

        logger.info(f"[MASHOV] Login attempt: user={self.username}, school={self.school_id}")

        try:
            # Run login in executor to avoid blocking async loop
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(None, self._login_sync)

            if result:
                self.authenticated = True
                logger.info(f"[MASHOV] Login successful for {self.username}")
                # Cache the session
                self._cache_session(self.username, self.session)
                return True
            else:
                logger.warning(f"[MASHOV] Login failed for {self.username}")
                self.authenticated = False
                return False

        except Exception as e:
            logger.error(f"[MASHOV] Login error: {e}")
            self.authenticated = False
            return False

    def _login_sync(self) -> bool:
        """
        Synchronous login implementation.
        Called from async context via run_in_executor.
        """
        try:
            self.session = requests.Session()
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            }

            payload = {
                "username": self.username,
                "password": self.password,
                "semel": self.school_id,
                "year": YEAR,
            }

            response = self.session.post(
                f"{MASHOV_URL}/login",
                json=payload,
                headers=headers,
                timeout=10,
            )

            if response.status_code == 200:
                self.student_data = response.json()
                logger.debug(f"[MASHOV] Login response: {len(str(self.student_data))} bytes")
                return True
            else:
                logger.warning(f"[MASHOV] Login failed with status {response.status_code}")
                return False

        except Exception as e:
            logger.error(f"[MASHOV] Login sync error: {e}")
            return False

    async def fetch_homework(self, user_id: str) -> Optional[list[dict[str, Any]]]:
        """
        Fetch pending homework assignments.

        Args:
            user_id: Student user ID (from login response)

        Returns:
            List of homework items or None on failure
        """
        if not self.authenticated or not self.session:
            logger.warning("fetch_homework: not authenticated")
            return None

        try:
            loop = asyncio.get_event_loop()
            homework = await loop.run_in_executor(None, self._fetch_homework_sync, user_id)

            if homework:
                logger.info(f"[MASHOV] Fetched {len(homework)} homework items for {user_id}")
            else:
                logger.info(f"[MASHOV] No homework for {user_id}")

            return homework

        except Exception as e:
            logger.error(f"[MASHOV] Homework fetch error: {e}")
            return None

    def _fetch_homework_sync(self, user_id: str) -> Optional[list[dict]]:
        """Synchronous homework fetch."""
        try:
            if not self.session:
                return None

            response = self.session.get(
                f"{MASHOV_URL}/students/{user_id}/homework",
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                logger.warning("[MASHOV] Session expired (401)")
                self.authenticated = False
                return None
            else:
                logger.warning(f"[MASHOV] Homework fetch failed: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"[MASHOV] Homework sync error: {e}")
            return None

    async def fetch_grades(self, user_id: str) -> Optional[list[dict[str, Any]]]:
        """
        Fetch student grades.

        Args:
            user_id: Student user ID (from login response)

        Returns:
            List of grade items or None on failure
        """
        if not self.authenticated or not self.session:
            logger.warning("fetch_grades: not authenticated")
            return None

        try:
            loop = asyncio.get_event_loop()
            grades = await loop.run_in_executor(None, self._fetch_grades_sync, user_id)

            if grades:
                logger.info(f"[MASHOV] Fetched {len(grades)} grades for {user_id}")
            else:
                logger.info(f"[MASHOV] No grades for {user_id}")

            return grades

        except Exception as e:
            logger.error(f"[MASHOV] Grades fetch error: {e}")
            return None

    def _fetch_grades_sync(self, user_id: str) -> Optional[list[dict]]:
        """Synchronous grades fetch."""
        try:
            if not self.session:
                return None

            response = self.session.get(
                f"{MASHOV_URL}/students/{user_id}/grades",
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"[MASHOV] Grades fetch failed: {response.status_code}")
                return None

        except Exception as e:
            logger.error(f"[MASHOV] Grades sync error: {e}")
            return None

    def _get_cached_session(self, username: str) -> Optional[requests.Session]:
        """
        Retrieve cached session if still valid (TTL not expired).

        Args:
            username: Username to look up in cache

        Returns:
            Cached session or None if not found/expired
        """
        cache_key = f"mashov_{username}"
        if cache_key in self._session_cache:
            session, expires_at = self._session_cache[cache_key]
            if datetime.now() < expires_at:
                logger.debug(f"[MASHOV] Cache hit for {username}")
                return session
            else:
                logger.debug(f"[MASHOV] Cache expired for {username}")
                del self._session_cache[cache_key]

        return None

    def _cache_session(self, username: str, session: requests.Session, ttl: int = 3600) -> None:
        """
        Cache session with TTL (time-to-live).

        Args:
            username: Username for cache key
            session: Session object to cache
            ttl: Time-to-live in seconds (default: 1 hour)
        """
        cache_key = f"mashov_{username}"
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self._session_cache[cache_key] = (session, expires_at)
        logger.info(f"[MASHOV] Cached session for {username} (expires: {expires_at.strftime('%H:%M:%S')})")

    def _invalidate_cache(self, username: str) -> None:
        """Invalidate cached session (e.g., on 401 errors)."""
        cache_key = f"mashov_{username}"
        if cache_key in self._session_cache:
            del self._session_cache[cache_key]
            logger.info(f"[MASHOV] Invalidated cache for {username}")

    @staticmethod
    async def find_school(query: str) -> list[dict[str, Any]]:
        """
        Search for schools by name.

        Args:
            query: School name or partial name to search for

        Returns:
            List of matching schools
        """
        try:
            loop = asyncio.get_event_loop()
            schools = await loop.run_in_executor(None, MashovClient._find_school_sync, query)
            logger.info(f"[MASHOV] Found {len(schools)} schools matching '{query}'")
            return schools

        except Exception as e:
            logger.error(f"[MASHOV] School search error: {e}")
            return []

    @staticmethod
    def _find_school_sync(query: str) -> list[dict]:
        """Synchronous school search."""
        try:
            response = requests.get(
                f"{MASHOV_URL}/schools",
                timeout=10,
            )

            if response.status_code == 200:
                schools = response.json()
                # Filter by query (case-insensitive substring match)
                query_lower = query.lower()
                return [
                    s
                    for s in schools
                    if query_lower in s.get("name", "").lower() or query_lower in str(s.get("semel", "")).lower()
                ]
            else:
                logger.warning(f"[MASHOV] Schools fetch failed: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"[MASHOV] School search sync error: {e}")
            return []

    def get_student_id(self) -> Optional[str]:
        """
        Extract student ID from login response data.

        Returns:
            Student user ID or None
        """
        if not self.student_data:
            return None

        try:
            return self.student_data.get("credential", {}).get("userId")
        except (KeyError, TypeError):
            return None
