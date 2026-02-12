"""MCP tool orchestrator for validating user permissions and executing tools."""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession

from ..mcp.tools.auth_validation import verify_user_owns_task, validate_user_id
from ..mcp.tools.task_operations import (
    add_task as mcp_add_task,
    list_tasks as mcp_list_tasks,
    update_task as mcp_update_task,
    complete_task as mcp_complete_task,
    delete_task as mcp_delete_task
)
from ..db import get_session
from ..exceptions.ai_exceptions import (
    ToolExecutionError,
    UserPermissionError,
    InvalidToolParametersError
)


logger = logging.getLogger(__name__)


class ToolOrchestrator:
    """Orchestrator that validates user permissions and executes appropriate MCP tools."""

    def __init__(self):
        """Initialize the tool orchestrator."""
        logger.info("ToolOrchestrator initialized")

    async def execute_tool(
        self,
        tool_name: str,
        params: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Execute an MCP tool with proper user permission validation.

        Args:
            tool_name: Name of the tool to execute
            params: Parameters for the tool
            user_id: ID of the user requesting the tool execution

        Returns:
            Result of the tool execution
        """
        try:
            # Validate user ID format
            if not await validate_user_id(user_id):
                raise UserPermissionError(f"Invalid user ID format: {user_id}")

            # Validate parameters based on tool type
            validated_params = await self._validate_tool_parameters(tool_name, params, user_id)

            # Execute the appropriate tool
            async with get_session() as session:
                if tool_name == "add_task":
                    return await mcp_add_task(validated_params, session)
                elif tool_name == "list_tasks":
                    return await mcp_list_tasks(validated_params, session)
                elif tool_name == "update_task":
                    # Verify user owns the task before updating
                    task_id = validated_params.get("task_id")
                    if task_id and not await verify_user_owns_task(user_id, task_id, session):
                        raise UserPermissionError(f"User {user_id} does not own task {task_id}")

                    return await mcp_update_task(validated_params, session)
                elif tool_name == "complete_task":
                    # Verify user owns the task before completing
                    task_id = validated_params.get("task_id")
                    if task_id and not await verify_user_owns_task(user_id, task_id, session):
                        raise UserPermissionError(f"User {user_id} does not own task {task_id}")

                    return await mcp_complete_task(validated_params, session)
                elif tool_name == "delete_task":
                    # Verify user owns the task before deleting
                    task_id = validated_params.get("task_id")
                    if task_id and not await verify_user_owns_task(user_id, task_id, session):
                        raise UserPermissionError(f"User {user_id} does not own task {task_id}")

                    return await mcp_delete_task(validated_params, session)
                else:
                    raise InvalidToolParametersError(f"Unknown tool: {tool_name}")

        except UserPermissionError:
            raise
        except InvalidToolParametersError:
            raise
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            raise ToolExecutionError(f"Error executing tool {tool_name}: {str(e)}")

    async def validate_user_permission_for_task(
        self,
        user_id: str,
        task_id: int
    ) -> bool:
        """
        Validate that a user has permission to access a specific task.

        Args:
            user_id: ID of the user
            task_id: ID of the task to check permission for

        Returns:
            Boolean indicating if the user has permission
        """
        try:
            async with get_session() as session:
                return await verify_user_owns_task(user_id, task_id, session)
        except Exception as e:
            logger.error(f"Error validating user permission for task {task_id}: {str(e)}")
            return False

    async def _validate_tool_parameters(
        self,
        tool_name: str,
        params: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Validate tool parameters based on the tool type.

        Args:
            tool_name: Name of the tool
            params: Parameters to validate
            user_id: ID of the user (to ensure it matches if provided in params)

        Returns:
            Validated and cleaned parameters
        """
        validated_params = params.copy()

        # Ensure user_id consistency
        if "user_id" in validated_params and validated_params["user_id"] != user_id:
            raise UserPermissionError("User ID mismatch between request and parameters")

        # Add user_id to params if not present
        validated_params["user_id"] = user_id

        if tool_name == "add_task":
            return self._validate_add_task_params(validated_params)
        elif tool_name == "list_tasks":
            return self._validate_list_tasks_params(validated_params)
        elif tool_name == "update_task":
            return self._validate_update_task_params(validated_params)
        elif tool_name == "complete_task":
            return self._validate_complete_task_params(validated_params)
        elif tool_name == "delete_task":
            return self._validate_delete_task_params(validated_params)
        else:
            raise InvalidToolParametersError(f"Unknown tool: {tool_name}")

    def _validate_add_task_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for add_task tool."""
        validated = {}

        # Required fields
        if "title" not in params or not params["title"].strip():
            raise InvalidToolParametersError("Title is required for add_task")

        validated["title"] = params["title"].strip()

        # Optional fields
        validated["user_id"] = params["user_id"]

        if "description" in params:
            validated["description"] = params["description"] or ""
        else:
            validated["description"] = ""

        if "priority" in params:
            priority = params["priority"].lower()
            if priority not in ["low", "medium", "high"]:
                raise InvalidToolParametersError(
                    f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'."
                )
            validated["priority"] = priority
        else:
            validated["priority"] = "medium"

        return validated

    def _validate_list_tasks_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for list_tasks tool."""
        validated = {}

        validated["user_id"] = params["user_id"]

        if "status" in params:
            status = params["status"].lower()
            if status not in ["all", "pending", "completed"]:
                raise InvalidToolParametersError(
                    f"Invalid status: {status}. Must be 'all', 'pending', or 'completed'."
                )
            validated["status"] = status
        else:
            validated["status"] = "all"

        return validated

    def _validate_update_task_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for update_task tool."""
        validated = {}

        # Required fields
        if "task_id" not in params:
            raise InvalidToolParametersError("task_id is required for update_task")

        if not isinstance(params["task_id"], int) or params["task_id"] <= 0:
            raise InvalidToolParametersError("task_id must be a positive integer")

        validated["task_id"] = params["task_id"]
        validated["user_id"] = params["user_id"]

        # Optional fields
        if "title" in params and params["title"]:
            validated["title"] = params["title"].strip()

        if "description" in params:
            validated["description"] = params["description"] or ""

        if "priority" in params:
            priority = params["priority"].lower()
            if priority not in ["low", "medium", "high"]:
                raise InvalidToolParametersError(
                    f"Invalid priority: {priority}. Must be 'low', 'medium', or 'high'."
                )
            validated["priority"] = priority

        return validated

    def _validate_complete_task_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for complete_task tool."""
        validated = {}

        # Required fields
        if "task_id" not in params:
            raise InvalidToolParametersError("task_id is required for complete_task")

        if not isinstance(params["task_id"], int) or params["task_id"] <= 0:
            raise InvalidToolParametersError("task_id must be a positive integer")

        validated["task_id"] = params["task_id"]
        validated["user_id"] = params["user_id"]

        return validated

    def _validate_delete_task_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Validate parameters for delete_task tool."""
        validated = {}

        # Required fields
        if "task_id" not in params:
            raise InvalidToolParametersError("task_id is required for delete_task")

        if not isinstance(params["task_id"], int) or params["task_id"] <= 0:
            raise InvalidToolParametersError("task_id must be a positive integer")

        validated["task_id"] = params["task_id"]
        validated["user_id"] = params["user_id"]

        return validated

    async def batch_execute_tools(
        self,
        tools: list,
        user_id: str
    ) -> list:
        """
        Execute multiple tools in sequence for the same user.

        Args:
            tools: List of tuples (tool_name, params) to execute
            user_id: ID of the user requesting the tool executions

        Returns:
            List of results from each tool execution
        """
        results = []

        for tool_name, params in tools:
            try:
                result = await self.execute_tool(tool_name, params, user_id)
                results.append({
                    "tool_name": tool_name,
                    "success": True,
                    "result": result
                })
            except Exception as e:
                logger.error(f"Error executing tool {tool_name} in batch: {str(e)}")
                results.append({
                    "tool_name": tool_name,
                    "success": False,
                    "error": str(e)
                })

        return results