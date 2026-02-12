"""Context reconstruction service for AI agent."""
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from ..models.task import Task
from ..models.tool_call_log import ToolCallLog
from ..db import get_session
from ..exceptions.ai_exceptions import ContextRetrievalError
from ..schemas.ai_schemas import MCPToolName


logger = logging.getLogger(__name__)


class ContextReconstructor:
    """Service for reconstructing conversation context from database per request."""

    def __init__(self):
        """Initialize the context reconstructor."""
        logger.info("ContextReconstructor initialized")

    async def reconstruct_context(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Reconstruct conversation context for a user from database.

        Args:
            user_id: ID of the user whose context to reconstruct
            limit: Maximum number of recent interactions to include

        Returns:
            List of message dictionaries representing the conversation context
        """
        try:
            # Get recent tasks for context
            recent_tasks = await self._get_recent_tasks(user_id, limit=5)

            # Get recent tool calls for context
            recent_tool_calls = await self._get_recent_tool_calls(user_id, limit=5)

            # Build context messages
            context_messages = []

            # Add system message about the user's tasks
            if recent_tasks:
                task_info = self._format_task_info(recent_tasks)
                context_messages.append({
                    "role": "system",
                    "content": f"Here are the user's recent tasks: {task_info}"
                })

            # Add recent tool call information
            if recent_tool_calls:
                tool_info = self._format_tool_call_info(recent_tool_calls)
                context_messages.append({
                    "role": "system",
                    "content": f"Recent actions taken: {tool_info}"
                })

            logger.info(f"Reconstructed context for user {user_id} with {len(context_messages)} messages")
            return context_messages

        except Exception as e:
            logger.error(f"Error reconstructing context for user {user_id}: {str(e)}")
            raise ContextRetrievalError(f"Failed to reconstruct context: {str(e)}")

    async def _get_recent_tasks(self, user_id: str, limit: int = 10) -> List[Task]:
        """Get recent tasks for a user to provide context."""
        try:
            async with get_session() as session:
                # Query recent tasks for the user
                statement = (
                    select(Task)
                    .where(Task.user_id == user_id)
                    .order_by(Task.updated_at.desc())
                    .limit(limit)
                )

                result = await session.execute(statement)
                tasks = result.scalars().all()

                return tasks
        except Exception as e:
            logger.error(f"Error retrieving recent tasks for user {user_id}: {str(e)}")
            raise

    async def _get_recent_tool_calls(self, user_id: str, limit: int = 10) -> List[ToolCallLog]:
        """Get recent tool calls for a user to provide context."""
        try:
            async with get_session() as session:
                # Query recent tool calls for the user
                statement = (
                    select(ToolCallLog)
                    .where(ToolCallLog.user_id == user_id)
                    .order_by(ToolCallLog.timestamp.desc())
                    .limit(limit)
                )

                result = await session.execute(statement)
                tool_calls = result.scalars().all()

                return tool_calls
        except Exception as e:
            logger.error(f"Error retrieving recent tool calls for user {user_id}: {str(e)}")
            raise

    def _format_task_info(self, tasks: List[Task]) -> str:
        """Format task information for context."""
        if not tasks:
            return "No recent tasks found."

        task_list = []
        for task in tasks[:5]:  # Limit to first 5 tasks for brevity
            status = "completed" if task.completed else "pending"
            task_list.append(
                f"ID: {task.id}, Title: '{task.title}', "
                f"Status: {status}, Priority: {task.priority}"
            )

        return "; ".join(task_list)

    def _format_tool_call_info(self, tool_calls: List[ToolCallLog]) -> str:
        """Format tool call information for context."""
        if not tool_calls:
            return "No recent tool calls found."

        call_list = []
        for call in tool_calls[:5]:  # Limit to first 5 calls for brevity
            status = call.status.value
            call_list.append(
                f"Tool: {call.tool_name}, Status: {status}, "
                f"Time: {call.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            )

        return "; ".join(call_list)

    async def get_user_task_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get a summary of the user's tasks for broader context.

        Args:
            user_id: ID of the user

        Returns:
            Dictionary containing task summary statistics
        """
        try:
            async with get_session() as session:
                # Get all tasks for the user
                all_tasks_statement = select(Task).where(Task.user_id == user_id)
                all_result = await session.execute(all_tasks_statement)
                all_tasks = all_result.scalars().all()

                # Count tasks by status
                total_tasks = len(all_tasks)
                completed_tasks = sum(1 for task in all_tasks if task.completed)
                pending_tasks = total_tasks - completed_tasks

                # Count by priority
                priority_counts = {"high": 0, "medium": 0, "low": 0}
                for task in all_tasks:
                    if task.priority in priority_counts:
                        priority_counts[task.priority] += 1

                summary = {
                    "total_tasks": total_tasks,
                    "completed_tasks": completed_tasks,
                    "pending_tasks": pending_tasks,
                    "priority_breakdown": priority_counts,
                    "last_updated_task": max(
                        (task.updated_at for task in all_tasks),
                        default=None
                    ).isoformat() if all_tasks else None
                }

                return summary

        except Exception as e:
            logger.error(f"Error getting user task summary for {user_id}: {str(e)}")
            raise ContextRetrievalError(f"Failed to get user task summary: {str(e)}")

    async def limit_context_size(self, context: List[Dict[str, Any]], max_tokens: int = 2000) -> List[Dict[str, Any]]:
        """
        Limit the context size to prevent exceeding model limits.

        Args:
            context: List of context messages
            max_tokens: Maximum number of tokens allowed

        Returns:
            Trimmed context list
        """
        # Simple estimation: assume ~4 characters per token
        estimated_chars = 0
        limited_context = []

        for message in reversed(context):  # Start from most recent
            content = message.get("content", "")
            estimated_chars += len(content)

            if estimated_chars > max_tokens * 4:  # 4 chars per token approximation
                break

            limited_context.insert(0, message)  # Insert at beginning to maintain order

        logger.info(f"Limited context from {len(context)} to {len(limited_context)} messages")
        return limited_context