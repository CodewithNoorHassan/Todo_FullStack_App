# Authentication Module Documentation

## Overview

The authentication module provides JWT-based authentication for the TaskMaster API, integrating with Better Auth for user management while maintaining local user references for data association.

## Components

### 1. JWT Handler (`jwt_handler.py`)

Handles JWT token verification and user extraction from tokens.

#### Key Functions:
- `create_access_token(data, expires_delta)`: Creates new JWT tokens
- `verify_token(token)`: Verifies JWT tokens
- `get_current_user(credentials)`: Extracts authenticated user from JWT

#### Usage:
```python
from backend.auth.jwt_handler import get_current_user
from backend.models.user import User

async def protected_endpoint(current_user: User = Depends(get_current_user)):
    # This endpoint requires authentication
    return {"user_id": current_user.id, "message": "Access granted"}
```

### 2. Auth Configuration (`config.py`)

Manages authentication settings from environment variables.

#### Settings:
- `secret_key`: Secret key for JWT signing (from BETTER_AUTH_SECRET)
- `algorithm`: JWT algorithm (default: HS256)
- `access_token_expire_minutes`: Token expiration time

### 3. User Utilities (`user_utils.py`)

Provides helper functions for user management.

#### Key Functions:
- `get_user_by_external_id(session, external_user_id)`: Find user by external ID
- `create_or_get_user(session, external_user_id, email, name)`: Sync user from Better Auth
- `extract_user_info_from_token_payload(payload)`: Extract user info from JWT

## Integration with Better Auth

The system is designed to work with Better Auth for user management:
1. Better Auth handles user registration/login
2. JWT tokens contain user information (particularly the `sub` claim with external user ID)
3. Our system maps external user IDs to local user records for data association
4. User data is synchronized between Better Auth and our local database

## Security Features

1. **JWT Verification**: All requests to protected endpoints require valid JWT tokens
2. **User Isolation**: Users can only access their own data
3. **Token Expiration**: Tokens expire after configured time
4. **Error Handling**: Clear error responses for authentication failures

## Protected Endpoints

To protect an endpoint, use the `get_current_user` dependency:

```python
from fastapi import Depends
from backend.auth.jwt_handler import get_current_user
from backend.models.user import User

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user_id": current_user.id, "message": "This is a protected route"}
```

## Testing

Use the test utilities for development:

```python
from backend.auth.test_utils import create_test_token

# Create a test token
token = create_test_token("test_user_123", "test@example.com", "Test User")

# Use in API requests as Authorization: Bearer <token>
```

## Error Responses

- `401 Unauthorized`: Invalid, expired, or missing JWT token
- `403 Forbidden`: User attempting to access resources they don't own