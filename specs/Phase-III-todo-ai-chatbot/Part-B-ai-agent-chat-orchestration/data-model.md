# Data Model: AI Agent & Chat Orchestration

## Overview
This document defines the data structures needed for the AI agent and chat orchestration system that operates through MCP tools with stateless architecture.

## Entity Definitions

### AISessionContext
Stores conversation context for AI agent interactions (reconstructed per request, not stored server-side)

```
Table: ai_session_context (Virtual - represented in application logic)

Fields:
- user_id: UUID (Foreign key to users table)
- messages: JSON (Array of conversation messages)
- created_at: DateTime (Timestamp of initial request)
- last_interaction_at: DateTime (Timestamp of last interaction)
- metadata: JSON (Additional context information)

Validation:
- user_id must be a valid UUID
- messages array must not exceed MAX_MESSAGE_HISTORY_SIZE (e.g., 50 messages)
- created_at must be in the past
- last_interaction_at must be >= created_at
```

### ToolCallLog
Records all tool calls made by the AI agent for audit and tracking purposes

```
Table: tool_call_logs

Fields:
- id: UUID (Primary key, auto-generated)
- user_id: UUID (Foreign key to users table)
- session_id: UUID (Identifier for the conversation session)
- tool_name: String (Name of the MCP tool called: add_task, list_tasks, update_task, complete_task, delete_task)
- tool_params: JSON (Parameters passed to the tool)
- result: JSON (Result returned from the tool)
- status: String (Enum: 'success', 'error', 'pending')
- error_details: JSON (Optional error information if status is 'error')
- timestamp: DateTime (When the tool was called)
- ai_confidence: Float (Optional confidence score from AI agent)

Relationships:
- Belongs to user (via user_id)

Indexes:
- idx_tool_call_logs_user_timestamp (user_id, timestamp DESC) - for quick retrieval of user's recent activity
- idx_tool_call_logs_tool_name (tool_name) - for analyzing tool usage
- idx_tool_call_logs_session_id (session_id) - for session-based analysis

Validation:
- id must be a valid UUID
- user_id must reference an existing user
- tool_name must be one of the allowed MCP tools
- timestamp must be in the past or present
- status must be one of 'success', 'error', 'pending'
```

## Relationship Diagram

```
[users] 1 ←→ * [tool_call_logs]
```

## State Transitions

### ToolCallLog Status Transitions
```
pending → success (on successful tool execution)
pending → error (on tool execution failure)
```

## Constraints

### Data Integrity
1. All foreign key references must exist
2. Tool names must match the 5 MCP tools from Part A
3. User permissions must be validated before any tool call
4. Audit logs must be immutable once created

### Business Rules
1. Each AI agent interaction may result in 0 or more tool calls
2. All tool calls must be associated with a valid user
3. Conversation history must be retrieved from existing task data, not stored separately
4. Audit logs must be created synchronously with tool calls

## Indexing Strategy

### Performance Considerations
- ToolCallLog table should be indexed on (user_id, timestamp) for efficient retrieval of user's recent activity
- ToolCallLog should have indexes on tool_name for usage analytics
- Consider partitioning ToolCallLog by date for large-scale deployments

## Access Patterns

### Query Examples
```
-- Get user's recent tool calls
SELECT * FROM tool_call_logs
WHERE user_id = ?
ORDER BY timestamp DESC
LIMIT 20;

-- Count tool usage by type
SELECT tool_name, COUNT(*) as usage_count
FROM tool_call_logs
WHERE timestamp > ?
GROUP BY tool_name;

-- Find failed operations for monitoring
SELECT * FROM tool_call_logs
WHERE status = 'error'
ORDER BY timestamp DESC;
```

## Size Estimation

### Storage Requirements (approximate)
- ToolCallLog: ~1KB per entry (including metadata)
- With 1000 daily active users and 5 tool calls per user: ~5MB/day
- Monthly storage requirement: ~150MB
- Yearly storage requirement: ~1.8GB

## Privacy & Security

### Data Protection
- Tool parameters may contain user data; encrypt at rest if required
- PII in tool parameters should be handled according to privacy regulations
- Audit logs should be protected with appropriate access controls
- Log retention policies should comply with legal requirements

### Access Control
- Users can only access their own ToolCallLog entries
- Admins can access all ToolCallLog entries for operational purposes
- Audit trail should be tamper-evident