"""Pydantic schemas for AI request/response handling."""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID
import enum


class ToolCallStatus(str, enum.Enum):
    """Status of a tool call."""
    SUCCESS = "success"
    ERROR = "error"
    PENDING = "pending"


class MCPToolName(str, enum.Enum):
    """Valid MCP tool names."""
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"


class MCPToolCall(BaseModel):
    """Schema for an individual tool call made by the AI agent."""
    id: str = Field(..., description="Unique identifier for the tool call")
    tool_name: MCPToolName = Field(..., description="Name of the MCP tool called")
    tool_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters passed to the tool")
    result: Optional[Dict[str, Any]] = Field(default=None, description="Result from the tool execution")
    status: ToolCallStatus = Field(..., description="Status of the tool call")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="ISO 8601 datetime of execution")


class AIChatRequest(BaseModel):
    """Schema for AI chat request."""
    message: str = Field(..., min_length=1, max_length=1000, description="Natural language command from user")
    context: Optional[dict] = Field(default=None, description="Additional context for the request")
    requires_confirmation: bool = Field(default=True, description="Whether to require confirmation for destructive operations")


class AIChatResponse(BaseModel):
    """Schema for AI chat response."""
    response: str = Field(..., description="AI-generated response to user")
    tool_calls: List[MCPToolCall] = Field(default_factory=list, description="Tool calls made by the AI agent")
    requires_confirmation: bool = Field(default=False, description="Whether user confirmation is needed for any actions")
    success: bool = Field(..., description="Whether the request was successful")
    message: str = Field(..., description="Human-readable message about the result")


class AIChatResponseData(BaseModel):
    """Schema for the data portion of AI chat response."""
    response: str = Field(..., description="AI-generated response to user")
    tool_calls: List[MCPToolCall] = Field(default_factory=list, description="Tool calls made by the AI agent")
    requires_confirmation: bool = Field(default=False, description="Whether user confirmation is needed for any actions")
    next_prompt: Optional[str] = Field(default=None, description="Follow-up question or prompt from AI")


class ToolCallLogRequest(BaseModel):
    """Schema for tool call log request."""
    limit: int = Field(default=20, ge=1, le=100, description="Number of records to return")
    offset: int = Field(default=0, ge=0, description="Offset for pagination")
    start_date: Optional[str] = Field(default=None, description="ISO 8601 date to filter logs from")
    end_date: Optional[str] = Field(default=None, description="ISO 8601 date to filter logs until")
    tool_name: Optional[MCPToolName] = Field(default=None, description="Filter by specific tool name")
    status: Optional[ToolCallStatus] = Field(default=None, description="Filter by status")


class ToolCallLogResponseItem(BaseModel):
    """Schema for individual tool call log response item."""
    id: UUID = Field(..., description="Unique identifier for the log entry")
    tool_name: MCPToolName = Field(..., description="Name of the MCP tool called")
    tool_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters passed to the tool")
    result_summary: str = Field(..., description="Brief summary of the result")
    status: ToolCallStatus = Field(..., description="One of: success, error, pending")
    timestamp: datetime = Field(..., description="ISO 8601 datetime of execution")
    ai_confidence: Optional[float] = Field(default=None, description="Confidence score from AI agent")


class ToolCallLogResponse(BaseModel):
    """Schema for tool call log response."""
    status: str = Field(..., pattern=r"^(success|error)$", description="Response status")
    data: dict = Field(..., description="Response data")
    meta: dict = Field(default_factory=dict, description="Additional metadata")


class ToolCallLogData(BaseModel):
    """Schema for the data portion of tool call log response."""
    logs: List[ToolCallLogResponseItem] = Field(..., description="List of tool call log entries")
    pagination: dict = Field(..., description="Pagination information")


class AIHealthResponse(BaseModel):
    """Schema for AI agent health check response."""
    status: str = Field(..., pattern=r"^(success|error)$", description="Response status")
    data: dict = Field(..., description="Response data")
    meta: Optional[dict] = Field(default=None, description="Additional metadata")


class HealthCheckResponse(BaseModel):
    """Schema for health check response."""
    status: str = Field(..., description="Overall health status")
    service: str = Field(..., description="Service name")
    timestamp: str = Field(..., description="ISO 8601 timestamp of the check")
    checks: Dict[str, Any] = Field(..., description="Individual health checks")