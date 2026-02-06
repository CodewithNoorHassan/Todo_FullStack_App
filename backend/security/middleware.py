from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

# Import using relative path from same directory
from .validation import validate_request_integrity, log_security_event, mask_sensitive_data
import time
import logging


logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle security validations and protections.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        # Validate request integrity
        try:
            is_valid = validate_request_integrity(request)
            if not is_valid:
                log_security_event("INVALID_REQUEST", {"path": request.url.path, "method": request.method}, request)
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content={"detail": "Invalid request"}
                )
        except Exception as e:
            log_security_event("REQUEST_VALIDATION_ERROR", {"error": str(e)}, request)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"detail": "Request validation failed"}
            )

        # Add security headers to response
        response = await call_next(request)

        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

        return response


def add_security_middleware(app):
    """
    Add security middleware to the FastAPI app.
    """
    app.add_middleware(SecurityMiddleware)