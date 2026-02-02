#!/usr/bin/env python3
"""
Retry Utilities with Exponential Backoff

Provides decorators and utilities for robust API error handling with:
- Exponential backoff with jitter
- Configurable retry counts and delays
- HTTP status code filtering
- Sync and async support
"""

import asyncio
import functools
import logging
import random
import time
from collections.abc import Sequence
from typing import Callable, Optional

logger = logging.getLogger(__name__)

# Default retryable HTTP status codes
DEFAULT_RETRYABLE_CODES = (429, 500, 502, 503, 504)

# Default retryable exceptions
DEFAULT_RETRYABLE_EXCEPTIONS = (
    ConnectionError,
    TimeoutError,
)


class RetryExhausted(Exception):
    """Raised when all retry attempts have been exhausted."""

    pass


def calculate_backoff(
    attempt: int,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
) -> float:
    """
    Calculate delay with exponential backoff and optional jitter.

    Args:
        attempt: Current attempt number (0-indexed)
        base_delay: Base delay in seconds
        max_delay: Maximum delay cap in seconds
        jitter: Add random jitter to prevent thundering herd

    Returns:
        Delay in seconds
    """
    delay = min(base_delay * (2**attempt), max_delay)
    if jitter:
        delay = delay * (0.5 + random.random())
    return delay


def retry_with_backoff(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
    retryable_codes: Sequence[int] = DEFAULT_RETRYABLE_CODES,
    retryable_exceptions: Sequence[type[Exception]] = DEFAULT_RETRYABLE_EXCEPTIONS,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
):
    """
    Decorator for sync functions with retry and exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Base delay between retries in seconds
        max_delay: Maximum delay cap in seconds
        jitter: Add random jitter to delays
        retryable_codes: HTTP status codes that should trigger retry
        retryable_exceptions: Exception types that should trigger retry
        on_retry: Optional callback(attempt, exception, delay) called before each retry

    Example:
        @retry_with_backoff(max_retries=3, base_delay=1.0)
        def call_api():
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    # Check if this exception should trigger retry
                    should_retry = False

                    # Check for HTTP status code errors
                    status_code = _extract_status_code(e)
                    if status_code and status_code in retryable_codes:
                        should_retry = True

                    # Check for retryable exception types
                    if isinstance(e, tuple(retryable_exceptions)):
                        should_retry = True

                    if not should_retry or attempt >= max_retries:
                        logger.error(f"[Retry] {func.__name__} failed after {attempt + 1} attempts: {e}")
                        raise

                    delay = calculate_backoff(attempt, base_delay, max_delay, jitter)

                    logger.warning(
                        f"[Retry] {func.__name__} attempt {attempt + 1}/{max_retries + 1} failed "
                        f"(status={status_code}). Retrying in {delay:.2f}s..."
                    )

                    if on_retry:
                        on_retry(attempt, e, delay)

                    time.sleep(delay)

            raise RetryExhausted(f"All {max_retries + 1} attempts exhausted") from last_exception

        return wrapper

    return decorator


def async_retry_with_backoff(
    max_retries: int = 5,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    jitter: bool = True,
    retryable_codes: Sequence[int] = DEFAULT_RETRYABLE_CODES,
    retryable_exceptions: Sequence[type[Exception]] = DEFAULT_RETRYABLE_EXCEPTIONS,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
):
    """
    Decorator for async functions with retry and exponential backoff.
    Same parameters as retry_with_backoff but for async functions.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    should_retry = False
                    status_code = _extract_status_code(e)

                    if status_code and status_code in retryable_codes:
                        should_retry = True

                    if isinstance(e, tuple(retryable_exceptions)):
                        should_retry = True

                    if not should_retry or attempt >= max_retries:
                        logger.error(f"[Retry] {func.__name__} failed after {attempt + 1} attempts: {e}")
                        raise

                    delay = calculate_backoff(attempt, base_delay, max_delay, jitter)

                    logger.warning(
                        f"[Retry] {func.__name__} attempt {attempt + 1}/{max_retries + 1} failed "
                        f"(status={status_code}). Retrying in {delay:.2f}s..."
                    )

                    if on_retry:
                        on_retry(attempt, e, delay)

                    await asyncio.sleep(delay)

            raise RetryExhausted(f"All {max_retries + 1} attempts exhausted") from last_exception

        return wrapper

    return decorator


def _extract_status_code(exception: Exception) -> Optional[int]:
    """
    Extract HTTP status code from various exception types.
    Supports: requests, httpx, aiohttp, openai exceptions.
    """
    # requests.HTTPError
    if hasattr(exception, "response") and hasattr(exception.response, "status_code"):
        return exception.response.status_code

    # httpx.HTTPStatusError
    if hasattr(exception, "response") and hasattr(exception.response, "status_code"):
        return exception.response.status_code

    # aiohttp.ClientResponseError
    if hasattr(exception, "status"):
        return exception.status

    # OpenAI APIError
    if hasattr(exception, "status_code"):
        return exception.status_code

    # Check exception message for status code
    msg = str(exception)
    for code in [429, 400, 500, 502, 503, 504]:
        if str(code) in msg:
            return code

    return None


def sanitize_prompt(prompt: str, max_length: int = 4000) -> str:
    """
    Sanitize prompt for API calls to prevent 400 errors.

    - Removes control characters
    - Truncates to max length
    - Escapes problematic sequences
    """
    import re

    # Remove control characters except newlines and tabs
    prompt = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", "", prompt)

    # Truncate if too long
    if len(prompt) > max_length:
        prompt = prompt[:max_length] + "..."

    return prompt.strip()


def escape_telegram_markdown(text: str) -> str:
    """
    Escape special characters for Telegram MarkdownV2.
    Use this before sending messages with parse_mode='MarkdownV2'.
    """
    # Characters that need escaping in MarkdownV2
    special_chars = ["_", "*", "[", "]", "(", ")", "~", "`", ">", "#", "+", "-", "=", "|", "{", "}", ".", "!"]

    for char in special_chars:
        text = text.replace(char, f"\\{char}")

    return text


def escape_telegram_html(text: str) -> str:
    """
    Escape special characters for Telegram HTML mode.
    """
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# Convenience function for wrapping any callable with retry
def with_retry(func: Callable, max_retries: int = 3, base_delay: float = 1.0, **kwargs) -> Callable:
    """
    Wrap an existing function with retry logic without using decorator syntax.

    Example:
        safe_api_call = with_retry(risky_api_call, max_retries=5)
        result = safe_api_call(arg1, arg2)
    """
    return retry_with_backoff(max_retries=max_retries, base_delay=base_delay, **kwargs)(func)


if __name__ == "__main__":
    # Quick test
    logging.basicConfig(level=logging.DEBUG)

    @retry_with_backoff(max_retries=3, base_delay=0.5)
    def test_retry():
        import random

        if random.random() < 0.7:
            raise ConnectionError("Simulated failure")
        return "Success!"

    try:
        result = test_retry()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Final error: {e}")
