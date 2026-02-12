"""Audit logger service for comprehensive logging of all AI-initiated tool calls."""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.tool_call_log import ToolCallLog, ToolCallStatus
from ..db import get_session
from ..exceptions.ai_exceptions import AuditLoggingError


logger = logging.getLogger(__name__)


class AuditLogger:
    """Service class for logging all AI agent tool calls with comprehensive metadata."""

    def __init__(self):
        """Initialize the audit logger service."""
        logger.info("AuditLogger initialized")

    async def log_tool_call(
        self,
        user_id: str,
        tool_name: str,
        tool_params: Dict[str, Any],
        result: Dict[str, Any],
        status: ToolCallStatus,
        execution_time_ms: Optional[float] = None,
        error_details: Optional[Dict[str, Any]] = None
    ) -> ToolCallLog:
        """
        Create a ToolCallLog entry in the database for an AI-initiated tool call.

        Args:
            user_id: ID of the user who initiated the tool call
            tool_name: Name of the tool that was called
            tool_params: Parameters passed to the tool
            result: Result of the tool execution
            status: Status of the tool call (SUCCESS, ERROR, PENDING)
            execution_time_ms: Execution time in milliseconds (optional)
            error_details: Details about any errors that occurred (optional)

        Returns:
            The created ToolCallLog entry
        """
        try:
            async with get_session() as session:
                tool_call_log = ToolCallLog(
                    user_id=user_id,
                    tool_name=tool_name,
                    tool_params=tool_params,
                    result=result,
                    status=status,
                    execution_time_ms=execution_time_ms,
                    error_details=error_details
                )

                session.add(tool_call_log)
                await session.commit()
                await session.refresh(tool_call_log)

                logger.info(f"Logged tool call for user {user_id}, tool {tool_name}, status {status}")
                return tool_call_log

        except Exception as e:
            logger.error(f"Error logging tool call: {str(e)}")
            raise AuditLoggingError(f"Failed to log tool call: {str(e)}")

    async def get_tool_call_history(
        self,
        user_id: str,
        tool_name: Optional[str] = None,
        status: Optional[ToolCallStatus] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[ToolCallLog]:
        """
        Retrieve audit history for a user's tool calls with optional filters.

        Args:
            user_id: ID of the user whose tool call history to retrieve
            tool_name: Optional filter for specific tool name
            status: Optional filter for specific status
            limit: Maximum number of records to return
            offset: Number of records to skip

        Returns:
            List of ToolCallLog entries matching the criteria
        """
        try:
            async with get_session() as session:
                from sqlmodel import select

                query = select(ToolCallLog).where(ToolCallLog.user_id == user_id)

                if tool_name:
                    query = query.where(ToolCallLog.tool_name == tool_name)

                if status:
                    query = query.where(ToolCallLog.status == status)

                query = query.order_by(ToolCallLog.timestamp.desc()).offset(offset).limit(limit)

                result = await session.execute(query)
                tool_calls = result.scalars().all()

                logger.info(f"Retrieved {len(tool_calls)} tool call logs for user {user_id}")
                return tool_calls

        except Exception as e:
            logger.error(f"Error retrieving tool call history for user {user_id}: {str(e)}")
            raise AuditLoggingError(f"Failed to retrieve tool call history: {str(e)}")

    async def get_tool_call_by_id(self, log_id: int) -> Optional[ToolCallLog]:
        """
        Retrieve a specific tool call log by its ID.

        Args:
            log_id: ID of the tool call log to retrieve

        Returns:
            ToolCallLog entry if found, None otherwise
        """
        try:
            async with get_session() as session:
                from sqlmodel import select

                query = select(ToolCallLog).where(ToolCallLog.id == log_id)
                result = await session.execute(query)
                tool_call = result.scalar_one_or_none()

                return tool_call

        except Exception as e:
            logger.error(f"Error retrieving tool call log {log_id}: {str(e)}")
            raise AuditLoggingError(f"Failed to retrieve tool call log: {str(e)}")

    async def get_user_tool_usage_stats(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get usage statistics for a user's tool calls.

        Args:
            user_id: ID of the user to get stats for
            start_date: Optional start date for filtering
            end_date: Optional end date for filtering

        Returns:
            Dictionary containing usage statistics
        """
        try:
            async with get_session() as session:
                from sqlmodel import select, func

                query = select(ToolCallLog).where(ToolCallLog.user_id == user_id)

                if start_date:
                    query = query.where(ToolCallLog.timestamp >= start_date)

                if end_date:
                    query = query.where(ToolCallLog.timestamp <= end_date)

                result = await session.execute(query)
                all_calls = result.scalars().all()

                # Calculate statistics
                total_calls = len(all_calls)
                successful_calls = sum(1 for call in all_calls if call.status == ToolCallStatus.SUCCESS)
                error_calls = sum(1 for call in all_calls if call.status == ToolCallStatus.ERROR)
                pending_calls = sum(1 for call in all_calls if call.status == ToolCallStatus.PENDING)

                # Tool usage breakdown
                tool_usage = {}
                for call in all_calls:
                    tool_name = call.tool_name
                    if tool_name in tool_usage:
                        tool_usage[tool_name] += 1
                    else:
                        tool_usage[tool_name] = 1

                # Average execution time
                exec_times = [call.execution_time_ms for call in all_calls if call.execution_time_ms is not None]
                avg_execution_time = sum(exec_times) / len(exec_times) if exec_times else None

                stats = {
                    "total_calls": total_calls,
                    "successful_calls": successful_calls,
                    "error_calls": error_calls,
                    "pending_calls": pending_calls,
                    "tool_usage_breakdown": tool_usage,
                    "average_execution_time_ms": avg_execution_time,
                    "date_range": {
                        "start": start_date.isoformat() if start_date else None,
                        "end": end_date.isoformat() if end_date else None
                    } if start_date or end_date else None
                }

                logger.info(f"Retrieved usage stats for user {user_id}: {stats}")
                return stats

        except Exception as e:
            logger.error(f"Error calculating usage stats for user {user_id}: {str(e)}")
            raise AuditLoggingError(f"Failed to calculate usage stats: {str(e)}")

    async def cleanup_old_logs(
        self,
        days_to_keep: int = 90,
        limit: int = 1000
    ) -> int:
        """
        Clean up old tool call logs to manage database size.

        Args:
            days_to_keep: Number of days of logs to keep
            limit: Maximum number of records to delete in one operation

        Returns:
            Number of records deleted
        """
        try:
            from sqlmodel import select, delete
            from sqlalchemy import and_
            from datetime import timedelta

            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)

            async with get_session() as session:
                # First, count how many records would be affected
                count_query = select(func.count(ToolCallLog.id)).where(
                    ToolCallLog.timestamp < cutoff_date
                )
                count_result = await session.execute(count_query)
                records_to_delete = count_result.scalar_one()

                if records_to_delete == 0:
                    logger.info("No old logs to clean up")
                    return 0

                # Actually delete the records
                delete_query = (
                    delete(ToolCallLog)
                    .where(ToolCallLog.timestamp < cutoff_date)
                    .limit(limit)
                )

                result = await session.execute(delete_query)
                deleted_count = result.rowcount

                await session.commit()

                logger.info(f"Cleaned up {deleted_count} old tool call logs older than {days_to_keep} days")
                return deleted_count

        except Exception as e:
            logger.error(f"Error cleaning up old logs: {str(e)}")
            raise AuditLoggingError(f"Failed to clean up old logs: {str(e)}")

    async def log_batch_tool_calls(
        self,
        tool_calls_data: List[Dict[str, Any]]
    ) -> List[ToolCallLog]:
        """
        Log multiple tool calls in a single transaction for efficiency.

        Args:
            tool_calls_data: List of dictionaries containing tool call data
                           Each dict should have: user_id, tool_name, tool_params,
                           result, status, execution_time_ms, error_details

        Returns:
            List of created ToolCallLog entries
        """
        try:
            async with get_session() as session:
                created_logs = []

                for call_data in tool_calls_data:
                    tool_call_log = ToolCallLog(
                        user_id=call_data["user_id"],
                        tool_name=call_data["tool_name"],
                        tool_params=call_data["tool_params"],
                        result=call_data["result"],
                        status=call_data["status"],
                        execution_time_ms=call_data.get("execution_time_ms"),
                        error_details=call_data.get("error_details")
                    )

                    session.add(tool_call_log)
                    created_logs.append(tool_call_log)

                await session.commit()

                # Refresh all created logs to get their IDs
                for log in created_logs:
                    await session.refresh(log)

                logger.info(f"Logged {len(created_logs)} batch tool calls")
                return created_logs

        except Exception as e:
            logger.error(f"Error logging batch tool calls: {str(e)}")
            raise AuditLoggingError(f"Failed to log batch tool calls: {str(e)}")