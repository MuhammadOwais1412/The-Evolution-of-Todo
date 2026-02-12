"""Conversation service for managing chat conversations and messages."""
from datetime import datetime
from uuid import UUID
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from src.models.conversation import Conversation
from src.models.message import Message, MessageRole


class ConversationService:
    """Service for managing conversations and messages."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: str) -> Conversation:
        """Create a new conversation for a user.

        Args:
            user_id: The ID of the user creating the conversation

        Returns:
            The newly created Conversation object
        """
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def add_message(
        self,
        conversation_id: UUID,
        role: MessageRole,
        content: str,
        metadata: Optional[dict] = None
    ) -> Message:
        """Add a message to a conversation and update conversation timestamp.

        Args:
            conversation_id: The ID of the conversation
            role: The role of the message sender (user or assistant)
            content: The message content
            metadata: Optional metadata (e.g., tool calls, confirmation status)

        Returns:
            The newly created Message object
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata=metadata
        )
        self.session.add(message)

        # Update conversation's updated_at timestamp
        conversation = await self.session.get(Conversation, conversation_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()

        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_conversation_messages(
        self,
        conversation_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[Message], int]:
        """Retrieve messages for a conversation with pagination.

        Args:
            conversation_id: The ID of the conversation
            limit: Maximum number of messages to return (default 50, max 100)
            offset: Number of messages to skip (default 0)

        Returns:
            Tuple of (list of messages, total count)
        """
        # Enforce max limit
        limit = min(limit, 100)

        # Get messages
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.asc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        messages = result.scalars().all()

        # Get total count
        count_statement = (
            select(func.count(Message.id))
            .where(Message.conversation_id == conversation_id)
        )
        count_result = await self.session.execute(count_statement)
        total_count = count_result.scalar() or 0

        return list(messages), total_count

    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Conversation]:
        """Retrieve user's conversations ordered by most recent activity.

        Args:
            user_id: The ID of the user
            limit: Maximum number of conversations to return (default 20)
            offset: Number of conversations to skip (default 0)

        Returns:
            List of Conversation objects
        """
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(desc(Conversation.updated_at))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return list(result.scalars().all())

    async def get_conversation(self, conversation_id: UUID) -> Optional[Conversation]:
        """Get a conversation by ID.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            The Conversation object or None if not found
        """
        return await self.session.get(Conversation, conversation_id)

    async def verify_conversation_ownership(
        self,
        conversation_id: UUID,
        user_id: str
    ) -> bool:
        """Verify that a conversation belongs to a specific user.

        Args:
            conversation_id: The ID of the conversation
            user_id: The ID of the user

        Returns:
            True if the conversation belongs to the user, False otherwise
        """
        conversation = await self.get_conversation(conversation_id)
        return conversation is not None and conversation.user_id == user_id
