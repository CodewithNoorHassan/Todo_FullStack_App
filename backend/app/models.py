from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """
    Base model for error responses.
    """
    detail: str


class HealthResponse(BaseModel):
    """
    Model for health check responses.
    """
    status: str
    environment: str
    version: Optional[str] = None


class TokenPayload(BaseModel):
    """
    Model for JWT token payload.
    """
    sub: str
    exp: int
    iat: Optional[int] = None
    email: Optional[str] = None
    name: Optional[str] = None