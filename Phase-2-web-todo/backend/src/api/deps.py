"""API dependencies for JWT authentication and database sessions."""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.config import get_settings

settings = get_settings()

# HTTP Bearer token security scheme
security = HTTPBearer(auto_error=False)


async def verify_jwt(token: str) -> dict:
    """
    Verify and decode a JWT token from Better Auth.

    Args:
        token: The JWT token string

    Returns:
        Decoded token payload with 'sub' claim containing user_id

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"],
            options={"verify_exp": True}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """
    Dependency to extract and verify user identity from JWT.

    Args:
        credentials: HTTP Bearer credentials from Authorization header

    Returns:
        The user_id from the JWT 'sub' claim

    Raises:
        HTTPException: If no token provided or token is invalid
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = await verify_jwt(credentials.credentials)

    # Extract user_id from 'sub' claim
    user_id: Optional[str] = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing 'sub' claim",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id


async def get_session_dependency() -> AsyncSession:
    """
    Dependency for getting async database session.

    Yields:
        AsyncSession: Database session for the request
    """
    async for session in get_session():
        yield session


async def get_current_user_id(
    user_id: str = Depends(get_current_user)
) -> str:
    """
    Dependency that returns the authenticated user's ID.

    This is a convenience wrapper around get_current_user
    for cases where we need explicit typing.
    """
    return user_id
