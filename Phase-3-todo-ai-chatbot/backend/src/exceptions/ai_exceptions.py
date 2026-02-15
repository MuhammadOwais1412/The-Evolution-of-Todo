"""Base exception classes for AI agent functionality."""


class AIAgentException(Exception):
    """Base exception for AI agent related errors."""

    def __init__(self, message: str, error_code: str = "AI_AGENT_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.error_code}] {self.message}"


class AIProcessingError(AIAgentException):
    """Raised when there's an error during AI processing."""

    def __init__(self, message: str = "Error occurred during AI processing"):
        super().__init__(message, "AI_PROCESSING_ERROR")


class ToolExecutionError(AIAgentException):
    """Raised when there's an error executing an MCP tool."""

    def __init__(self, message: str = "Error occurred while executing an MCP tool"):
        super().__init__(message, "TOOL_EXECUTION_ERROR")


class ContextRetrievalError(AIAgentException):
    """Raised when there's an error retrieving conversation context."""

    def __init__(self, message: str = "Failed to retrieve conversation context"):
        super().__init__(message, "CONTEXT_RETRIEVAL_ERROR")


class InvalidToolParametersError(AIAgentException):
    """Raised when MCP tool parameters are invalid."""

    def __init__(self, message: str = "Invalid parameters provided to MCP tool"):
        super().__init__(message, "INVALID_TOOL_PARAMETERS")


class UserPermissionError(AIAgentException):
    """Raised when a user doesn't have permission to perform an action."""

    def __init__(self, message: str = "User doesn't have permission to perform this action"):
        super().__init__(message, "USER_PERMISSION_ERROR")


class AIConfigurationError(AIAgentException):
    """Raised when there's an issue with AI configuration."""

    def __init__(self, message: str = "AI configuration error"):
        super().__init__(message, "AI_CONFIGURATION_ERROR")


class ToolNotFoundError(AIAgentException):
    """Raised when an MCP tool is not found."""

    def __init__(self, message: str = "Requested MCP tool not found"):
        super().__init__(message, "TOOL_NOT_FOUND")


class RateLimitExceededError(AIAgentException):
    """Raised when AI request rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded for AI requests"):
        super().__init__(message, "RATE_LIMIT_EXCEEDED")


class InvalidRequestError(AIAgentException):
    """Raised when an AI request is invalid."""

    def __init__(self, message: str = "Invalid request format"):
        super().__init__(message, "INVALID_REQUEST")


class AIServiceUnavailableError(AIAgentException):
    """Raised when the AI service is unavailable."""

    def __init__(self, message: str = "AI service is temporarily unavailable"):
        super().__init__(message, "AI_SERVICE_UNAVAILABLE")


class ConfirmationRequiredError(AIAgentException):
    """Raised when a confirmation is required before proceeding with an action."""

    def __init__(self, message: str = "Confirmation required before proceeding with this action"):
        super().__init__(message, "CONFIRMATION_REQUIRED")


class UnsafeContentError(AIAgentException):
    """Raised when AI generates potentially unsafe content."""

    def __init__(self, message: str = "Potentially unsafe content detected"):
        super().__init__(message, "UNSAFE_CONTENT_DETECTED")


class AuditLoggingError(AIAgentException):
    """Raised when there's an error logging audit information."""

    def __init__(self, message: str = "Error occurred while logging audit information"):
        super().__init__(message, "AUDIT_LOGGING_ERROR")


class ConfirmationError(AIAgentException):
    """Raised when there's an error with confirmation handling."""

    def __init__(self, message: str = "Error occurred during confirmation handling"):
        super().__init__(message, "CONFIRMATION_ERROR")