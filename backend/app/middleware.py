from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import logging


logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle errors and ensure consistent error responses.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        try:
            response = await call_next(request)
            return response
        except HTTPException as exc:
            # Log the error
            logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")

            # Return consistent error response with full detail
            return JSONResponse(
                status_code=exc.status_code,
                content={"detail": str(exc.detail), "status": exc.status_code}
            )
        except Exception as exc:
            # Log unexpected errors with full traceback
            logger.error(f"Unexpected error: {str(exc)}", exc_info=True)

            # Return consistent server error response with more detail in development
            import os
            is_dev = os.getenv('APP_ENV') == 'development'
            
            return JSONResponse(
                status_code=500,
                content={
                    "detail": str(exc) if is_dev else "Internal server error",
                    "status": 500,
                    "error_type": type(exc).__name__ if is_dev else None
                }
            )


def add_error_handling_middleware(app):
    """
    Add error handling middleware to the FastAPI app.
    """
    app.add_middleware(ErrorHandlingMiddleware)