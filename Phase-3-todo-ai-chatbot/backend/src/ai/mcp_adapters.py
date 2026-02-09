"""MCP tool adapter functions that connect OpenAI Assistant tools to MCP tools."""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from ..mcp.tools.task_operations import (
    add_task as mcp_add_task,
    list_tasks as mcp_list_tasks,
    update_task as mcp_update_task,
    complete_task as mcp_complete_task,
    delete_task as mcp_delete_task
)
from ..mcp.tools.auth_validation import verify_user_owns_task, validate_user_id
from ..exceptions.ai_exceptions import (
    ToolExecutionError,
    InvalidToolParametersError,
    UserPermissionError
)
from ..db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession


logger = logging.getLogger(__name__)


class MCPAdapters:
    """Adapter class to connect OpenAI Assistant tools to MCP tools."""

    def __init__(self):
        """Initialize the MCP adapters."""
        logger.info("MCP Adapters initialized")

    async def add_task(
        self,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium"
    ) -> Dict[str, Any]:
        """
        Adapter for the add_task MCP tool.

        Args:
            user_id: ID of the user requesting the task creation
            title: Title of the task
            description: Optional description of the task
            priority: Priority level ('low', 'medium', 'high'), defaults to 'medium'

        Returns:
            Dictionary containing the created task information
        """
        try:
            # Validate user ID format
            if not await validate_user_id(user_id):
                raise InvalidToolParametersError(f"Invalid user_id format: {user_id}")

            # Validate priority
            if priority not in ["low", "medium", "high"]:
                raise InvalidToolParametersError(f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'.")

            # Prepare parameters for MCP tool
            params = {
                "user_id": user_id,
                "title": title,
                "description": description or "",
                "priority": priority
            }

            # Call the MCP add_task function
            # Since MCP tools work with database sessions, we need to create one
            async with get_session() as session:
                result = await mcp_add_task(params, session)

                if result.get("success"):
                    task_data = result["task"]
                    return {
                        "id": task_data["id"],
                        "user_id": task_data["user_id"],
                        "title": task_data["title"],
                        "description": task_data["description"],
                        "completed": task_data["completed"],
                        "created_at": task_data["created_at"],
                        "updated_at": task_data["updated_at"],
                        "priority": task_data["priority"],
                        "message": "Task added successfully"
                    }
                else:
                    raise ToolExecutionError(result.get("message", "Failed to add task"))

        except InvalidToolParametersError:
            raise
        except UserPermissionError:
            raise
        except Exception as e:
            logger.error(f"Error in add_task adapter: {str(e)}")
            raise ToolExecutionError(f"Failed to add task: {str(e)}")

    async def list_tasks(
        self,
        user_id: str,
        status: str = "all"
    ) -> Dict[str, Any]:
        """
        Adapter for the list_tasks MCP tool.

        Args:
            user_id: ID of the user requesting the tasks
            status: Filter tasks by status ('all', 'pending', 'completed'), defaults to 'all'

        Returns:
            Dictionary containing the list of tasks
        """
        try:
            # Validate user ID format
            if not await validate_user_id(user_id):
                raise InvalidToolParametersError(f"Invalid user_id format: {user_id}")

            # Validate status
            if status not in ["all", "pending", "completed"]:
                raise InvalidToolParametersError(f"Invalid status: {status}. Must be 'all', 'pending', or 'completed'.")

            # Prepare parameters for MCP tool
            params = {
                "user_id": user_id,
                "status": status
            }

            # Call the MCP list_tasks function
            async with get_session() as session:
                result = await mcp_list_tasks(params, session)

                if result.get("success"):
                    return {
                        "tasks": result.get("tasks", []),
                        "count": len(result.get("tasks", [])),
                        "status_filter": status,
                        "message": "Tasks retrieved successfully"
                    }
                else:
                    raise ToolExecutionError(result.get("message", "Failed to list tasks"))

        except InvalidToolParametersError:
            raise
        except UserPermissionError:
            raise
        except Exception as e:
            logger.error(f"Error in list_tasks adapter: {str(e)}")
            raise ToolExecutionError(f"Failed to list tasks: {str(e)}")

    async def update_task(
        self,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Adapter for the update_task MCP tool.

        Args:
            user_id: ID of the user requesting the task update
            task_id: ID of the task to update
            title: New title for the task (optional)
            description: New description for the task (optional)
            priority: New priority for the task (optional)

        Returns:
            Dictionary containing the updated task information
        """
        try:
            # Validate user ID format
            if not await validate_user_id(user_id):
                raise InvalidToolParametersError(f"Invalid user_id format: {user_id}")

            # Validate task ID
            if not isinstance(task_id, int) or task_id <= 0:
                raise InvalidToolParametersError(f"Invalid task_id: {task_id}")

            # Validate priority if provided
            if priority and priority not in ["low", "medium", "high"]:
                raise InvalidToolParametersError(f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'.")

            # Prepare parameters for MCP tool
            params = {
                "user_id": user_id,
                "task_id": task_id
            }

            # Add optional parameters
            if title is not None:
                params["title"] = title
            if description is not None:
                params["description"] = description
            if priority is not None:
                params["priority"] = priority

            # Verify user owns the task before updating
            async with get_session() as session:
                if not await verify_user_owns_task(user_id, task_id, session):
                    raise UserPermissionError(f"User {user_id} does not own task {task_id}")

                # Call the MCP update_task function
                result = await mcp_update_task(params, session)

                if result.get("success"):
                    task_data = result["task"]
                    return {
                        "id": task_data["id"],
                        "user_id": task_data["user_id"],
                        "title": task_data["title"],
                        "description": task_data["description"],
                        "completed": task_data["completed"],
                        "created_at": task_data["created_at"],
                        "updated_at": task_data["updated_at"],
                        "priority": task_data["priority"],
                        "message": "Task updated successfully"
                    }
                else:
                    raise ToolExecutionError(result.get("message", "Failed to update task"))

        except InvalidToolParametersError:
            raise
        except UserPermissionError:
            raise
        except Exception as e:
            logger.error(f"Error in update_task adapter: {str(e)}")
            raise ToolExecutionError(f"Failed to update task: {str(e)}")

    async def complete_task(
        self,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Adapter for the complete_task MCP tool.

        Args:
            user_id: ID of the user requesting to complete the task
            task_id: ID of the task to complete

        Returns:
            Dictionary containing the completed task information
        """
        try:
            # Validate user ID format
            if not await validate_user_id(user_id):
                raise InvalidToolParametersError(f"Invalid user_id format: {user_id}")

            # Validate task ID
            if not isinstance(task_id, int) or task_id <= 0:
                raise InvalidToolParametersError(f"Invalid task_id: {task_id}")

            # Prepare parameters for MCP tool
            params = {
                "user_id": user_id,
                "task_id": task_id
            }

            # Verify user owns the task before completing
            async with get_session() as session:
                if not await verify_user_owns_task(user_id, task_id, session):
                    raise UserPermissionError(f"User {user_id} does not own task {task_id}")

                # Call the MCP complete_task function
                result = await mcp_complete_task(params, session)

                if result.get("success"):
                    task_data = result["task"]
                    return {
                        "id": task_data["id"],
                        "user_id": task_data["user_id"],
                        "title": task_data["title"],
                        "description": task_data["description"],
                        "completed": task_data["completed"],
                        "created_at": task_data["created_at"],
                        "updated_at": task_data["updated_at"],
                        "priority": task_data["priority"],
                        "message": "Task completed successfully"
                    }
                else:
                    raise ToolExecutionError(result.get("message", "Failed to complete task"))

        except InvalidToolParametersError:
            raise
        except UserPermissionError:
            raise
        except Exception as e:
            logger.error(f"Error in complete_task adapter: {str(e)}")
            raise ToolExecutionError(f"Failed to complete task: {str(e)}")

    async def delete_task(
        self,
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        Adapter for the delete_task MCP tool.

        Args:
            user_id: ID of the user requesting to delete the task
            task_id: ID of the task to delete

        Returns:
            Dictionary containing the deletion result
        """
        try:
            # Validate user ID format
            if not await validate_user_id(user_id):
                raise InvalidToolParametersError(f"Invalid user_id format: {user_id}")

            # Validate task ID
            if not isinstance(task_id, int) or task_id <= 0:
                raise InvalidToolParametersError(f"Invalid task_id: {task_id}")

            # Prepare parameters for MCP tool
            params = {
                "user_id": user_id,
                "task_id": task_id
            }

            # Verify user owns the task before deleting
            async with get_session() as session:
                if not await verify_user_owns_task(user_id, task_id, session):
                    raise UserPermissionError(f"User {user_id} does not own task {task_id}")

                # Call the MCP delete_task function
                result = await mcp_delete_task(params, session)

                if result.get("success"):
                    return {
                        "task_id": task_id,
                        "message": "Task deleted successfully"
                    }
                else:
                    raise ToolExecutionError(result.get("message", "Failed to delete task"))

        except InvalidToolParametersError:
            raise
        except UserPermissionError:
            raise
        except Exception as e:
            logger.error(f"Error in delete_task adapter: {str(e)}")
            raise ToolExecutionError(f"Failed to delete task: {str(e)}")

    async def validate_task_access(
        self,
        user_id: str,
        task_id: int
    ) -> bool:
        """
        Validate that a user has access to a specific task.

        Args:
            user_id: ID of the user
            task_id: ID of the task to check access for

        Returns:
            Boolean indicating if the user has access to the task
        """
        try:
            async with get_session() as session:
                return await verify_user_owns_task(user_id, task_id, session)
        except Exception as e:
            logger.error(f"Error validating task access: {str(e)}")
            return False