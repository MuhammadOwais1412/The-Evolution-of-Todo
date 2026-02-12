# Chat UI & End-to-End Integration

**Phase III - Part C: Chat UI Integration**

A conversational interface for todo management that integrates with the AI Agent (Part B) to provide natural language task management through an authenticated chat interface.

## Overview

This feature adds a chat-based UI that allows users to manage their todos through natural language conversations. Users can create, view, update, and complete tasks by simply chatting with an AI assistant.

### Key Features

- 🔐 **JWT Authentication** - Secure access with Better Auth integration
- 💬 **Natural Language Processing** - Manage tasks through conversational commands
- 💾 **Conversation Persistence** - Chat history saved and synced across devices
- ⚡ **Optimistic UI Updates** - Immediate feedback with automatic rollback on errors
- 🔄 **Automatic Retry** - Exponential backoff for transient network errors
- 📱 **Responsive Design** - Works on desktop and mobile devices
- ⌨️ **Multi-line Support** - Shift+Enter for new lines, Enter to send

## Architecture

### Backend (FastAPI + SQLModel)

```
backend/src/
├── models/
│   ├── conversation.py      # Conversation model
│   └── message.py           # Message model with MessageRole enum
├── services/
│   └── conversation_service.py  # CRUD operations for conversations
├── schemas/
│   └── chat_schemas.py      # Request/response schemas
└── api/routes/
    └── chat.py              # Chat endpoints
```

**Endpoints:**
- `POST /api/{user_id}/chat` - Send message and receive AI response
- `GET /api/{user_id}/conversations/{conversation_id}/messages` - Get conversation history

### Frontend (Next.js + React + TypeScript)

```
frontend/src/
├── app/chat/
│   └── page.tsx             # Chat page route
├── components/
│   ├── AuthGuard.tsx        # Authentication protection
│   ├── ChatInterface.tsx    # Main chat container
│   ├── MessageList.tsx      # Message display with auto-scroll
│   └── MessageInput.tsx     # Input with validation
├── hooks/
│   └── useChat.ts           # Chat state management
└── services/
    ├── apiClient.ts         # Axios client with JWT interceptor
    └── chatService.ts       # Chat API client with retry logic
```

## Setup

### Prerequisites

- **Part A (MCP Server)**: Must be running and accessible
- **Part B (AI Agent)**: Must be configured and operational
- **Better Auth**: Configured and issuing JWT tokens
- **Neon PostgreSQL**: Database accessible
- **Python 3.11+**: For backend
- **Node.js 18+**: For frontend

### Installation

#### Backend

```bash
cd Phase-3-todo-ai-chatbot/backend

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Verify models can be imported
python -c "from src.models.conversation import Conversation; from src.models.message import Message; print('✓ Models imported successfully')"
```

#### Frontend

```bash
cd Phase-3-todo-ai-chatbot/frontend

# Install dependencies
npm install

# Verify build
npm run build
```

### Environment Variables

#### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@host/database
GEMINI_API_KEY=your-gemini-api-key
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
AUTH_SECRET=your-auth-secret
JWT_SECRET=your-jwt-secret
PORT=8000
HOST=0.0.0.0
```

#### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:3000/api/auth
```

## Running the Application

### Start Backend

```bash
cd Phase-3-todo-ai-chatbot/backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

**Verify health:**
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

### Start Frontend

```bash
cd Phase-3-todo-ai-chatbot/frontend
npm run dev
```

**Expected output:**
```
▲ Next.js 15.x.x
- Local:        http://localhost:3000
- Ready in 2.5s
```

### Access Chat Interface

1. Navigate to `http://localhost:3000`
2. Log in with valid credentials
3. Navigate to `http://localhost:3000/chat`
4. Start chatting with the AI assistant

## Usage Examples

### Creating Tasks

```
User: Add a task to buy groceries
AI: I've added "Buy groceries" to your task list.

User: Create a task to finish the report by Friday
AI: I've created a task "Finish the report" with a deadline of Friday.
```

### Viewing Tasks

```
User: Show me all my tasks
AI: Here are your tasks:
1. Buy groceries
2. Finish the report (due Friday)
```

### Updating Tasks

```
User: Mark the first task as complete
AI: I've marked "Buy groceries" as complete.

User: Change the deadline for the report to Monday
AI: I've updated the deadline for "Finish the report" to Monday.
```

### Deleting Tasks

```
User: Delete the grocery task
AI: Are you sure you want to delete "Buy groceries"?

User: Yes, delete it
AI: I've deleted "Buy groceries" from your task list.
```

## Database Schema

### Conversations Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | VARCHAR(255) | Foreign key to users |
| created_at | TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

**Indexes:**
- `ix_conversations_user_id` on `user_id`
- `ix_conversations_updated_at` on `updated_at`

### Messages Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| conversation_id | UUID | Foreign key to conversations |
| role | ENUM | 'user' or 'assistant' |
| content | TEXT | Message content (max 10000 chars) |
| timestamp | TIMESTAMP | Message timestamp |
| metadata | JSON | Optional metadata (tool calls, etc.) |

**Indexes:**
- `ix_messages_conversation_id` on `conversation_id`
- `ix_messages_timestamp` on `timestamp`
- `ix_messages_conversation_timestamp` on `(conversation_id, timestamp)`

## Testing

### Manual Testing Checklist

- [ ] **Authentication**
  - [ ] Unauthenticated users redirected to login
  - [ ] Authenticated users can access /chat
  - [ ] Expired tokens trigger re-authentication

- [ ] **Message Sending**
  - [ ] User messages appear immediately (optimistic update)
  - [ ] AI responses appear within 3 seconds
  - [ ] Loading indicator shows during processing
  - [ ] Character limit enforced (1000 chars)

- [ ] **Conversation Persistence**
  - [ ] Messages persist after page refresh
  - [ ] Conversation history loads on mount
  - [ ] Auto-scroll to latest message works

- [ ] **Error Handling**
  - [ ] Network errors show user-friendly messages
  - [ ] Automatic retry for transient errors
  - [ ] Error banner dismissible
  - [ ] Invalid input shows validation error

- [ ] **Multi-device Sync**
  - [ ] Conversation accessible from different browsers
  - [ ] History syncs across devices

### Automated Testing

```bash
# Backend tests (when implemented)
cd Phase-3-todo-ai-chatbot/backend
pytest tests/test_conversation_service.py
pytest tests/test_chat_endpoints.py

# Frontend tests (when implemented)
cd Phase-3-todo-ai-chatbot/frontend
npm test
```

## Troubleshooting

### Chat endpoint returns 401 Unauthorized

**Cause:** JWT token missing or invalid

**Solution:**
1. Verify token in localStorage: `localStorage.getItem('auth_token')`
2. Check token expiration at jwt.io
3. Log out and log back in
4. Verify Better Auth is issuing tokens correctly

### Messages not persisting

**Cause:** Database connection issue or tables not created

**Solution:**
1. Check database connection: `psql $DATABASE_URL`
2. Verify tables exist: `\dt` (should show conversations and messages)
3. Check backend logs for database errors
4. Restart backend to trigger table creation

### AI not responding

**Cause:** Part B (AI Agent) not running or misconfigured

**Solution:**
1. Verify Part B is running
2. Check Gemini API key is valid
3. Review backend logs for AI processing errors
4. Test AI agent endpoint directly

### Chat UI not loading

**Cause:** Frontend build errors or missing dependencies

**Solution:**
1. Check browser console for errors
2. Verify all dependencies installed: `npm install`
3. Rebuild frontend: `npm run build`
4. Check API URL in .env.local

## Performance Considerations

- **Response Time Target:** <3 seconds (95th percentile)
- **History Load Target:** <2 seconds
- **Concurrent Sessions:** Supports 100+ concurrent users
- **Database Queries:** <500ms with proper indexing

## Security

- **Authentication:** JWT tokens validated on every request
- **Authorization:** User ID in URL must match authenticated user
- **User Isolation:** Users can only access their own conversations
- **Input Validation:** Message length limited to 1000 characters
- **Error Messages:** No sensitive information leaked in errors

## Known Limitations

- **Rate Limiting:** Not yet implemented (planned: 10 messages/minute)
- **Confirmation Dialogs:** Destructive operations need explicit confirmation UI
- **Input Sanitization:** XSS prevention needs additional middleware
- **Structured Logging:** Chat operations logging not yet implemented

## Future Enhancements

- [ ] Rate limiting middleware
- [ ] Confirmation dialogs for destructive operations
- [ ] Input sanitization for XSS prevention
- [ ] Structured logging for monitoring
- [ ] Conversation search functionality
- [ ] Export conversation history
- [ ] Voice input support
- [ ] File attachment support

## Documentation

- **Specification:** `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/spec.md`
- **Implementation Plan:** `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/plan.md`
- **Task List:** `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/tasks.md`
- **Research:** `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/research.md`
- **Data Model:** `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/data-model.md`
- **Quickstart:** `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/quickstart.md`

## Support

For issues or questions:
- Review implementation documentation in `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/`
- Check backend logs: `tail -f backend/logs/app.log`
- Check frontend console: Browser DevTools > Console
- Review database logs: Check Neon dashboard
- Test AI agent directly: Use Part B testing procedures

## License

MIT
