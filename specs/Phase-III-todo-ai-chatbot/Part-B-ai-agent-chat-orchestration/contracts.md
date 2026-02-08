# API Contracts: AI Agent & Chat Orchestration

## Overview
This document defines the API contracts for the AI agent and chat orchestration system that operates through MCP tools with stateless architecture.

## 1. AI Chat Endpoint

### POST /api/ai/chat

**Description**: Process a natural language message from a user and generate a response, potentially executing MCP tools as needed.

**Authentication**: Bearer token (JWT from Better Auth)

**Request Headers**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body**:
```json
{
  "message": "string (required) - Natural language command from user",
  "context": {
    "conversation_id": "string (optional) - Session identifier for advanced scenarios",
    "include_history": "boolean (optional) - Whether to include conversation history in context, default: false"
  }
}
```

**Request Validation**:
- `message` must be 1-1000 characters
- `context.conversation_id` if provided must be a valid UUID string
- Request size must not exceed 10KB

**Response Codes**:
- `200 OK` - Successfully processed message
- `400 Bad Request` - Invalid request format
- `401 Unauthorized` - Invalid or expired token
- `403 Forbidden` - User lacks required permissions
- `422 Unprocessable Entity` - Message could not be processed
- `500 Internal Server Error` - Server error occurred

**Success Response (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "response": "string - AI-generated response to user",
    "tool_calls": [
      {
        "id": "string - Unique identifier for the tool call",
        "tool_name": "string - One of: add_task, list_tasks, update_task, complete_task, delete_task",
        "tool_params": "object - Parameters passed to the tool",
        "result": "object - Result from the tool execution",
        "status": "string - One of: success, error",
        "timestamp": "string - ISO 8601 datetime of execution"
      }
    ],
    "requires_confirmation": "boolean - Whether user confirmation is needed for any actions",
    "next_prompt": "string (optional) - Follow-up question or prompt from AI"
  },
  "meta": {
    "processing_time_ms": "number - Time taken to process the request",
    "tokens_used": {
      "input": "number - Input tokens consumed",
      "output": "number - Output tokens consumed"
    }
  }
}
```

**Error Response (4xx/5xx)**:
```json
{
  "status": "error",
  "error": {
    "code": "string - Error code (AUTH_FAILED, VALIDATION_ERROR, etc.)",
    "message": "string - Human-readable error message",
    "details": "object (optional) - Additional error details"
  },
  "meta": {
    "request_id": "string - Unique identifier for the request"
  }
}
```

**Examples**:

_Request_:
```json
{
  "message": "Add a task to buy groceries tomorrow"
}
```

_Success Response_:
```json
{
  "status": "success",
  "data": {
    "response": "I've added a task to buy groceries for tomorrow.",
    "tool_calls": [
      {
        "id": "call_abc123",
        "tool_name": "add_task",
        "tool_params": {
          "user_id": "user-xyz789",
          "title": "Buy groceries",
          "description": "Tomorrow's grocery shopping",
          "priority": "medium"
        },
        "result": {
          "id": 123,
          "user_id": "user-xyz789",
          "title": "Buy groceries",
          "description": "Tomorrow's grocery shopping",
          "completed": false,
          "created_at": "2023-01-01T10:00:00",
          "updated_at": "2023-01-01T10:00:00",
          "priority": "medium"
        },
        "status": "success",
        "timestamp": "2023-01-01T10:00:00Z"
      }
    ],
    "requires_confirmation": false,
    "next_prompt": null
  },
  "meta": {
    "processing_time_ms": 850,
    "tokens_used": {
      "input": 24,
      "output": 18
    }
  }
}
```

## 2. Tool Call Audit Log Endpoint

### GET /api/ai/tool-call-log

**Description**: Retrieve audit logs for tool calls made by the AI agent on behalf of the user.

**Authentication**: Bearer token (JWT from Better Auth)

**Query Parameters**:
```
limit: number (optional, default: 20, max: 100) - Number of records to return
offset: number (optional, default: 0) - Offset for pagination
start_date: string (optional) - ISO 8601 date to filter logs from
end_date: string (optional) - ISO 8601 date to filter logs until
tool_name: string (optional) - Filter by specific tool name
status: string (optional) - Filter by status ('success', 'error', 'pending')
```

**Response (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "logs": [
      {
        "id": "string - Unique identifier for the log entry",
        "tool_name": "string - Name of the MCP tool called",
        "tool_params": "object - Parameters passed to the tool",
        "result_summary": "string - Brief summary of the result",
        "status": "string - One of: success, error, pending",
        "timestamp": "string - ISO 8601 datetime of execution",
        "ai_confidence": "number (optional) - Confidence score from AI agent"
      }
    ],
    "pagination": {
      "total": "number - Total number of records available",
      "limit": "number - Requested limit",
      "offset": "number - Requested offset",
      "has_more": "boolean - Whether more records are available"
    }
  }
}
```

## 3. AI Agent Health Check

### GET /api/ai/health

**Description**: Check the health status of the AI agent service.

**Authentication**: Optional (public endpoint)

**Response (200 OK)**:
```json
{
  "status": "success",
  "data": {
    "service": "ai-agent",
    "version": "string - Version of the AI agent service",
    "model": "string - Active AI model identifier",
    "connected_to_mcp": "boolean - Whether MCP tools are accessible",
    "last_heartbeat": "string - ISO 8601 datetime of last health check",
    "tool_availability": {
      "add_task": "boolean",
      "list_tasks": "boolean",
      "update_task": "boolean",
      "complete_task": "boolean",
      "delete_task": "boolean"
    }
  }
}
```

## Rate Limits

- **Standard users**: 100 requests per hour per user
- **Authenticated users**: 500 requests per hour per user
- **Tool execution**: 50 MCP tool calls per hour per user

Rate limit headers will be included in responses:
- `X-RateLimit-Limit`: Request limit for the time window
- `X-RateLimit-Remaining`: Remaining requests in the time window
- `X-RateLimit-Reset`: Unix timestamp for when the rate limit resets

## Error Codes

| Code | Description |
|------|-------------|
| AUTH_FAILED | Authentication token is invalid or expired |
| VALIDATION_ERROR | Request body failed validation |
| TOOL_EXECUTION_ERROR | Error occurred while executing an MCP tool |
| CONTEXT_RETRIEVAL_ERROR | Failed to retrieve conversation context |
| AI_PROCESSING_ERROR | Error occurred during AI processing |
| QUOTA_EXCEEDED | User has exceeded rate limits |
| MAINTENANCE_MODE | Service is temporarily unavailable |

## Webhook Events (Future Extension)

**POST /webhook/ai-agent/events**

Event types that may be sent to registered webhook endpoints:
- `tool_call.completed` - When an AI-initiated tool call completes
- `tool_call.failed` - When an AI-initiated tool call fails
- `ai_response.generated` - When an AI response is generated