# Phase III: Todo AI Chatbot

An intelligent todo management application with natural language processing capabilities, allowing users to manage their tasks through conversational AI.

## Overview

Phase III extends the todo application with AI-powered features:

- **Natural Language Task Management**: Create, update, and manage tasks using conversational commands
- **AI Agent Integration**: Powered by Google Gemini for intelligent task understanding
- **MCP (Model Context Protocol)**: Structured tool calling for reliable AI-to-backend communication
- **Conversation Persistence**: Chat history saved and synced across sessions
- **Multi-User Support**: Secure JWT authentication with Better Auth
- **Real-time Updates**: Optimistic UI with automatic error handling

## Architecture

### Backend (FastAPI + SQLModel + PostgreSQL)

```
backend/
├── src/
│   ├── main.py                    # FastAPI application
│   ├── db.py                      # Database configuration
│   ├── config/
│   │   ├── __init__.py           # App settings
│   │   └── ai_config.py          # AI provider configuration
│   ├── models/
│   │   ├── task.py               # Task model
│   │   ├── conversation.py       # Chat conversation model
│   │   ├── message.py            # Chat message model
│   │   └── tool_call_log.py      # AI tool call audit log
│   ├── ai/
│   │   ├── agent_service.py      # Main AI agent service
│   │   ├── mcp_adapters.py       # MCP tool adapters
│   │   ├── audit_logger.py       # Tool call logging
│   │   └── confirmation_handler.py
│   ├── mcp/
│   │   ├── server.py             # MCP server
│   │   └── tools/
│   │       └── task_operations.py
│   └── api/
│       ├── tasks.py              # Task CRUD endpoints
│       └── routes/
│           ├── ai_chat.py        # AI chatbot endpoints
│           └── chat.py           # Chat UI endpoints
```

### Frontend (Next.js + React + TypeScript)

```
frontend/
├── src/
│   ├── app/
│   │   ├── chat/                 # Chat interface page
│   │   └── tasks/                # Task management page
│   ├── components/
│   │   ├── ChatInterface.tsx     # Main chat UI
│   │   ├── MessageList.tsx       # Message display
│   │   └── MessageInput.tsx      # Input component
│   ├── hooks/
│   │   └── useChat.ts            # Chat state management
│   └── services/
│       ├── apiClient.ts          # Axios client with JWT
│       └── chatService.ts        # Chat API client
```

## Prerequisites

- **Python 3.11+**: For backend
- **Node.js 18+**: For frontend
- **UV Package Manager**: For Python dependency management
- **PostgreSQL**: Neon or local instance
- **Google Gemini API Key**: For AI capabilities

## Quick Start

### 1. Backend Setup

```bash
cd Phase-3-todo-ai-chatbot/backend

# Install dependencies with UV
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your database URL, Gemini API key, etc.

# Run the backend
uv run uvicorn src.main:app --reload
```

**Backend will be available at:** `http://localhost:8000`

### 2. Frontend Setup

```bash
cd Phase-3-todo-ai-chatbot/frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your API URL

# Run the frontend
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

### 3. Database Setup

The backend automatically creates tables on startup. For Better Auth tables, run:

```bash
psql $DATABASE_URL < frontend/better_auth_postgresql_schema.sql
```

## Environment Configuration

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host/database

# Authentication
BETTER_AUTH_SECRET=your-jwt-secret
BETTER_AUTH_URL=http://localhost:3000

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL_NAME=gemini-2.5-flash

# Server
API_HOST=localhost
API_PORT=8000
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:3000/api/auth
```

## Features

### Task Management
- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Filter and search tasks
- Priority levels and due dates

### AI Chatbot
- Natural language task creation
- Conversational task updates
- Smart task queries
- Context-aware responses
- Confirmation for destructive actions

### Authentication & Security
- JWT-based authentication
- Secure session management
- User isolation
- Input validation

### Conversation History
- Persistent chat history
- Multi-device sync
- Message timestamps
- User/assistant role tracking

## API Endpoints

### Task Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{task_id}` | Get task details |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion |

### AI Chatbot

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/chat` | Send message to AI |
| POST | `/api/ai/confirm/{id}` | Confirm pending action |
| GET | `/api/ai/pending-confirmations` | Get pending confirmations |
| GET | `/api/ai/tool-call-log` | Get audit logs |
| GET | `/api/ai/metrics` | Get usage metrics |
| GET | `/api/ai/health` | Health check |

### Chat History

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/{user_id}/chat` | Send message |
| GET | `/api/{user_id}/conversations/{id}/messages` | Get history |

## Usage Examples

### Creating Tasks via Chat

```
User: Add a task to buy groceries tomorrow
AI: I've created a task "Buy groceries" with a due date of tomorrow.

User: Create a high priority task to finish the report
AI: I've added "Finish the report" as a high priority task.
```

### Viewing Tasks

```
User: Show me all my tasks
AI: Here are your tasks:
1. Buy groceries (due tomorrow)
2. Finish the report (high priority)
3. Call dentist

User: What tasks are due this week?
AI: You have 2 tasks due this week:
1. Buy groceries (due tomorrow)
2. Submit timesheet (due Friday)
```

### Updating Tasks

```
User: Mark the grocery task as complete
AI: I've marked "Buy groceries" as complete.

User: Change the report deadline to next Monday
AI: I've updated "Finish the report" with a deadline of next Monday.
```

## Development

### Backend Development

```bash
cd Phase-3-todo-ai-chatbot/backend

# Install dev dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Format code
uv run black src/

# Type checking
uv run mypy src/
```

### Frontend Development

```bash
cd Phase-3-todo-ai-chatbot/frontend

# Run development server
npm run dev

# Build for production
npm run build

# Run tests
npm test

# Lint code
npm run lint
```

## Troubleshooting

### Backend won't start

**Issue:** Import errors or module not found

**Solution:**
```bash
cd Phase-3-todo-ai-chatbot/backend
uv sync  # Reinstall dependencies
```

### Database connection errors

**Issue:** `could not connect to server`

**Solution:**
1. Verify DATABASE_URL in .env
2. Check PostgreSQL is running
3. Ensure database exists
4. Test connection: `psql $DATABASE_URL`

### AI not responding

**Issue:** Chat messages timeout or error

**Solution:**
1. Verify GEMINI_API_KEY is valid
2. Check API quota/limits
3. Review backend logs for errors
4. Test Gemini API directly

### Authentication errors

**Issue:** 401 Unauthorized responses

**Solution:**
1. Verify Better Auth is configured
2. Check JWT token in browser localStorage
3. Ensure BETTER_AUTH_SECRET matches frontend
4. Log out and log back in

## Testing

### Manual Testing Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads successfully
- [ ] User can log in
- [ ] Tasks can be created via UI
- [ ] Tasks can be created via chat
- [ ] Chat history persists
- [ ] AI responds within 3 seconds
- [ ] Error messages are user-friendly

### Automated Tests

```bash
# Backend tests
cd Phase-3-todo-ai-chatbot/backend
uv run pytest tests/

# Frontend tests
cd Phase-3-todo-ai-chatbot/frontend
npm test
```

## Performance

- **AI Response Time:** <3 seconds (95th percentile)
- **Task Operations:** <500ms
- **Chat History Load:** <2 seconds
- **Concurrent Users:** Supports 100+ users

## Security

- JWT authentication on all endpoints
- User isolation (users can only access their own data)
- Input validation and sanitization
- SQL injection prevention via SQLModel
- XSS protection in frontend
- Secure password hashing (Better Auth)

## Documentation

- **Backend README:** `backend/README.md`
- **API Documentation:** `http://localhost:8000/docs` (when running)
- **Specifications:** `specs/Phase-III-todo-ai-chatbot/`

## Known Limitations

- Rate limiting not yet implemented
- Voice input not supported
- File attachments not supported
- Conversation search not available

## Future Enhancements

- [ ] Rate limiting (10 messages/minute)
- [ ] Voice input support
- [ ] File attachment handling
- [ ] Conversation search
- [ ] Export chat history
- [ ] Multi-language support
- [ ] Offline mode

## Support

For issues or questions:
1. Check backend logs: `tail -f backend/logs/app.log`
2. Check browser console for frontend errors
3. Review database logs in Neon dashboard
4. Test API endpoints directly with curl or Postman

## License

MIT
