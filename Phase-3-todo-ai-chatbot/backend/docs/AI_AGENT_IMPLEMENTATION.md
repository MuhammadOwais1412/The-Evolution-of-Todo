# AI Agent & Chat Orchestration - Implementation Documentation

## Overview

This document describes the implementation of the AI Agent & Chat Orchestration feature for the Todo application. The AI agent interprets natural language commands and executes appropriate MCP tools to manage tasks.

## Architecture

### Core Components

1. **AIAgentService** (`src/ai/agent_service.py`)
   - Main service for processing natural language commands
   - Integrates with Google Gemini via OpenAI-compatible API
   - Implements retry logic for transient failures
   - Includes input sanitization and response moderation

2. **ContextReconstructor** (`src/ai/context_reconstructor.py`)
   - Reconstructs conversation context from database per request
   - Maintains stateless operation
   - Optimizes context size to prevent model limits

3. **ToolOrchestrator** (`src/ai/tool_orchestrator.py`)
   - Validates user permissions for tool calls
   - Executes MCP tools on behalf of the AI agent
   - Ensures user isolation

4. **AuditLogger** (`src/ai/audit_logger.py`)
   - Logs all AI-initiated tool calls
   - Provides audit trail for compliance
   - Supports log querying and cleanup

5. **ConfirmationHandler** (`src/ai/confirmation_handler.py`)
   - Manages user confirmations for destructive operations
   - Implements expiration for pending confirmations
   - Ensures safety for critical operations

## API Endpoints

### POST /api/ai/chat
Main endpoint for AI chat interactions.

**Request:**
```json
{
  "message": "Add a task to buy groceries",
  "requires_confirmation": true
}
```

**Response:**
```json
{
  "success": true,
  "response": "I've added a task to buy groceries.",
  "tool_calls": [...],
  "requires_confirmation": false,
  "message": "Successfully processed AI command"
}
```

### POST /api/ai/confirm/{confirmation_id}
Confirm a pending destructive operation.

### GET /api/ai/pending-confirmations
Retrieve pending confirmations for the current user.

### POST /api/ai/reject/{confirmation_id}
Reject a pending confirmation.

### GET /api/ai/tool-call-log
Retrieve audit logs of tool calls.

**Query Parameters:**
- `limit`: Number of records (default: 20)
- `offset`: Pagination offset
- `tool_name`: Filter by tool name
- `status`: Filter by status
- `start_date`: Filter by start date
- `end_date`: Filter by end date

### GET /api/ai/health
Health check endpoint for AI service.

### GET /api/ai/metrics
Retrieve AI agent usage metrics.

## Security Features

### Input Sanitization
- Message length validation (max 1000 characters)
- Prompt injection detection
- Harmful pattern filtering

### Content Moderation
- AI response validation
- Harmful content detection
- Response length limiting

### Authentication & Authorization
- JWT-based authentication required for all endpoints
- User isolation enforced at tool execution level
- Rate limiting (10 requests per minute)

## Error Handling

### Retry Logic
- Exponential backoff for transient failures
- Configurable retry attempts (default: 3)
- Intelligent error classification

### Error Types
- `AIProcessingError`: General AI processing failures
- `ToolExecutionError`: Tool execution failures
- `ContextRetrievalError`: Context reconstruction failures
- `UserPermissionError`: Permission violations
- `ConfirmationError`: Confirmation-related errors

## Testing

### Unit Tests
- `tests/ai/test_agent_service.py`: AI agent service tests
- `tests/ai/test_context_reconstructor.py`: Context reconstruction tests
- `tests/ai/test_tool_orchestrator.py`: Tool orchestration tests

### Integration Tests
- `tests/ai/test_ai_chat_endpoint.py`: API endpoint tests

### End-to-End Tests
- `tests/ai/test_e2e_flows.py`: Complete interaction flow tests

### Running Tests
```bash
# Run all tests
pytest

# Run unit tests only
pytest -m "not integration and not e2e"

# Run integration tests
pytest -m integration

# Run with coverage
pytest --cov=src/ai --cov-report=html
```

## Configuration

### Environment Variables
```env
GEMINI_API_KEY=your-api-key
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
```

### AI Model Configuration
Located in `src/config/ai_config.py`:
- Model selection
- Temperature settings
- Token limits
- Timeout configuration

## Deployment

### Prerequisites
1. PostgreSQL database (Neon)
2. Google Gemini API access
3. Python 3.11+
4. Required dependencies installed

### Startup
The AI agent service initializes automatically on application startup via the FastAPI lifespan manager.

### Shutdown
Graceful shutdown is handled automatically, including:
- Closing AI client connections
- Cleaning up pending confirmations
- Flushing audit logs

## Monitoring

### Health Checks
- AI model connection status
- Database connection status
- MCP tool availability

### Metrics
- Total tool calls
- Success/error rates
- Average execution time
- Tool usage breakdown

### Logging
All operations are logged with appropriate levels:
- INFO: Normal operations
- WARNING: Potential issues (e.g., prompt injection attempts)
- ERROR: Failures requiring attention

## Future Enhancements

1. **Caching Layer**: Add Redis for context caching
2. **Advanced NLP**: Improve intent recognition
3. **Multi-turn Conversations**: Better conversation state management
4. **Voice Interface**: Add speech-to-text integration
5. **Analytics Dashboard**: Visualize usage patterns
6. **A/B Testing**: Test different AI models and prompts

## Troubleshooting

### Common Issues

**Issue: AI responses are slow**
- Check network latency to Gemini API
- Review context size (may be too large)
- Check database query performance

**Issue: Tool calls failing**
- Verify MCP tools are properly initialized
- Check user permissions
- Review audit logs for error details

**Issue: Context not maintained**
- Verify database connection
- Check context reconstruction logic
- Review recent tool call logs

## Support

For issues or questions, refer to:
- Project documentation in `specs/`
- Audit logs in database
- Application logs
