# Quickstart Guide: Backend Foundation

**Feature**: 002-backend-foundation | **Date**: 2026-01-01
**Purpose**: Developer onboarding for backend API setup and testing.

## Prerequisites

- Python 3.11+ installed
- Neon PostgreSQL account (free tier available)
- Better Auth secret (obtain from authentication system)
- Git (for cloning repository)

## Step 1: Set Up Neon PostgreSQL Database

1. **Create Neon Account**:
   - Visit https://neon.tech and sign up for free
   - Create a new project: "todo-backend"
   - Copy the **Connection String** (format: `postgresql://user:password@host/database`)

2. **Create Database Schema**:
   ```sql
   CREATE TABLE tasks (
       id SERIAL PRIMARY KEY,
       title VARCHAR(200) NOT NULL,
       description TEXT,
       completed BOOLEAN DEFAULT FALSE,
       user_id VARCHAR(255) NOT NULL,
       created_at TIMESTAMP DEFAULT NOW(),
       updated_at TIMESTAMP DEFAULT NOW()
   );

   CREATE INDEX idx_tasks_user_id ON tasks(user_id);
   CREATE INDEX idx_tasks_completed ON tasks(completed);
   ```
   - Run this in Neon's SQL Editor or via psql

3. **Save Connection String**:
   - You'll need this for `.env` configuration

## Step 2: Configure Environment Variables

1. **Create `.env` file** in repository root:
   ```bash
   # Database connection
   DATABASE_URL=postgresql+asyncpg://user:password@host/database

   # Better Auth JWT secret
   BETTER_AUTH_SECRET=your-secret-key-here

   # API configuration
   API_HOST=localhost
   API_PORT=8000
   ```

2. **Replace placeholders**:
   - `DATABASE_URL`: Paste Neon connection string (add `+asyncpg` for async driver)
   - `BETTER_AUTH_SECRET`: Get from your Better Auth configuration

3. **Never commit `.env`**:
   - Ensure `.env` is in `.gitignore`
   - Provide `.env.example` in repository

## Step 3: Install Dependencies

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlmodel psycopg2-binary asyncpg pydantic python-jose[cryptography] python-multipart httpx pytest pytest-asyncio
   ```

4. **Verify installation**:
   ```bash
   pip list | grep -E "fastapi|sqlmodel|pydantic"
   ```

## Step 4: Run the API Server

1. **Start the server**:
   ```bash
   uvicorn src.main:app --reload --host localhost --port 8000
   ```

2. **Verify startup**:
   - Visit http://localhost:8000/docs (FastAPI auto-generated docs)
   - Visit http://localhost:8000/redoc (alternative documentation)
   - You should see the API endpoints listed

3. **Check health** (if implemented):
   ```bash
   curl http://localhost:8000/health
   ```

## Step 5: Obtain JWT Token

**Option A: Use Better Auth UI** (if available):
1. Navigate to Better Auth login page
2. Sign in with email/password
3. Use browser DevTools to copy JWT from localStorage or cookies

**Option B: Generate Test Token** (for development only):
```python
from jose import jwt
import time

secret = "your-better-auth-secret"
user_id = "test-user-123"
payload = {
    "sub": user_id,
    "exp": time.time() + 3600  # 1 hour
}
token = jwt.encode(payload, secret, algorithm="HS256")
print(token)
```

**Save token as environment variable**:
```bash
export JWT_TOKEN="your-jwt-token-here"
```

## Step 6: Test API Endpoints

### Test 1: Create a Task
```bash
curl -X POST http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task from quickstart",
    "description": "This is a test task"
  }'
```

**Expected Response**:
```json
{
  "id": 1,
  "title": "Test task from quickstart",
  "description": "This is a test task",
  "completed": false,
  "user_id": "test-user-123",
  "created_at": "2026-01-01T12:00:00Z",
  "updated_at": "2026-01-01T12:00:00Z"
}
```

### Test 2: List All Tasks
```bash
curl -X GET http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response**:
```json
[
  {
    "id": 1,
    "title": "Test task from quickstart",
    "description": "This is a test task",
    "completed": false,
    "user_id": "test-user-123",
    "created_at": "2026-01-01T12:00:00Z",
    "updated_at": "2026-01-01T12:00:00Z"
  }
]
```

### Test 3: Get Single Task
```bash
curl -X GET http://localhost:8000/api/test-user-123/tasks/1 \
  -H "Authorization: Bearer $JWT_TOKEN"
```

### Test 4: Toggle Completion
```bash
curl -X PATCH http://localhost:8000/api/test-user-123/tasks/1/complete \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response**: `completed` should be `true`

### Test 5: Update Task
```bash
curl -X PUT http://localhost:8000/api/test-user-123/tasks/1 \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated task title",
    "description": "Updated description",
    "completed": true
  }'
```

### Test 6: Delete Task
```bash
curl -X DELETE http://localhost:8000/api/test-user-123/tasks/1 \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected Response**: HTTP 204 (no body)

### Test 7: Verify User Isolation
```bash
# Try to access user "A"'s tasks with user "B"'s token
curl -X GET http://localhost:8000/api/user-A/tasks \
  -H "Authorization: Bearer $USER_B_JWT_TOKEN"
```

**Expected Response**:
```json
{
  "error": "unauthorized",
  "message": "User ID mismatch"
}
```

### Test 8: Validate Error Handling

**Missing Title**:
```bash
curl -X POST http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response** (HTTP 422):
```json
{
  "error": "validation_error",
  "message": "Title is required",
  "details": {
    "field": "title"
  }
}
```

**Invalid JWT**:
```bash
curl -X GET http://localhost:8000/api/test-user-123/tasks \
  -H "Authorization: Bearer invalid-token"
```

**Expected Response** (HTTP 401):
```json
{
  "error": "unauthorized",
  "message": "Invalid or expired JWT token"
}
```

## Step 7: Run Tests

1. **Install test dependencies** (if not already installed):
   ```bash
   pip install pytest pytest-asyncio httpx
   ```

2. **Run all tests**:
   ```bash
   pytest tests/
   ```

3. **Run with coverage**:
   ```bash
   pytest --cov=src tests/
   ```

4. **Run specific test file**:
   ```bash
   pytest tests/test_tasks.py -v
   ```

## Step 8: Verify Database Persistence

1. **Check Neon Dashboard**:
   - Navigate to your Neon project
   - Use the SQL Editor to run:
   ```sql
   SELECT * FROM tasks ORDER BY created_at DESC LIMIT 10;
   ```

2. **Verify isolation**:
   ```sql
   -- Check tasks for a specific user
   SELECT * FROM tasks WHERE user_id = 'test-user-123';
   ```

## Troubleshooting

### Issue: Connection refused
**Solution**: Ensure Neon connection string uses `+asyncpg` driver and network allows outbound connections.

### Issue: JWT verification fails
**Solution**: Check that `BETTER_AUTH_SECRET` matches the secret used to generate the token.

### Issue: 422 Validation errors
**Solution**: Verify request body matches OpenAPI schema (e.g., `title` must be 1-200 characters).

### Issue: Tasks not persisting
**Solution**: Check Neon dashboard for connection status and ensure `await session.commit()` is called.

### Issue: User isolation not working
**Solution**: Verify JWT `sub` claim matches `user_id` in URL and `verify_jwt()` is implemented correctly.

## Next Steps

1. **Review API Documentation**: http://localhost:8000/docs
2. **Explore Test Files**: `backend/tests/test_tasks.py`
3. **Read Implementation Plan**: `specs/Phase-2-full-stack-web-todo/002-backend-foundation/plan.md`
4. **Check Data Model**: `specs/Phase-2-full-stack-web-todo/002-backend-foundation/data-model.md`

## Support

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLModel Docs**: https://sqlmodel.tiangolo.com/
- **Neon Docs**: https://neon.tech/docs
- **Project Issues**: Use repository's issue tracker

## Success Criteria

You're successfully set up when:
- ✅ API server starts without errors
- ✅ All test endpoints return expected responses
- ✅ Tasks persist in Neon database
- ✅ JWT authentication works
- ✅ User isolation prevents cross-user access
- ✅ All manual tests pass (Test 1-8)
