from typing import Dict, Optional
from ..models.user import User
from sqlmodel import Session, select


def get_user_by_external_id(session: Session, external_user_id: str) -> Optional[User]:
    """
    Retrieve a user by their external user ID from Better Auth.

    Args:
        session: Database session
        external_user_id: The external user ID from Better Auth

    Returns:
        User object if found, None otherwise
    """
    statement = select(User).where(User.external_user_id == external_user_id)
    return session.exec(statement).first()


def create_or_get_user(session: Session, external_user_id: str, email: str, name: Optional[str] = None) -> User:
    """
    Create a new user if they don't exist, or return existing user.

    Args:
        session: Database session
        external_user_id: The external user ID from Better Auth
        email: User's email address
        name: User's name (optional)

    Returns:
        User object
    """
    # Try to find existing user
    user = get_user_by_external_id(session, external_user_id)

    if user:
        return user

    # Create new user if not found
    user = User(
        external_user_id=external_user_id,
        email=email,
        name=name
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def extract_user_info_from_token_payload(payload: Dict) -> Dict[str, str]:
    """
    Extract user information from JWT payload.

    Args:
        payload: Decoded JWT payload

    Returns:
        Dictionary containing user information
    """
    user_info = {
        "external_user_id": payload.get("sub"),
        "email": payload.get("email"),
        "name": payload.get("name", payload.get("given_name", ""))
    }

    return user_info