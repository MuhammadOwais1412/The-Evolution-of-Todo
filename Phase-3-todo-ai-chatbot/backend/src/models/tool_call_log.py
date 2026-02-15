"""SQLModel for logging AI agent tool calls."""
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from typing import Optional, Dict, Any, TYPE_CHECKING
from uuid import UUID, uuid4
import enum

if TYPE_CHECKING:
    from .user import User  # Assuming User model exists


class ToolCallStatus(str, enum.Enum):
    """Status of a tool call."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


class ToolCallLog(SQLModel, table=True):
    """Log entry for AI agent tool calls for audit and tracking purposes."""

    __tablename__ = "tool_call_logs"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True)
    session_id: UUID = Field(default_factory=uuid4)
    tool_name: str = Field()
    tool_params: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    result: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    status: ToolCallStatus = Field(default=ToolCallStatus.PENDING)
    error_details: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    ai_confidence: Optional[float] = Field(default=None)

    # Relationship to user (if needed)
    # user: User = Relationship(back_populates="tool_call_logs")