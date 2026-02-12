"""Confirmation handler for managing user confirmations for destructive operations."""
import logging
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.tool_call_log import ToolCallLog, ToolCallStatus
from ..db import get_session
from ..exceptions.ai_exceptions import ConfirmationError, UserPermissionError
from ..schemas.ai_schemas import MCPToolName


logger = logging.getLogger(__name__)


class ConfirmationHandler:
    """Handler for managing user confirmations for potentially destructive operations."""

    def __init__(self):
        """Initialize the confirmation handler."""
        logger.info("ConfirmationHandler initialized")
        # In-memory storage for pending confirmations
        # In a production system, this would be stored in a database with expiration
        self.pending_confirmations = {}

    async def create_confirmation_request(
        self,
        user_id: str,
        tool_name: str,
        tool_params: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a confirmation request for a potentially destructive operation.

        Args:
            user_id: ID of the user requesting the operation
            tool_name: Name of the tool that requires confirmation
            tool_params: Parameters for the tool call
            context: Additional context for the confirmation

        Returns:
            Confirmation ID that can be used to approve/reject the operation
        """
        confirmation_id = str(uuid.uuid4())

        confirmation_data = {
            "id": confirmation_id,
            "user_id": user_id,
            "tool_name": tool_name,
            "tool_params": tool_params,
            "context": context,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(minutes=10),  # Expires in 10 minutes
            "status": "pending"
        }

        # Store in memory (in production, store in database with TTL)
        self.pending_confirmations[confirmation_id] = confirmation_data

        logger.info(f"Created confirmation request {confirmation_id} for user {user_id}, tool {tool_name}")
        return confirmation_id

    async def validate_confirmation(
        self,
        confirmation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Validate a confirmation request for a specific user.

        Args:
            confirmation_id: ID of the confirmation to validate
            user_id: ID of the user attempting to validate

        Returns:
            Confirmation data if valid, raises exception if invalid
        """
        if confirmation_id not in self.pending_confirmations:
            raise ConfirmationError(f"Confirmation {confirmation_id} not found")

        confirmation_data = self.pending_confirmations[confirmation_id]

        if confirmation_data["status"] != "pending":
            raise ConfirmationError(f"Confirmation {confirmation_id} is not pending")

        if confirmation_data["user_id"] != user_id:
            raise UserPermissionError("User does not have permission to confirm this action")

        if confirmation_data["expires_at"] < datetime.utcnow():
            # Remove expired confirmation
            del self.pending_confirmations[confirmation_id]
            raise ConfirmationError(f"Confirmation {confirmation_id} has expired")

        logger.info(f"Validated confirmation {confirmation_id} for user {user_id}")
        return confirmation_data

    async def approve_confirmation(
        self,
        confirmation_id: str,
        user_id: str,
        executor_func = None  # Function to execute the confirmed action
    ) -> Dict[str, Any]:
        """
        Approve a confirmation and execute the associated action.

        Args:
            confirmation_id: ID of the confirmation to approve
            user_id: ID of the user approving
            executor_func: Optional function to execute the confirmed action

        Returns:
            Result of the action execution
        """
        confirmation_data = await self.validate_confirmation(confirmation_id, user_id)

        # Update status to approved
        confirmation_data["status"] = "approved"
        confirmation_data["approved_at"] = datetime.utcnow()

        # Execute the action if an executor function is provided
        result = None
        if executor_func:
            try:
                result = await executor_func(
                    confirmation_data["tool_name"],
                    confirmation_data["tool_params"]
                )

                # Log the successful execution
                await self._log_tool_call(
                    user_id=user_id,
                    tool_name=confirmation_data["tool_name"],
                    tool_params=confirmation_data["tool_params"],
                    result=result,
                    status=ToolCallStatus.SUCCESS
                )
            except Exception as e:
                # Log the failed execution
                error_result = {"error": str(e)}
                await self._log_tool_call(
                    user_id=user_id,
                    tool_name=confirmation_data["tool_name"],
                    tool_params=confirmation_data["tool_params"],
                    result=error_result,
                    status=ToolCallStatus.ERROR
                )
                raise

        # Remove the confirmation from pending list
        del self.pending_confirmations[confirmation_id]

        logger.info(f"Approved confirmation {confirmation_id} for user {user_id}")
        return {
            "confirmation_id": confirmation_id,
            "status": "approved",
            "result": result,
            "tool_name": confirmation_data["tool_name"],
            "tool_params": confirmation_data["tool_params"]
        }

    async def reject_confirmation(
        self,
        confirmation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Reject a confirmation request.

        Args:
            confirmation_id: ID of the confirmation to reject
            user_id: ID of the user rejecting

        Returns:
            Confirmation rejection data
        """
        confirmation_data = await self.validate_confirmation(confirmation_id, user_id)

        # Update status to rejected
        confirmation_data["status"] = "rejected"
        confirmation_data["rejected_at"] = datetime.utcnow()

        # Remove the confirmation from pending list
        del self.pending_confirmations[confirmation_id]

        logger.info(f"Rejected confirmation {confirmation_id} for user {user_id}")
        return {
            "confirmation_id": confirmation_id,
            "status": "rejected",
            "tool_name": confirmation_data["tool_name"],
            "tool_params": confirmation_data["tool_params"]
        }

    async def get_pending_confirmations(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all pending confirmations for a user.

        Args:
            user_id: ID of the user

        Returns:
            List of pending confirmation requests
        """
        user_confirmations = []

        for confirmation_id, data in self.pending_confirmations.items():
            if (data["user_id"] == user_id and
                data["status"] == "pending" and
                data["expires_at"] >= datetime.utcnow()):
                user_confirmations.append({
                    "id": confirmation_id,
                    "tool_name": data["tool_name"],
                    "tool_params": data["tool_params"],
                    "context": data["context"],
                    "created_at": data["created_at"],
                    "expires_at": data["expires_at"]
                })

        logger.info(f"Retrieved {len(user_confirmations)} pending confirmations for user {user_id}")
        return user_confirmations

    async def _log_tool_call(
        self,
        user_id: str,
        tool_name: str,
        tool_params: Dict[str, Any],
        result: Dict[str, Any],
        status: ToolCallStatus
    ):
        """Log the tool call for audit purposes."""
        from .audit_logger import AuditLogger
        audit_logger = AuditLogger()

        await audit_logger.log_tool_call(
            user_id=user_id,
            tool_name=tool_name,
            tool_params=tool_params,
            result=result,
            status=status
        )

    async def cleanup_expired_confirmations(self):
        """Remove expired confirmations from storage."""
        current_time = datetime.utcnow()
        expired_ids = []

        for confirmation_id, data in self.pending_confirmations.items():
            if data["expires_at"] < current_time:
                expired_ids.append(confirmation_id)

        for confirmation_id in expired_ids:
            del self.pending_confirmations[confirmation_id]
            logger.info(f"Removed expired confirmation {confirmation_id}")

        return len(expired_ids)