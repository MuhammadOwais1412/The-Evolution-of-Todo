"""
JWT validation utilities for MCP tools
"""
from typing import Optional
import jwt
from datetime import datetime
from ...config import get_settings
from sqlmodel import select
from ...models.task import Task
from ...db import async_session_factory
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

def validate_user_from_token(token: str) -> Optional[str]:
    """
    Validate JWT token and extract user_id

    Args:
        token: JWT token string

    Returns:
        user_id if valid, None otherwise
    """
    try:
        # Get the settings
        settings = get_settings()

        # Decode the JWT token using the secret
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )

        # Extract user_id from the payload
        user_id = payload.get("sub")  # Standard JWT field for subject/user

        if not user_id:
            logger.error("No user_id found in JWT token payload")
            return None

        return user_id

    except jwt.ExpiredSignatureError:
        logger.error("JWT token has expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid JWT token: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error decoding JWT token: {str(e)}")
        return None

async def verify_user_owns_task(user_id: str, task_id: int) -> bool:
    """
    Verify that a user owns a specific task

    Args:
        user_id: The ID of the user making the request
        task_id: The ID of the task to verify ownership for

    Returns:
        True if user owns the task, False otherwise
    """
    async with async_session_factory() as session:
        try:
            # Query for the task with matching user_id and task_id
            statement = select(Task).where(
                Task.id == task_id,
                Task.user_id == user_id
            )
            result = await session.execute(statement)
            task = result.scalar_one_or_none()

            return task is not None

        except SQLAlchemyError as e:
            logger.error(f"Database error verifying task ownership: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error verifying task ownership: {str(e)}")
            return False

def validate_user_id(user_id: str) -> bool:
    """
    Validate that a user_id is in the proper format

    Args:
        user_id: The ID of the user ID to validate

    Returns:
        True if valid format, False otherwise
    """
    # For now, we'll just check that user_id is not empty
    # In a real implementation, you might want to validate UUID format or other constraints
    return bool(user_id and isinstance(user_id, str) and len(user_id.strip()) > 0)