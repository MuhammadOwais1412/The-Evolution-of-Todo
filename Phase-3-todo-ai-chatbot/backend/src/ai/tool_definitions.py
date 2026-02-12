"""Tool definitions for OpenAI Assistant API that map to MCP tools."""
from typing import List, Dict, Any


def get_mcp_tool_definitions() -> List[Dict[str, Any]]:
    """
    Get the complete set of tool definitions that map to MCP tools.

    These definitions follow the OpenAI/Gemini function calling format
    and map directly to the available MCP tools.

    Returns:
        List of tool definitions in OpenAI API format
    """
    return [
        {
            "type": "function",
            "function": {
                "name": "add_task",
                "description": "Add a new task to the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user creating the task"
                        },
                        "title": {
                            "type": "string",
                            "description": "The title of the task"
                        },
                        "description": {
                            "type": "string",
                            "description": "The description of the task (optional)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "Priority of the task (optional, defaults to 'medium')"
                        }
                    },
                    "required": ["user_id", "title"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "list_tasks",
                "description": "List tasks for the user, optionally filtered by status",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user whose tasks to list"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Status filter for tasks (optional, defaults to 'all')"
                        }
                    },
                    "required": ["user_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "update_task",
                "description": "Update an existing task for the user",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user who owns the task"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to update"
                        },
                        "title": {
                            "type": "string",
                            "description": "The new title of the task (optional)"
                        },
                        "description": {
                            "type": "string",
                            "description": "The new description of the task (optional)"
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high"],
                            "description": "New priority of the task (optional)"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user who owns the task"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to complete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "delete_task",
                "description": "Delete a task from the user's todo list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "The ID of the user who owns the task"
                        },
                        "task_id": {
                            "type": "integer",
                            "description": "The ID of the task to delete"
                        }
                    },
                    "required": ["user_id", "task_id"]
                }
            }
        }
    ]


def get_tool_definition_by_name(tool_name: str) -> Dict[str, Any]:
    """
    Get a specific tool definition by name.

    Args:
        tool_name: Name of the tool to retrieve

    Returns:
        Tool definition dictionary

    Raises:
        ValueError: If the tool name is not found
    """
    tools = get_mcp_tool_definitions()

    for tool in tools:
        if tool["function"]["name"] == tool_name:
            return tool

    raise ValueError(f"Tool '{tool_name}' not found in available tools")


def validate_tool_parameters(tool_name: str, params: Dict[str, Any]) -> bool:
    """
    Validate parameters for a specific tool.

    Args:
        tool_name: Name of the tool to validate
        params: Parameters to validate

    Returns:
        Boolean indicating if parameters are valid
    """
    try:
        tool_def = get_tool_definition_by_name(tool_name)
        required_fields = tool_def["function"]["parameters"]["properties"]

        # Check required fields
        if "required" in tool_def["function"]["parameters"]:
            required = tool_def["function"]["parameters"]["required"]
            for field in required:
                if field not in params:
                    return False

        # Validate field types and constraints
        for param_name, param_value in params.items():
            if param_name in required_fields:
                field_def = required_fields[param_name]

                # Type validation
                expected_type = field_def.get("type")
                if expected_type == "string" and not isinstance(param_value, str):
                    return False
                elif expected_type == "integer" and not isinstance(param_value, int):
                    return False
                elif expected_type == "number" and not isinstance(param_value, (int, float)):
                    return False

                # Enum validation
                if "enum" in field_def and param_value not in field_def["enum"]:
                    return False

        return True

    except ValueError:
        return False


def format_tool_result(tool_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format the result from an MCP tool call for the AI agent.

    Args:
        tool_name: Name of the tool that was called
        result: Raw result from the MCP tool

    Returns:
        Formatted result suitable for AI agent consumption
    """
    formatted_result = {
        "tool_name": tool_name,
        "success": result.get("success", False),
        "timestamp": result.get("timestamp"),
        "execution_details": {}
    }

    if result.get("success"):
        if tool_name == "add_task":
            formatted_result["execution_details"] = {
                "task_id": result.get("task", {}).get("id"),
                "title": result.get("task", {}).get("title"),
                "message": result.get("message", "Task added successfully")
            }
        elif tool_name == "list_tasks":
            formatted_result["execution_details"] = {
                "task_count": len(result.get("tasks", [])),
                "tasks": result.get("tasks", []),
                "message": result.get("message", "Tasks retrieved successfully")
            }
        elif tool_name in ["update_task", "complete_task"]:
            formatted_result["execution_details"] = {
                "task_id": result.get("task", {}).get("id"),
                "title": result.get("task", {}).get("title"),
                "completed": result.get("task", {}).get("completed", False),
                "message": result.get("message", f"Task {tool_name.replace('_', ' ').title()} successfully")
            }
        elif tool_name == "delete_task":
            formatted_result["execution_details"] = {
                "task_id": result.get("task_id"),
                "message": result.get("message", "Task deleted successfully")
            }
    else:
        formatted_result["execution_details"] = {
            "error": result.get("message", "Unknown error occurred"),
            "error_code": result.get("error_code")
        }

    return formatted_result