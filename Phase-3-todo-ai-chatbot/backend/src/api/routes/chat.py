"""Chat endpoints for conversation management."""
from datetime import datetime
from uuid import UUID
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.api.deps import get_current_user_id
from src.services.conversation_service import ConversationService
from src.schemas.chat_schemas import (
    ChatRequest,
    ChatResponse,
    ConversationHistoryResponse,
    MessageSchema,
    ErrorResponse
)
from src.models.message import MessageRole

# Import AI Agent service from existing Part B implementation
from src.api.routes.ai_chat import get_ai_agent_service

router = APIRouter(prefix="/api", tags=["chat"])


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication failed"},
        403: {"model": ErrorResponse, "description": "Unauthorized access"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def send_chat_message(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_session),
    authenticated_user_id: str = Depends(get_current_user_id)
):
    """Send a chat message and receive AI response.

    This endpoint:
    1. Validates user authentication and authorization
    2. Creates a new conversation or uses existing one
    3. Persists user message to database
    4. Calls AI Agent service for natural language processing
    5. Persists AI response to database
    6. Returns response with conversation context
    """
    # Authorization check: user_id in URL must match authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own conversations"
        )

    # Input validation
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    if len(request.message) > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message exceeds maximum length of 1000 characters"
        )

    try:
        conversation_service = ConversationService(session)

        # Get or create conversation
        if request.conversation_id:
            # Verify conversation ownership
            is_owner = await conversation_service.verify_conversation_ownership(
                request.conversation_id,
                user_id
            )
            if not is_owner:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have access to this conversation"
                )
            conversation_id = request.conversation_id
        else:
            # Create new conversation
            conversation = await conversation_service.create_conversation(user_id)
            conversation_id = conversation.id

        # Persist user message
        user_message = await conversation_service.add_message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=request.message,
            metadata={"requires_confirmation": request.requires_confirmation}
        )

        # Get conversation history for context reconstruction
        messages, _ = await conversation_service.get_conversation_messages(
            conversation_id=conversation_id,
            limit=50  # Last 50 messages for context
        )

        # Build context for AI Agent
        conversation_history = [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages[:-1]  # Exclude the just-added user message
        ]

        # Call AI Agent service (from Part B)
        ai_service = get_ai_agent_service()
        ai_response = await ai_service.process_message(
            user_id=user_id,
            message=request.message,
            conversation_history=conversation_history
        )

        # Persist AI response
        assistant_message = await conversation_service.add_message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response.get("response", "I encountered an error processing your request."),
            metadata={
                "tool_calls": ai_response.get("tool_calls", []),
                "requires_confirmation": ai_response.get("requires_confirmation", False)
            }
        )

        return ChatResponse(
            success=True,
            response=ai_response.get("response", ""),
            conversation_id=conversation_id,
            message_id=user_message.id,
            tool_calls=ai_response.get("tool_calls"),
            requires_confirmation=ai_response.get("requires_confirmation", False),
            timestamp=datetime.utcnow()
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat message: {str(e)}"
        )


@router.get(
    "/{user_id}/conversations/{conversation_id}/messages",
    response_model=ConversationHistoryResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication failed"},
        403: {"model": ErrorResponse, "description": "Unauthorized access"},
        404: {"model": ErrorResponse, "description": "Conversation not found"}
    }
)
async def get_conversation_history(
    user_id: str,
    conversation_id: UUID,
    limit: int = 50,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    authenticated_user_id: str = Depends(get_current_user_id)
):
    """Retrieve conversation history with pagination.

    This endpoint:
    1. Validates user authentication and authorization
    2. Verifies conversation ownership
    3. Retrieves messages in chronological order
    4. Returns paginated results with metadata
    """
    # Authorization check
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only access your own conversations"
        )

    # Validate pagination parameters
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )

    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset must be non-negative"
        )

    try:
        conversation_service = ConversationService(session)

        # Verify conversation exists and user owns it
        is_owner = await conversation_service.verify_conversation_ownership(
            conversation_id,
            user_id
        )
        if not is_owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Get messages with pagination
        messages, total_count = await conversation_service.get_conversation_messages(
            conversation_id=conversation_id,
            limit=limit,
            offset=offset
        )

        # Convert to response schema
        message_schemas = [
            MessageSchema(
                id=msg.id,
                role=msg.role.value,
                content=msg.content,
                timestamp=msg.timestamp,
                metadata=msg.metadata
            )
            for msg in messages
        ]

        has_more = (offset + len(messages)) < total_count

        return ConversationHistoryResponse(
            success=True,
            messages=message_schemas,
            total_count=total_count,
            has_more=has_more
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve conversation history: {str(e)}"
        )
