"""SQLModel for logging AI agent tool calls."""
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
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
    user_id: UUID = Field(foreign_key="users.id", nullable=False)
    session_id: UUID = Field(default_factory=uuid4, nullable=False)  # Identifier for the conversation session
    tool_name: str = Field(nullable=False)  # Name of the MCP tool called
    tool_params: dict = Field(default={}, sa_column_kwargs={"server_default": "{}"})  # Parameters passed to the tool
    result: dict = Field(default={}, sa_column_kwargs={"server_default": "{}"})  # Result returned from the tool
    status: ToolCallStatus = Field(sa_column_kwargs={"server_default": "pending"})  # Status of the call
    error_details: Optional[dict] = Field(default=None)  # Error information if status is 'error'
    timestamp: datetime = Field(default_factory=datetime.utcnow, nullable=False)  # When the tool was called
    ai_confidence: Optional[float] = Field(default=None)  # Optional confidence score from AI agent

    # Relationship to user (if needed)
    # user: User = Relationship(back_populates="tool_call_logs")