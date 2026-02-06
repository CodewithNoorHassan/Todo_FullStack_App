from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Optional
import threading
import time
import logging


logger = logging.getLogger(__name__)


class InMemoryRateLimiter:
    """
    Simple in-memory rate limiter for API endpoints.
    NOTE: This is for development purposes only. For production, use Redis-based rate limiting.
    """
    def __init__(self):
        self.requests = defaultdict(list)  # key: [timestamps]
        self.lock = threading.Lock()

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """
        Check if a request is allowed based on rate limits.

        Args:
            key: Unique identifier for the rate limit (e.g., IP address)
            max_requests: Maximum number of requests allowed
            window_seconds: Time window in seconds

        Returns:
            True if request is allowed, False otherwise
        """
        with self.lock:
            now = datetime.now()
            window_start = now - timedelta(seconds=window_seconds)

            # Remove old requests outside the window
            self.requests[key] = [
                timestamp for timestamp in self.requests[key]
                if timestamp > window_start
            ]

            # Check if we're under the limit
            current_count = len(self.requests[key])

            if current_count < max_requests:
                # Add current request
                self.requests[key].append(now)
                return True
            else:
                # Limit exceeded
                logger.warning(f"Rate limit exceeded for {key}: {current_count}/{max_requests} requests")
                return False


# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()


def check_rate_limit(identifier: str, max_requests: int = 100, window_seconds: int = 3600) -> bool:
    """
    Check if a request is within rate limits.

    Args:
        identifier: Unique identifier (e.g., IP address or user ID)
        max_requests: Maximum requests allowed in the window
        window_seconds: Time window in seconds

    Returns:
        True if within limits, False if exceeded
    """
    return rate_limiter.is_allowed(identifier, max_requests, window_seconds)


def get_requests_count(identifier: str, window_seconds: int = 3600) -> int:
    """
    Get the number of requests for an identifier within the time window.

    Args:
        identifier: Unique identifier
        window_seconds: Time window in seconds

    Returns:
        Number of requests in the current window
    """
    with rate_limiter.lock:
        now = datetime.now()
        window_start = now - timedelta(seconds=window_seconds)

        rate_limiter.requests[identifier] = [
            timestamp for timestamp in rate_limiter.requests[identifier]
            if timestamp > window_start
        ]

        return len(rate_limiter.requests[identifier])


# Predefined rate limits for different endpoints
RATE_LIMITS = {
    'auth': {'max_requests': 5, 'window_seconds': 300},  # 5 requests per 5 minutes
    'api': {'max_requests': 100, 'window_seconds': 3600},  # 100 requests per hour
    'task_crud': {'max_requests': 50, 'window_seconds': 600},  # 50 requests per 10 minutes
}


def check_endpoint_rate_limit(endpoint_type: str, identifier: str) -> bool:
    """
    Check rate limit for a specific endpoint type.

    Args:
        endpoint_type: Type of endpoint ('auth', 'api', 'task_crud', etc.)
        identifier: Unique identifier for the requester

    Returns:
        True if within limits, False if exceeded
    """
    if endpoint_type not in RATE_LIMITS:
        # Default to API limits if endpoint type not found
        endpoint_type = 'api'

    limits = RATE_LIMITS[endpoint_type]
    return check_rate_limit(identifier, limits['max_requests'], limits['window_seconds'])