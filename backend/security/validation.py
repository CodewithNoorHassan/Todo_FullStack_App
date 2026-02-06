from app.models import ErrorResponse
from fastapi import HTTPException, status, Request
from typing import Dict, Any, Optional
import re
import html
import logging


logger = logging.getLogger(__name__)


def validate_input_safety(input_text: str) -> str:
    """
    Validate and sanitize input text to prevent injection attacks.

    Args:
        input_text: Input text to validate

    Returns:
        Sanitized input text
    """
    if input_text is None:
        return None

    # Remove potentially dangerous characters/sequences
    sanitized = input_text.strip()

    # Prevent common injection patterns
    dangerous_patterns = [
        r'<script.*?>.*?</script>',  # Script tags
        r'javascript:',              # JS protocol
        r'on\w+\s*=',               # Event handlers
        r'expression\s*\(',         # CSS expressions
    ]

    for pattern in dangerous_patterns:
        import re
        if re.search(pattern, sanitized, re.IGNORECASE):
            raise ValueError("Potentially dangerous input detected")

    # Escape HTML characters
    sanitized = html.escape(sanitized)

    return sanitized


def validate_task_title(title: str) -> bool:
    """
    Validate task title according to security requirements.

    Args:
        title: Task title to validate

    Returns:
        True if valid, raises exception if invalid
    """
    if not title or len(title.strip()) == 0:
        raise ValueError("Task title cannot be empty")

    if len(title) > 255:
        raise ValueError("Task title exceeds maximum length of 255 characters")

    # Check for potentially dangerous content
    try:
        validate_input_safety(title)
    except ValueError as e:
        raise ValueError(f"Invalid task title: {str(e)}")

    return True


def validate_task_description(description: Optional[str]) -> bool:
    """
    Validate task description according to security requirements.

    Args:
        description: Task description to validate (can be None)

    Returns:
        True if valid, raises exception if invalid
    """
    if description is None:
        return True

    if len(description) > 10000:
        raise ValueError("Task description exceeds maximum length of 10000 characters")

    # Check for potentially dangerous content
    try:
        validate_input_safety(description)
    except ValueError as e:
        raise ValueError(f"Invalid task description: {str(e)}")

    return True


def log_security_event(event_type: str, details: Dict[str, Any], request: Optional[Request] = None):
    """
    Log security-related events for monitoring.

    Args:
        event_type: Type of security event
        details: Details about the event
        request: Optional request object for context
    """
    ip_address = None
    user_agent = None

    if request:
        ip_address = request.headers.get("x-forwarded-for", request.client.host)
        user_agent = request.headers.get("user-agent")

    log_data = {
        "event_type": event_type,
        "details": details,
        "ip_address": ip_address,
        "user_agent": user_agent,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }

    logger.warning(f"SECURITY EVENT: {event_type} - {log_data}")


def mask_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Mask sensitive information in data for logging.

    Args:
        data: Data dictionary to mask

    Returns:
        Data dictionary with sensitive fields masked
    """
    masked_data = data.copy()

    sensitive_fields = ['token', 'password', 'secret', 'key', 'authorization', 'auth']

    for key, value in masked_data.items():
        if isinstance(key, str) and any(field in key.lower() for field in sensitive_fields):
            if isinstance(value, str):
                masked_data[key] = f"{value[:4]}..." if len(value) > 4 else "***"
            else:
                masked_data[key] = "***"

    return masked_data


def validate_rate_limit(bucket_name: str, max_requests: int = 100, window_seconds: int = 3600) -> bool:
    """
    Validate rate limits to prevent abuse.

    Args:
        bucket_name: Identifier for the rate limit bucket
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds

    Returns:
        True if within limits, False if exceeded
    """
    # This would be implemented with a proper rate limiting system (Redis, etc.)
    # For now, we'll return True as a placeholder
    return True


def validate_request_integrity(request: Request) -> bool:
    """
    Validate request integrity for common attack vectors.

    Args:
        request: Request object to validate

    Returns:
        True if request appears legitimate
    """
    # Check for suspicious headers
    suspicious_headers = [
        'x-forwarded-for',
        'x-real-ip',
        'x-client-ip',
        'x-originating-ip'
    ]

    for header in suspicious_headers:
        if header in request.headers:
            value = request.headers[header]
            # Log potential proxy abuse
            if value and len(value.split(',')) > 3:  # More than 3 proxies
                log_security_event(
                    "PROXY_CHAIN_DETECTED",
                    {"header": header, "value": value},
                    request
                )

    return True