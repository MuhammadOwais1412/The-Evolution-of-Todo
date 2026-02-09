"""Utility functions for JWT validation from Better Auth."""
from typing import Optional
from datetime import datetime
import jwt
from fastapi import HTTPException, status, Request
from ..config import get_settings
from sqlmodel import Session
from ..models.user import User
from ..services.auth import verify_token  # Assuming this exists from the existing auth system


async def validate_user_from_token(token: str) -> Optional[dict]:
    """
    Validate a JWT token from Better Auth and return user information.

    Args:
        token: JWT token to validate

    Returns:
        Dictionary containing user information if valid, None otherwise
    """
    try:
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token[7:]

        # Use the existing Better Auth verification system
        user_info = await verify_token(token)

        if user_info:
            return user_info
        else:
            return None

    except Exception as e:
        print(f"Error validating token: {str(e)}")
        return None


async def get_current_user_id(request: Request) -> Optional[str]:
    """
    Extract and validate user ID from the Authorization header.

    Args:
        request: FastAPI request object containing the authorization header

    Returns:
        User ID if valid, raises HTTPException otherwise
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid format"
        )

    token = auth_header[7:]  # Remove "Bearer " prefix

    user_info = await validate_user_from_token(token)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    # Assuming user_info contains 'userId' field from Better Auth
    user_id = user_info.get('userId') or user_info.get('id')

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: no user ID found"
        )

    return user_id


async def verify_user_owns_resource(user_id: str, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the resource they're trying to access.

    Args:
        user_id: ID of the authenticated user
        resource_user_id: ID of the user who owns the resource

    Returns:
        True if user owns the resource, False otherwise
    """
    return str(user_id) == str(resource_user_id)


def create_jwt_payload(user_id: str, additional_claims: Optional[dict] = None) -> dict:
    """
    Create a JWT payload for a user.

    Args:
        user_id: User ID to include in the token
        additional_claims: Additional claims to include in the token

    Returns:
        Dictionary representing the JWT payload
    """
    payload = {
        "sub": user_id,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow().timestamp() + 3600 * 24 * 7  # 1 week expiry
    }

    if additional_claims:
        payload.update(additional_claims)

    return payload


async def validate_and_get_user_scoped_resource(session: Session, model_class, resource_id: str, user_id: str):
    """
    Helper function to validate that a user can access a specific resource.

    Args:
        session: Database session
        model_class: The SQLModel class for the resource
        resource_id: ID of the resource to retrieve
        user_id: ID of the authenticated user

    Returns:
        The resource if user has access, raises HTTPException otherwise
    """
    # Assuming the model has a user_id attribute
    resource = session.get(model_class, resource_id)

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_class.__name__} not found"
        )

    # Check if the resource belongs to the authenticated user
    if hasattr(resource, 'user_id'):
        if not await verify_user_owns_resource(user_id, resource.user_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You don't have permission to access this resource"
            )

    return resource