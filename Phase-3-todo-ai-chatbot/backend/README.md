# Todo AI Chatbot Backend

FastAPI backend for multi-user todo application with AI chatbot integration, PostgreSQL persistence, and natural language task management.

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- Neon PostgreSQL database
- Google Gemini API key

### Installation

```bash
# Install dependencies with UV
uv sync

# Install development dependencies (optional)
uv sync --extra dev
```

### Configuration

1. Copy `.env.example` to `.env`
2. Update the following environment variables:
   - `DATABASE_URL`: Your Neon PostgreSQL connection string
   - `BETTER_AUTH_SECRET`: JWT secret for authentication
   - `BETTER_AUTH_URL`: Frontend URL for Better Auth
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `GEMINI_MODEL_NAME`: Model name (default: gemini-2.5-flash)

### Running

```bash
# Development with auto-reload
uv run uvicorn src.main:app --reload

# Production
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### Documentation

- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Features

- **Task Management**: Full CRUD operations for todo tasks
- **AI Chatbot**: Natural language interface for managing tasks
- **JWT Authentication**: Secure user authentication with Better Auth
- **PostgreSQL**: Persistent storage with async database operations
- **MCP Tools**: Model Context Protocol integration for AI agents
- **Conversation History**: Track and persist chat conversations
- **Audit Logging**: Comprehensive logging of AI tool calls

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with lifespan
│   ├── db.py                # Database setup
│   ├── config/
│   │   ├── __init__.py      # App settings
│   │   └── ai_config.py     # AI provider configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py          # Task model
│   │   ├── conversation.py  # Chat conversation model
│   │   ├── message.py       # Chat message model
│   │   └── tool_call_log.py # AI tool call audit log
│   ├── schemas/
│   │   └── ai_schemas.py    # AI request/response schemas
│   ├── services/
│   │   ├── task_service.py
│   │   └── conversation_service.py
│   ├── ai/
│   │   ├── agent_service.py        # Main AI agent service
│   │   ├── mcp_adapters.py         # MCP tool adapters
│   │   ├── context_reconstructor.py
│   │   ├── tool_orchestrator.py
│   │   ├── audit_logger.py
│   │   └── confirmation_handler.py
│   ├── mcp/
│   │   ├── server.py        # MCP server
│   │   ├── tools/
│   │   │   ├── task_operations.py
│   │   │   └── auth_validation.py
│   │   └── schemas/
│   │       └── task_schemas.py
│   ├── api/
│   │   ├── deps.py          # JWT, DB dependencies
│   │   ├── tasks.py         # Task endpoints
│   │   └── routes/
│   │       ├── ai_chat.py   # AI chatbot endpoints
│   │       └── chat.py      # Chat UI endpoints
│   ├── exceptions/
│   │   └── ai_exceptions.py
│   └── utils/
│       └── auth_utils.py
├── tests/
├── pyproject.toml
├── .env.example
└── .gitignore
```

## API Endpoints

### Task Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List tasks |
| POST | `/api/{user_id}/tasks` | Create task |
| GET | `/api/{user_id}/tasks/{task_id}` | Get single task |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion |

### AI Chatbot

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat` | Send message to AI chatbot |
| POST | `/api/ai/confirm/{confirmation_id}` | Confirm pending action |
| POST | `/api/ai/reject/{confirmation_id}` | Reject pending action |
| GET | `/api/ai/pending-confirmations` | Get pending confirmations |
| GET | `/api/ai/tool-call-log` | Get AI tool call audit logs |
| GET | `/api/ai/metrics` | Get AI usage metrics |
| GET | `/api/ai/health` | AI service health check |

### Health & Status

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root health check |
| GET | `/health` | Health check endpoint |

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_tasks.py
```

## Database

The application uses PostgreSQL with async SQLAlchemy. Tables are automatically created on startup:

- `tasks`: User todo tasks
- `conversations`: Chat conversation sessions
- `messages`: Individual chat messages
- `tool_call_logs`: Audit log of AI tool executions

Better Auth tables (user, account, session, verification, jwks) should be created separately using the schema in `frontend/better_auth_postgresql_schema.sql`.

## Environment Variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/database

# Authentication
BETTER_AUTH_SECRET=your-jwt-secret
BETTER_AUTH_URL=http://localhost:3000

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL_NAME=gemini-2.5-flash

# MCP Server (optional)
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8000
MCP_SERVER_PATH=/mcp
```

## Development

### Adding New AI Tools

1. Define tool in `src/mcp/tools/`
2. Register in `src/ai/mcp_adapters.py`
3. Add tool definition in `src/ai/tool_definitions.py`

### Code Quality

```bash
# Format code
uv run black src/

# Lint code
uv run ruff check src/

# Type checking
uv run mypy src/
```
