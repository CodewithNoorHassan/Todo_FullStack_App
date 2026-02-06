from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from datetime import timedelta
from pydantic import BaseModel
from database.session import get_session
from models.user import User
from auth.auth_handler import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    get_current_user
)
from app.config import settings


router = APIRouter(prefix="/api/auth", tags=["authentication"])


class RegisterRequest(BaseModel):
    """User registration request model"""
    email: str
    password: str
    name: str = ""  # Optional with default empty string


class LoginRequest(BaseModel):
    """User login request model"""
    email: str
    password: str


class AuthResponse(BaseModel):
    """Authentication response model"""
    user: dict
    token: str


@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest, session: Session = Depends(get_session)):
    """
    Register a new user account.
    
    Args:
        request: User registration data (email, password, name)
        session: Database session
        
    Returns:
        AuthResponse with user data and JWT token
    """
    # Check if user already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user with hashed password
    hashed_password = get_password_hash(request.password)
    new_user = User(
        email=request.email,
        name=request.name,
        hashed_password=hashed_password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": new_user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    return AuthResponse(
        user={
            "id": str(new_user.id),
            "email": new_user.email,
            "name": new_user.name or "",
            "createdAt": new_user.id
        },
        token=access_token
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, session: Session = Depends(get_session)):
    """
    Login with email and password.
    
    Args:
        request: User login credentials (email, password)
        session: Database session
        
    Returns:
        AuthResponse with user data and JWT token
    """
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()
    
    if not user or not verify_password(request.password, user.hashed_password or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=settings.access_token_expire_minutes)
    )
    
    return AuthResponse(
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name or "",
            "createdAt": user.id
        },
        token=access_token
    )


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.

    Args:
        current_user: Current authenticated user

    Returns:
        User information
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "name": current_user.name or "",
        "createdAt": current_user.id
    }


@router.post("/logout")
async def logout():
    """
    Logout the current user (token invalidation handled on client).

    Returns:
        Success message
    """
    return {"message": "Logged out successfully"}


@router.get("/status")
async def get_auth_status():
    """
    Get authentication status of the current session.

    Returns:
        dict: Authentication status information
    """
    return {"authenticated": True, "provider": "Local JWT"}