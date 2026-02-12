"""Chat request and response schemas."""
from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """Request schema for sending a chat message."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message content")
    conversation_id: Optional[UUID] = Field(None, description="Existing conversation ID (optional for new conversations)")
    requires_confirmation: Optional[bool] = Field(False, description="Whether this action requires user confirmation")


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""
    success: bool = Field(..., description="Whether the request was successful")
    response: str = Field(..., description="AI assistant response")
    conversation_id: UUID = Field(..., description="Conversation ID (new or existing)")
    message_id: UUID = Field(..., description="ID of the user's message")
    tool_calls: Optional[List[Dict[str, Any]]] = Field(None, description="Tool calls made by the AI agent")
    requires_confirmation: Optional[bool] = Field(False, description="Whether the action requires user confirmation")
    timestamp: datetime = Field(..., description="Timestamp of the response")


class MessageSchema(BaseModel):
    """Schema for a single message."""
    id: UUID
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    metadata: Optional[Dict[str, Any]] = None


class ConversationHistoryResponse(BaseModel):
    """Response schema for conversation history endpoint."""
    success: bool = Field(..., description="Whether the request was successful")
    messages: List[MessageSchema] = Field(..., description="List of messages in chronological order")
    total_count: int = Field(..., description="Total number of messages in the conversation")
    has_more: bool = Field(..., description="Whether there are more messages to load")


class ErrorResponse(BaseModel):
    """Error response schema."""
    success: bool = Field(False, description="Always false for errors")
    error_code: str = Field(..., description="Error code (e.g., AUTH_FAILED, RATE_LIMIT)")
    error_message: str = Field(..., description="User-friendly error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
