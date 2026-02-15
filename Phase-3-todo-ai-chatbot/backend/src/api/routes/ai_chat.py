"""AI chat router for handling natural language todo commands."""
import logging
from typing import Dict, Any, Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer
from fastapi_limiter.depends import RateLimiter

from ...schemas.ai_schemas import AIChatRequest, AIChatResponse, HealthCheckResponse
from ...api.deps import get_current_user
from ...ai.agent_service import AIAgentService
from ...ai.confirmation_handler import ConfirmationHandler
from ...exceptions.ai_exceptions import (
    AIProcessingError,
    ToolExecutionError,
    ContextRetrievalError,
    UserPermissionError,
    ConfirmationError
)


# Global instances since they require async initialization
# In a real application, you might want to use a more sophisticated dependency injection system
_ai_agent_service_instance = None
_confirmation_handler_instance = None


async def get_ai_agent_service():
    """Dependency function to provide the AI agent service instance."""
    global _ai_agent_service_instance
    if _ai_agent_service_instance is None:
        _ai_agent_service_instance = AIAgentService()
    return _ai_agent_service_instance


async def get_confirmation_handler():
    """Dependency function to provide the confirmation handler instance."""
    global _confirmation_handler_instance
    if _confirmation_handler_instance is None:
        _confirmation_handler_instance = ConfirmationHandler()
    return _confirmation_handler_instance


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/ai", tags=["ai-chat"])
security = HTTPBearer()


@router.post(
    "/chat",
    response_model=AIChatResponse,
    # dependencies=[Depends(RateLimiter(times=10, seconds=60))]  # Rate limit: 10 requests per minute - TODO: Fix rate limiter syntax
)
async def ai_chat_endpoint(
    request: AIChatRequest,
    current_user: str = Depends(get_current_user),
    agent_service: AIAgentService = Depends(get_ai_agent_service)
) -> AIChatResponse:
    """
    Main AI chat endpoint that processes natural language commands and returns appropriate responses.

    Args:
        request: The AI chat request containing the user's message
        current_user: The authenticated user making the request
        agent_service: The AI agent service instance

    Returns:
        AIChatResponse containing the AI response and any tool calls made
    """
    try:
        logger.info(f"Received AI chat request from user {current_user}: {request.message}")

        # Process the command through the AI agent
        result = await agent_service.process_command(
            user_id=current_user,
            message=request.message,
            requires_confirmation=request.requires_confirmation
        )

        # Create the response
        response = AIChatResponse(
            response=result["response"],
            tool_calls=result["tool_calls"],
            requires_confirmation=result["requires_confirmation"],
            success=True,
            message="Successfully processed AI command"
        )

        logger.info(f"Successfully processed AI chat request for user {current_user}")
        return response

    except UserPermissionError as e:
        logger.warning(f"Permission error for user {current_user}: {str(e)}")
        raise HTTPException(status_code=403, detail=f"Permission denied: {str(e)}")

    except (AIProcessingError, ToolExecutionError, ContextRetrievalError) as e:
        logger.error(f"Error processing AI command for user {current_user}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing command: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in AI chat endpoint for user {current_user}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.post("/confirm/{confirmation_id}")
async def ai_confirmation_endpoint(
    confirmation_id: str,
    current_user: str = Depends(get_current_user),
    agent_service: AIAgentService = Depends(get_ai_agent_service),
    confirmation_handler: ConfirmationHandler = Depends(get_confirmation_handler)
) -> AIChatResponse:
    """
    Endpoint for handling user confirmations for potentially destructive operations.

    Args:
        confirmation_id: The ID of the confirmation being processed
        current_user: The authenticated user making the request
        agent_service: The AI agent service instance
        confirmation_handler: The confirmation handler instance

    Returns:
        AIChatResponse containing the result of the confirmed action
    """
    try:
        logger.info(f"Received confirmation {confirmation_id} from user {current_user}")

        # Validate the confirmation request
        confirmation_data = await confirmation_handler.validate_confirmation(
            confirmation_id,
            current_user
        )

        # Execute the confirmed action
        result = await agent_service._execute_mcp_tool(
            confirmation_data["tool_name"],
            confirmation_data["tool_params"]
        )

        # Create a mock response since we're bypassing the AI processing for confirmed actions
        response_content = f"Confirmed and executed {confirmation_data['tool_name']} operation successfully."

        # Create response with the executed tool call
        from ...schemas.ai_schemas import MCPToolCall, ToolCallStatus
        import json
        from datetime import datetime

        executed_tool_call = MCPToolCall(
            id=confirmation_id,
            tool_name=getattr(MCPToolName, confirmation_data["tool_name"].upper()),
            tool_params=confirmation_data["tool_params"],
            result=result,
            status=ToolCallStatus.SUCCESS,
            timestamp=datetime.utcnow()
        )

        response = AIChatResponse(
            response=response_content,
            tool_calls=[executed_tool_call],
            requires_confirmation=False,  # No further confirmation needed
            success=True,
            message="Successfully processed confirmed action"
        )

        logger.info(f"Successfully processed confirmation {confirmation_id} for user {current_user}")
        return response

    except UserPermissionError as e:
        logger.warning(f"Permission error for user {current_user}: {str(e)}")
        raise HTTPException(status_code=403, detail=f"Permission denied: {str(e)}")

    except ConfirmationError as e:
        logger.warning(f"Confirmation error for user {current_user}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Confirmation error: {str(e)}")

    except (AIProcessingError, ToolExecutionError, ContextRetrievalError) as e:
        logger.error(f"Error processing confirmation for user {current_user}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing confirmation: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in confirmation endpoint for user {current_user}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/pending-confirmations")
async def get_pending_confirmations(
    current_user: str = Depends(get_current_user),
    confirmation_handler: ConfirmationHandler = Depends(get_confirmation_handler)
) -> Dict[str, Any]:
    """
    Get all pending confirmations for the current user.

    Args:
        current_user: The authenticated user making the request
        confirmation_handler: The confirmation handler instance

    Returns:
        Dictionary containing pending confirmations
    """
    try:
        logger.info(f"Retrieving pending confirmations for user {current_user}")

        pending_confirmations = await confirmation_handler.get_pending_confirmations(
            current_user
        )

        return {
            "user_id": current_user,
            "pending_confirmations": pending_confirmations,
            "count": len(pending_confirmations),
            "success": True,
            "message": f"Retrieved {len(pending_confirmations)} pending confirmations"
        }

    except Exception as e:
        logger.error(f"Error retrieving pending confirmations for user {current_user}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving pending confirmations")


@router.post("/reject/{confirmation_id}")
async def reject_confirmation(
    confirmation_id: str,
    current_user: str = Depends(get_current_user),
    confirmation_handler: ConfirmationHandler = Depends(get_confirmation_handler)
) -> Dict[str, Any]:
    """
    Endpoint for rejecting a pending confirmation.

    Args:
        confirmation_id: The ID of the confirmation being rejected
        current_user: The authenticated user making the request
        confirmation_handler: The confirmation handler instance

    Returns:
        Dictionary with rejection result
    """
    try:
        logger.info(f"Received rejection for confirmation {confirmation_id} from user {current_user}")

        result = await confirmation_handler.reject_confirmation(
            confirmation_id,
            current_user
        )

        return {
            "confirmation_id": result["id"],
            "status": result["status"],
            "tool_name": result["tool_name"],
            "success": True,
            "message": f"Successfully rejected confirmation {confirmation_id}"
        }

    except UserPermissionError as e:
        logger.warning(f"Permission error for user {current_user['user_id']}: {str(e)}")
        raise HTTPException(status_code=403, detail=f"Permission denied: {str(e)}")

    except ConfirmationError as e:
        logger.warning(f"Confirmation error for user {current_user['user_id']}: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Confirmation error: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in rejection endpoint for user {current_user['user_id']}: {str(e)}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


@router.get("/tool-call-log")
async def get_tool_call_logs(
    current_user: str = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0,
    tool_name: Optional[str] = None,
    status: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    agent_service: AIAgentService = Depends(get_ai_agent_service)
) -> Dict[str, Any]:
    """
    Endpoint for retrieving audit logs of tool calls made by the AI agent.

    Args:
        current_user: The authenticated user making the request
        limit: Maximum number of records to return
        offset: Number of records to skip
        tool_name: Optional filter for specific tool name
        status: Optional filter for specific status
        start_date: Optional filter for start date
        end_date: Optional filter for end date
        agent_service: The AI agent service instance

    Returns:
        Dictionary containing the audit log entries
    """
    try:
        logger.info(f"Retrieving tool call logs for user {current_user}")

        from ...ai.audit_logger import AuditLogger
        audit_logger = AuditLogger()

        # Convert string status to enum if provided
        from ...models.tool_call_log import ToolCallStatus
        status_enum = None
        if status:
            try:
                status_enum = ToolCallStatus(status.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid status: {status}")

        # Convert string tool name to enum if provided
        from ...schemas.ai_schemas import MCPToolName
        tool_name_enum = None
        if tool_name:
            try:
                tool_name_enum = MCPToolName(tool_name.lower())
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid tool name: {tool_name}")

        # Parse date strings if provided
        from datetime import datetime
        start_datetime = None
        end_datetime = None
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid start date format: {start_date}")

        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid end date format: {end_date}")

        # Retrieve the logs
        logs = await audit_logger.get_tool_call_history(
            user_id=current_user,
            tool_name=tool_name_enum.value if tool_name_enum else None,
            status=status_enum if status_enum else None,
            limit=limit,
            offset=offset
        )

        # Format the response
        formatted_logs = []
        for log in logs:
            formatted_logs.append({
                "id": log.id,
                "user_id": log.user_id,
                "tool_name": log.tool_name,
                "tool_params": log.tool_params,
                "result": log.result,
                "status": log.status.value,
                "execution_time_ms": log.execution_time_ms,
                "timestamp": log.timestamp.isoformat(),
                "error_details": log.error_details
            })

        total_count = len(formatted_logs)  # In a real implementation, this would be a separate count query

        return {
            "user_id": current_user,
            "logs": formatted_logs,
            "pagination": {
                "limit": limit,
                "offset": offset,
                "total": total_count,  # This would be from a count query in real implementation
                "has_more": len(formatted_logs) == limit
            },
            "filters": {
                "tool_name": tool_name,
                "status": status,
                "start_date": start_date,
                "end_date": end_date
            },
            "success": True,
            "message": f"Retrieved {len(formatted_logs)} tool call logs"
        }

    except HTTPException:
        raise  # Re-raise HTTP exceptions

    except Exception as e:
        logger.error(f"Error retrieving tool call logs for user {current_user['user_id']}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving tool call logs")


@router.get("/health", response_model=HealthCheckResponse)
async def ai_health_check(agent_service: AIAgentService = Depends(get_ai_agent_service)) -> HealthCheckResponse:
    """
    Health check endpoint for the AI chat service.

    Args:
        agent_service: The AI agent service instance

    Returns:
        HealthCheckResponse indicating the service status
    """
    try:
        checks = {
            "agent_initialized": True,
            "ai_model_connection": False,
            "database_connection": False,
            "mcp_tools_availability": {}
        }

        # Check AI model connection
        try:
            # Attempt a simple call to verify AI model is accessible
            # This is a basic check - in practice, you might ping the API endpoint
            if hasattr(agent_service, 'client'):
                checks["ai_model_connection"] = True
        except:
            checks["ai_model_connection"] = False

        # Check database connection by attempting a simple query
        try:
            from ...db import get_session
            async with get_session() as session:
                # Execute a simple query to test DB connection
                await session.exec("SELECT 1")
                checks["database_connection"] = True
        except:
            checks["database_connection"] = False

        # Check MCP tool availability
        try:
            from ...mcp.tools.task_operations import add_task, list_tasks, update_task, complete_task, delete_task
            checks["mcp_tools_availability"] = {
                "add_task": True,
                "list_tasks": True,
                "update_task": True,
                "complete_task": True,
                "delete_task": True
            }
        except Exception as e:
            checks["mcp_tools_availability"] = {
                "error": str(e)
            }

        # Overall status determination
        overall_status = "healthy" if all([
            checks["agent_initialized"],
            checks["ai_model_connection"],
            checks["database_connection"],
            "error" not in checks["mcp_tools_availability"]
        ]) else "unhealthy"

        health_status = {
            "status": overall_status,
            "service": "ai-chat",
            "timestamp": __import__('datetime').datetime.utcnow().isoformat(),
            "checks": checks
        }

        logger.info(f"AI chat service health check completed: {overall_status}")
        return HealthCheckResponse(**health_status)

    except Exception as e:
        logger.error(f"AI chat service health check failed: {str(e)}")
        return HealthCheckResponse(
            status="unhealthy",
            service="ai-chat",
            timestamp=__import__('datetime').datetime.utcnow().isoformat(),
            checks={
                "agent_initialized": False,
                "error": str(e)
            }
        )


@router.get("/metrics")
async def get_ai_metrics(
    current_user: str = Depends(get_current_user),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    agent_service: AIAgentService = Depends(get_ai_agent_service)
) -> Dict[str, Any]:
    """
    Endpoint for retrieving AI agent usage metrics.

    Args:
        current_user: The authenticated user making the request
        start_date: Optional start date for metrics
        end_date: Optional end date for metrics
        agent_service: The AI agent service instance

    Returns:
        Dictionary containing usage metrics
    """
    try:
        from ...ai.audit_logger import AuditLogger
        from datetime import datetime

        audit_logger = AuditLogger()

        # Parse date strings if provided
        start_datetime = None
        end_datetime = None
        if start_date:
            try:
                start_datetime = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid start date format: {start_date}")

        if end_date:
            try:
                end_datetime = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail=f"Invalid end date format: {end_date}")

        # Get user usage stats
        stats = await audit_logger.get_user_tool_usage_stats(
            user_id=current_user,
            start_date=start_datetime,
            end_date=end_datetime
        )

        # Add additional metrics
        metrics = {
            "user_id": current_user,
            "period": {
                "start": start_date,
                "end": end_date
            },
            "usage_stats": stats,
            "tool_effectiveness": {},  # Could calculate success rates per tool
            "avg_response_time": stats.get("average_execution_time_ms"),
            "trend_analysis": {},  # Could analyze trends over time
            "success_rate": 0.0,  # Calculate success rate
            "total_interactions": stats.get("total_calls", 0)
        }

        # Calculate success rate if we have data
        if stats.get("total_calls", 0) > 0:
            successful_calls = stats.get("successful_calls", 0)
            metrics["success_rate"] = successful_calls / stats["total_calls"]

        logger.info(f"Retrieved metrics for user {current_user}")
        return {
            "metrics": metrics,
            "success": True,
            "message": "Successfully retrieved AI agent usage metrics"
        }

    except Exception as e:
        logger.error(f"Error retrieving metrics for user {current_user}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving metrics")


@router.get("/usage-stats")
async def get_user_usage_stats(
    current_user: str = Depends(get_current_user),
    agent_service: AIAgentService = Depends(get_ai_agent_service)
) -> Dict[str, Any]:
    """
    Get usage statistics for the current user.

    Args:
        current_user: The authenticated user making the request
        agent_service: The AI agent service instance

    Returns:
        Dictionary containing usage statistics
    """
    try:
        # In a real implementation, this would call the audit logger to get stats
        # For now, we'll return placeholder data
        from ...ai.audit_logger import AuditLogger
        audit_logger = AuditLogger()

        stats = await audit_logger.get_user_tool_usage_stats(current_user)

        return {
            "user_id": current_user,
            "stats": stats,
            "success": True,
            "message": "Successfully retrieved usage stats"
        }

    except Exception as e:
        logger.error(f"Error retrieving usage stats for user {current_user}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving usage stats")