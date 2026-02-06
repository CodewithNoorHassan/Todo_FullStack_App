from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import BaseModel


class User(SQLModel, table=True):
    """
    User model representing users in the application.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    external_user_id: Optional[str] = Field(default=None, max_length=255, unique=True, nullable=True)  # ID from Better Auth (optional)
    email: str = Field(max_length=255, unique=True)
    name: Optional[str] = Field(default=None, max_length=255)
    hashed_password: Optional[str] = Field(default=None, max_length=500)  # Password hash


class TokenData(BaseModel):
    """
    Token data model for storing user information in JWT tokens.
    """
    email: Optional[str] = None