# Quickstart Guide: Chat UI & End-to-End Integration

**Feature**: Phase III – Part C: Chat UI & End-to-End Integration
**Date**: 2026-02-12
**Status**: Ready for Implementation

## Overview

This guide provides step-by-step instructions for setting up, running, and testing the integrated chat system. Follow these steps after implementing all tasks from `tasks.md`.

---

## Prerequisites

Before starting, ensure the following are complete and functional:

### Part A: MCP Server (REQUIRED)
- ✅ MCP tools implemented (add_task, list_tasks, update_task, complete_task, delete_task)
- ✅ MCP server running and accessible
- ✅ Tool validation and error handling working

### Part B: AI Agent (REQUIRED)
- ✅ AI Agent service implemented
- ✅ Natural language processing functional
- ✅ Tool orchestration working
- ✅ Context reconstruction from database operational
- ✅ Audit logging enabled

### Infrastructure (REQUIRED)
- ✅ Neon PostgreSQL database accessible
- ✅ Better Auth configured and issuing JWT tokens
- ✅ Python 3.11+ installed
- ✅ Node.js 18+ installed
- ✅ Environment variables configured

---

## Step 1: Database Migration

Add the new conversation and message tables to your database.

### 1.1 Run Migration Script

```bash
# Navigate to backend directory
cd Phase-3-todo-ai-chatbot/backend

# Run Alembic migration
alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Running upgrade 002 -> 003, add conversation and message tables
```

### 1.2 Verify Tables Created

```bash
# Connect to your Neon database
psql $DATABASE_URL

# List tables
\dt

# Expected output should include:
# - conversations
# - messages
```

### 1.3 Verify Indexes

```sql
-- Check indexes on conversations table
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'conversations';

-- Expected indexes:
-- - conversations_pkey (PRIMARY KEY on id)
-- - ix_conversations_user_id (INDEX on user_id)
-- - ix_conversations_updated_at (INDEX on updated_at)

-- Check indexes on messages table
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'messages';

-- Expected indexes:
-- - messages_pkey (PRIMARY KEY on id)
-- - ix_messages_conversation_id (INDEX on conversation_id)
-- - ix_messages_timestamp (INDEX on timestamp)
-- - ix_messages_conversation_timestamp (COMPOSITE INDEX on conversation_id, timestamp)
```

---

## Step 2: Install Dependencies

### 2.1 Backend Dependencies

```bash
cd Phase-3-todo-ai-chatbot/backend

# Install new dependencies (if any were added)
pip install -r requirements.txt

# Verify SQLModel models can be imported
python -c "from src.models.conversation import Conversation; from src.models.message import Message; print('Models imported successfully')"
```

### 2.2 Frontend Dependencies

```bash
cd Phase-3-todo-ai-chatbot/frontend

# Install OpenAI ChatKit
npm install @openai/chatkit

# Install other dependencies
npm install

# Verify installation
npm list @openai/chatkit
```

---

## Step 3: Environment Configuration

### 3.1 Backend Environment Variables

Verify your `.env` file in `backend/` includes:

```env
# Database
DATABASE_URL=postgresql://user:password@host/database

# AI Agent (from Part B)
GEMINI_API_KEY=your-gemini-api-key
OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/

# Better Auth (from Phase II)
AUTH_SECRET=your-auth-secret
JWT_SECRET=your-jwt-secret

# Server
PORT=8000
HOST=0.0.0.0
```

### 3.2 Frontend Environment Variables

Verify your `.env.local` file in `frontend/` includes:

```env
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
NEXT_PUBLIC_AUTH_URL=http://localhost:3000/api/auth
```

---

## Step 4: Start the System

### 4.1 Start Backend Server

```bash
cd Phase-3-todo-ai-chatbot/backend

# Start FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend Health**:
```bash
curl http://localhost:8000/health
# Expected: {"status": "healthy"}
```

### 4.2 Start Frontend Server

```bash
cd Phase-3-todo-ai-chatbot/frontend

# Start Next.js development server
npm run dev
```

**Expected Output**:
```
  ▲ Next.js 16.x.x
  - Local:        http://localhost:3000
  - Ready in 2.5s
```

---

## Step 5: Manual Testing

### 5.1 Test Authentication

1. Open browser to `http://localhost:3000`
2. Navigate to login page
3. Log in with valid credentials
4. Verify JWT token is stored (check browser DevTools > Application > Local Storage)

### 5.2 Test Chat Interface Access

1. After logging in, navigate to `http://localhost:3000/chat`
2. Verify chat interface loads
3. Verify no authentication errors
4. Check browser console for errors (should be none)

### 5.3 Test Message Sending

**Test Case 1: Send First Message (New Conversation)**

1. Type in chat input: "Add a task to buy groceries"
2. Click Send button
3. **Expected**:
   - User message appears immediately (optimistic update)
   - Loading indicator shows
   - AI response appears within 3 seconds
   - Response confirms task was added
   - No errors in console

**Test Case 2: Continue Conversation**

1. Type: "Show me all my tasks"
2. Click Send
3. **Expected**:
   - Message sent to same conversation_id
   - AI lists tasks including the one just added
   - Conversation history maintained

**Test Case 3: Destructive Operation with Confirmation**

1. Type: "Delete the grocery task"
2. Click Send
3. **Expected**:
   - AI asks for confirmation
   - Confirmation prompt appears in UI
4. Confirm deletion
5. **Expected**:
   - Task is deleted
   - AI confirms deletion

### 5.4 Test Conversation Persistence

1. Refresh the page (F5)
2. **Expected**:
   - Chat interface reloads
   - Previous conversation history displays
   - Can continue conversation

3. Log out and log back in
4. Navigate to chat
5. **Expected**:
   - Previous conversation history still visible
   - Can continue from where left off

### 5.5 Test Error Handling

**Test Case 1: Network Error**

1. Stop backend server
2. Try to send a message
3. **Expected**:
   - Error message: "Connection lost. Retrying..."
   - Automatic retry attempts
   - After 3 failed attempts, manual retry button appears

**Test Case 2: Token Expiration**

1. Manually expire JWT token (or wait for expiration)
2. Try to send a message
3. **Expected**:
   - Error message: "Your session has expired. Please log in again."
   - Redirect to login page

**Test Case 3: Rate Limiting**

1. Send 11 messages rapidly (rate limit is 10/minute)
2. **Expected**:
   - 11th message fails
   - Error message: "You are sending messages too quickly. Please wait..."
   - Input disabled temporarily

### 5.6 Test Responsive Design

1. Open browser DevTools
2. Toggle device toolbar (mobile view)
3. **Expected**:
   - Chat interface adapts to mobile viewport
   - Messages remain readable
   - Input field accessible
   - No horizontal scrolling

---

## Step 6: Automated Testing

### 6.1 Backend Tests

```bash
cd Phase-3-todo-ai-chatbot/backend

# Run all tests
pytest

# Run only chat-related tests
pytest tests/test_conversation_service.py tests/test_chat_endpoints.py

# Run with coverage
pytest --cov=src/services/conversation_service --cov=src/api/routes/chat --cov-report=html
```

**Expected Results**:
- All tests pass
- Coverage >80% for new code

### 6.2 Frontend Tests

```bash
cd Phase-3-todo-ai-chatbot/frontend

# Run all tests
npm test

# Run only chat component tests
npm test -- ChatInterface MessageList MessageInput

# Run with coverage
npm test -- --coverage
```

**Expected Results**:
- All tests pass
- No console errors
- Coverage >80% for new components

### 6.3 Integration Tests

```bash
cd Phase-3-todo-ai-chatbot/backend

# Run integration tests
pytest -m integration tests/test_chat_integration.py
```

**Expected Results**:
- End-to-end chat flow works
- AI agent integrates correctly
- Database operations succeed

---

## Step 7: Performance Verification

### 7.1 Response Time Testing

```bash
# Test chat endpoint response time
curl -X POST http://localhost:8000/api/{user_id}/chat \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to test performance"}' \
  -w "\nTime: %{time_total}s\n"
```

**Expected**: Response time <3 seconds

### 7.2 Conversation History Load Time

```bash
# Test history endpoint response time
curl http://localhost:8000/api/{user_id}/conversations/{conversation_id}/messages \
  -H "Authorization: Bearer {jwt_token}" \
  -w "\nTime: %{time_total}s\n"
```

**Expected**: Response time <2 seconds

### 7.3 Concurrent Session Testing

```bash
# Run load test (requires Apache Bench or similar)
ab -n 100 -c 10 -H "Authorization: Bearer {jwt_token}" \
  -p message.json -T application/json \
  http://localhost:8000/api/{user_id}/chat
```

**Expected**: System handles 100 requests with 10 concurrent connections

---

## Troubleshooting

### Issue: Chat endpoint returns 401 Unauthorized

**Symptoms**: All chat requests fail with authentication error

**Solutions**:
1. Verify JWT token is valid: `jwt.io` to decode token
2. Check token expiration time
3. Verify Better Auth is issuing tokens correctly
4. Check Authorization header format: `Bearer {token}`

### Issue: Messages not persisting to database

**Symptoms**: Conversation history empty after page refresh

**Solutions**:
1. Verify database connection: `psql $DATABASE_URL`
2. Check migration ran successfully: `alembic current`
3. Verify tables exist: `\dt` in psql
4. Check backend logs for database errors

### Issue: AI agent not responding

**Symptoms**: Messages sent but no AI response

**Solutions**:
1. Verify Part B (AI Agent) is running
2. Check Gemini API key is valid
3. Review backend logs for AI processing errors
4. Test AI agent endpoint directly: `POST /api/ai/chat`

### Issue: Chat UI not loading

**Symptoms**: Blank page or component errors

**Solutions**:
1. Check browser console for JavaScript errors
2. Verify OpenAI ChatKit installed: `npm list @openai/chatkit`
3. Check Next.js build: `npm run build`
4. Verify API URL in environment variables

### Issue: Slow response times

**Symptoms**: Chat responses take >5 seconds

**Solutions**:
1. Check database query performance: `EXPLAIN ANALYZE` on queries
2. Verify indexes exist on conversation and message tables
3. Check AI agent processing time (Part B performance)
4. Monitor network latency to Gemini API

---

## Verification Checklist

Before considering the feature complete, verify:

### Functionality
- [ ] Users can log in and access chat interface
- [ ] Users can send messages and receive AI responses
- [ ] Conversations persist across page refreshes
- [ ] Conversation history loads correctly
- [ ] User isolation enforced (cannot access other users' chats)
- [ ] Authentication errors handled gracefully
- [ ] Destructive operations require confirmation

### Performance
- [ ] Chat endpoint responds in <3 seconds (95th percentile)
- [ ] History endpoint responds in <2 seconds
- [ ] System supports 100 concurrent sessions
- [ ] Database queries complete in <500ms

### User Experience
- [ ] Chat interface responsive on mobile and desktop
- [ ] Loading indicators display during processing
- [ ] Error messages clear and actionable
- [ ] Message timestamps display correctly
- [ ] Auto-scroll to latest message works
- [ ] Message input supports multi-line text

### Security
- [ ] JWT tokens validated on every request
- [ ] User_id in URL matches authenticated user
- [ ] No unauthorized access to other users' data
- [ ] Input sanitization prevents injection attacks
- [ ] Error messages don't leak sensitive information

---

## Next Steps

After successful verification:

1. **Code Review**: Have another developer review the implementation
2. **User Testing**: Get feedback from real users
3. **Performance Monitoring**: Set up monitoring for response times and errors
4. **Documentation**: Update user-facing documentation
5. **Deployment**: Deploy to staging environment for further testing

---

## Support

For issues or questions:
- Review implementation documentation in `specs/Phase-III-todo-ai-chatbot/Part-C-chat-ui-integration/`
- Check backend logs: `tail -f backend/logs/app.log`
- Check frontend console: Browser DevTools > Console
- Review database logs: Check Neon dashboard
- Test AI agent directly: Use Part B testing procedures
