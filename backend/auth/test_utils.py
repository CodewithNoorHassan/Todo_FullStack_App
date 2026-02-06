from datetime import datetime, timedelta
from jose import jwt
from ..auth.config import auth_settings
from typing import Dict, Optional


def create_test_token(
    user_external_id: str,
    email: str = "test@example.com",
    name: str = "Test User",
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a test JWT token for development and testing purposes.

    Args:
        user_external_id: External user ID (as would come from Better Auth)
        email: User's email address
        name: User's name
        expires_delta: Optional timedelta for token expiration

    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=auth_settings.access_token_expire_minutes)

    to_encode = {
        "sub": user_external_id,
        "email": email,
        "name": name,
        "exp": expire.timestamp(),
        "iat": datetime.utcnow().timestamp()
    }

    encoded_jwt = jwt.encode(
        to_encode,
        auth_settings.secret_key,
        algorithm=auth_settings.algorithm
    )
    return encoded_jwt


def create_expired_token(user_external_id: str = "test_user_123") -> str:
    """
    Create an expired JWT token for testing purposes.

    Args:
        user_external_id: External user ID for the expired token

    Returns:
        Expired JWT token string
    """
    expire = datetime.utcnow() - timedelta(hours=1)  # Expired 1 hour ago

    to_encode = {
        "sub": user_external_id,
        "email": "expired@example.com",
        "name": "Expired User",
        "exp": expire.timestamp(),
        "iat": (datetime.utcnow() - timedelta(hours=2)).timestamp()
    }

    encoded_jwt = jwt.encode(
        to_encode,
        auth_settings.secret_key,
        algorithm=auth_settings.algorithm
    )
    return encoded_jwt


def create_invalid_signature_token(user_external_id: str = "test_user_123") -> str:
    """
    Create a token with an invalid signature for testing purposes.
    This simulates a tampered token.

    Args:
        user_external_id: External user ID for the invalid token

    Returns:
        Invalid signature JWT token string
    """
    # Create a valid token
    valid_token = create_test_token(user_external_id)

    # Modify it slightly to invalidate the signature
    # (This is a simplified approach - real tampering would be different)
    parts = valid_token.split('.')
    if len(parts) >= 2:
        # Modify the payload part to invalidate signature
        modified_payload = parts[1][:-1] + ('a' if parts[1][-1] != 'a' else 'b')
        return f"{parts[0]}.{modified_payload}.{parts[2]}"

    # If we can't modify properly, return a completely fake token
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIxMjMiLCJleHAiOjE1MTYyMzkwMjJ9.invalid.signature"


def decode_token_without_verification(token: str) -> Dict:
    """
    Decode a JWT token without verifying the signature (for testing purposes only).

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload as dictionary
    """
    from jose import jwt
    # Decode without verification - ONLY for testing purposes
    return jwt.get_unverified_claims(token)


def create_test_user_data(user_id: int = 1) -> Dict:
    """
    Create test user data for development.

    Args:
        user_id: User ID for the test user

    Returns:
        Dictionary containing test user data
    """
    return {
        "id": user_id,
        "external_user_id": f"test_user_{user_id}",
        "email": f"test{user_id}@example.com",
        "name": f"Test User {user_id}"
    }


def simulate_better_auth_response(user_external_id: str) -> Dict:
    """
    Simulate a response from Better Auth for testing purposes.

    Args:
        user_external_id: External user ID

    Returns:
        Simulated Better Auth response
    """
    return {
        "user": {
            "id": user_external_id,
            "email": f"{user_external_id.replace(' ', '_')}@example.com",
            "name": f"Test {user_external_id.replace('_', ' ').title()}",
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        },
        "accessToken": create_test_token(user_external_id),
        "refreshToken": "mock_refresh_token"
    }