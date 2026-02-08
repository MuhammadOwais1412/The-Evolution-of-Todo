"""
MCP-specific task schemas for todo operations
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskSchema(BaseModel):
    """
    Schema representing a task in the system
    """
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime
    priority: Optional[PriorityEnum] = None


class AddTaskRequest(BaseModel):
    """
    Request schema for add_task operation
    """
    user_id: str
    title: str
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None


class AddTaskResponse(BaseModel):
    """
    Response schema for add_task operation
    """
    status: str = "success"
    task: TaskSchema
    message: str = "Task created successfully"


class ListTasksRequest(BaseModel):
    """
    Request schema for list_tasks operation
    """
    user_id: str
    status: Optional[str] = None  # "all", "pending", "completed"


class ListTasksResponse(BaseModel):
    """
    Response schema for list_tasks operation
    """
    status: str = "success"
    tasks: List[TaskSchema]
    message: str = "Tasks retrieved successfully"


class UpdateTaskRequest(BaseModel):
    """
    Request schema for update_task operation
    """
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    completed: Optional[bool] = None


class UpdateTaskResponse(BaseModel):
    """
    Response schema for update_task operation
    """
    status: str = "success"
    task: TaskSchema
    message: str = "Task updated successfully"


class CompleteTaskRequest(BaseModel):
    """
    Request schema for complete_task operation
    """
    user_id: str
    task_id: int
    completed: bool


class CompleteTaskResponse(BaseModel):
    """
    Response schema for complete_task operation
    """
    status: str = "success"
    task: TaskSchema
    message: str = "Task completion status updated successfully"


class DeleteTaskRequest(BaseModel):
    """
    Request schema for delete_task operation
    """
    user_id: str
    task_id: int


class DeleteTaskResponse(BaseModel):
    """
    Response schema for delete_task operation
    """
    status: str = "success"
    task_id: int
    message: str = "Task deleted successfully"


class ErrorResponse(BaseModel):
    """
    Schema for error responses across all MCP tools
    """
    status: str = "error"
    error_code: str
    message: str
    details: Optional[dict] = None