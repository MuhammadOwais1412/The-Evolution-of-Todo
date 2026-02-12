"""Message model for chat persistence."""
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, Dict, Any, TYPE_CHECKING
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Enum as SQLEnum, JSON

if TYPE_CHECKING:
    from src.models.conversation import Conversation


class MessageRole(str, Enum):
    """Role of the message sender."""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """Represents an individual message within a conversation."""

    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        index=True,
        nullable=False
    )
    role: MessageRole = Field(
        sa_column=Column(SQLEnum(MessageRole)),
        nullable=False
    )
    content: str = Field(nullable=False, max_length=10000)
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        sa_column=Column(JSON)
    )

    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
