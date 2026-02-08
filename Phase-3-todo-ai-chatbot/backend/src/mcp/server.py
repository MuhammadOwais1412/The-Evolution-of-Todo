"""
MCP (Model Context Protocol) Server for Todo Operations
"""
from mcp.server import Server
from mcp.types import ClientCapabilities, EndUserId
import asyncio
import logging
from typing import Dict, Any, List
from ..models.task import Task
from ..db import get_session
from .tools.task_operations import add_task, list_tasks, update_task, complete_task, delete_task
from .schemas.task_schemas import AddTaskRequest, AddTaskResponse, ListTasksRequest, ListTasksResponse, UpdateTaskRequest, UpdateTaskResponse, CompleteTaskRequest, CompleteTaskResponse, DeleteTaskRequest, DeleteTaskResponse, ErrorResponse

# Initialize the MCP server
server = Server(
    name="todo-mcp-server",
    version="1.0.0",
    description="Todo operations server using Model Context Protocol"
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Register the add_task function as an MCP tool
@server.register_tool(
    name="add_task",
    description="Create a new task for the authenticated user",
    parameters=AddTaskRequest.model_json_schema()
)
async def handle_add_task(request: AddTaskRequest) -> Any:
    """
    Handler for the add_task MCP tool
    """
    try:
        result = await add_task(request)
        return result.dict() if hasattr(result, 'dict') else result
    except Exception as e:
        logger.error(f"Error in add_task handler: {str(e)}")
        error_response = ErrorResponse(
            error_code="HANDLER_ERROR",
            message=f"Error processing add_task: {str(e)}"
        )
        return error_response.dict()

# Register the list_tasks function as an MCP tool
@server.register_tool(
    name="list_tasks",
    description="Retrieve all tasks for the authenticated user",
    parameters=ListTasksRequest.model_json_schema()
)
async def handle_list_tasks(user_id: str, status: str = None) -> Any:
    """
    Handler for the list_tasks MCP tool
    """
    try:
        result = await list_tasks(user_id, status)
        return result
    except Exception as e:
        logger.error(f"Error in list_tasks handler: {str(e)}")
        error_response = ErrorResponse(
            error_code="HANDLER_ERROR",
            message=f"Error processing list_tasks: {str(e)}"
        )
        return error_response.dict()

# Register the update_task function as an MCP tool
@server.register_tool(
    name="update_task",
    description="Update properties of an existing task for the authenticated user",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "task_id": {"type": "integer"},
            "title": {"type": "string"},
            "description": {"type": "string"},
            "priority": {"type": "string", "enum": ["low", "medium", "high"]},
            "completed": {"type": "boolean"}
        },
        "required": ["user_id", "task_id"]
    }
)
async def handle_update_task(user_id: str, task_id: int, title: str = None, description: str = None, priority: str = None, completed: bool = None) -> Any:
    """
    Handler for the update_task MCP tool
    """
    try:
        result = await update_task(user_id, task_id, title, description, priority, completed)
        return result
    except Exception as e:
        logger.error(f"Error in update_task handler: {str(e)}")
        error_response = ErrorResponse(
            error_code="HANDLER_ERROR",
            message=f"Error processing update_task: {str(e)}"
        )
        return error_response.dict()

# Register the complete_task function as an MCP tool
@server.register_tool(
    name="complete_task",
    description="Mark a task as complete or incomplete for the authenticated user",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "task_id": {"type": "integer"},
            "completed": {"type": "boolean"}
        },
        "required": ["user_id", "task_id", "completed"]
    }
)
async def handle_complete_task(user_id: str, task_id: int, completed: bool) -> Any:
    """
    Handler for the complete_task MCP tool
    """
    try:
        result = await complete_task(user_id, task_id, completed)
        return result
    except Exception as e:
        logger.error(f"Error in complete_task handler: {str(e)}")
        error_response = ErrorResponse(
            error_code="HANDLER_ERROR",
            message=f"Error processing complete_task: {str(e)}"
        )
        return error_response.dict()

# Register the delete_task function as an MCP tool
@server.register_tool(
    name="delete_task",
    description="Remove a task for the authenticated user",
    parameters={
        "type": "object",
        "properties": {
            "user_id": {"type": "string"},
            "task_id": {"type": "integer"}
        },
        "required": ["user_id", "task_id"]
    }
)
async def handle_delete_task(user_id: str, task_id: int) -> Any:
    """
    Handler for the delete_task MCP tool
    """
    try:
        result = await delete_task(user_id, task_id)
        return result
    except Exception as e:
        logger.error(f"Error in delete_task handler: {str(e)}")
        error_response = ErrorResponse(
            error_code="HANDLER_ERROR",
            message=f"Error processing delete_task: {str(e)}"
        )
        return error_response.dict()