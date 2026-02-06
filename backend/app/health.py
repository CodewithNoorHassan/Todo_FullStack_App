from fastapi import APIRouter, Depends
from .models import HealthResponse
from .config import settings


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify the application status.

    Returns:
        HealthResponse: Status information about the application
    """
    # Use the configured APP_ENV from settings (uppercase key in Settings)
    env = getattr(settings, "APP_ENV", None) or getattr(settings, "APP_ENV", "development")
    return HealthResponse(
        status="healthy",
        environment=env,
        version="1.0.0"
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint to verify the application is ready to serve traffic.

    Returns:
        dict: Readiness status
    """
    # In a real implementation, this might check database connectivity, etc.
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """
    Liveness check endpoint to verify the application is alive.

    Returns:
        dict: Liveness status
    """
    # In a real implementation, this might check internal health indicators
    return {"status": "alive"}