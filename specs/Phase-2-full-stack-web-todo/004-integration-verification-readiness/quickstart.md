# Quickstart Guide: Phase II - Full-Stack Todo Application

**Created**: 2026-01-10

## Prerequisites
- Node.js 18+ for frontend
- Python 3.9+ for backend
- Neon PostgreSQL database instance
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Configure Environment Variables

#### Backend Configuration (.env)
Create a `.env` file in the backend directory:
```bash
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here"
```

#### Frontend Configuration (.env.local)
Create a `.env.local` file in the frontend directory:
```bash
NEXT_PUBLIC_BETTER_AUTH_URL="http://localhost:3000"
BETTER_AUTH_SECRET="your-super-secret-jwt-key-here"
DATABASE_URL="postgresql://username:password@ep-xxxxxx.us-east-1.aws.neon.tech/dbname?sslmode=require"
BACKEND_API_URL="http://localhost:8000"  # Replace with your backend URL
```

**CRITICAL**: The `BETTER_AUTH_SECRET` must be IDENTICAL in both frontend and backend configurations for JWT validation to work.

### 3. Start the Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
The backend should start on `http://localhost:8000`.

### 4. Start the Frontend
```bash
cd frontend  # or wherever your Next.js app is located
npm install
npm run dev
```
The frontend should start on `http://localhost:3000`.

## Verification Steps

### 1. Check Environment Configuration
- Verify both systems use the same `DATABASE_URL`
- Verify both systems use the same `BETTER_AUTH_SECRET`

### 2. Test Authentication Flow
- Navigate to the frontend
- Sign up or sign in using the authentication UI
- Verify that you receive a JWT token and are properly authenticated

### 3. Test API Communication
- After logging in, try creating a task
- Check that the task appears in the UI
- Verify that the task is persisted in the database

### 4. Test User Isolation
- Log in as one user and create tasks
- Log out and log in as a different user
- Verify that the second user cannot see the first user's tasks

## Common Issues and Solutions

### Issue: JWT Authentication Failure
**Symptoms**: Cannot access backend API after logging in through frontend
**Solution**: Verify that `BETTER_AUTH_SECRET` is identical in both frontend and backend environments

### Issue: Database Connection Problems
**Symptoms**: Cannot create or retrieve tasks
**Solution**: Verify that `DATABASE_URL` is correct and accessible from both systems

### Issue: Cross-Origin Requests Blocked
**Symptoms**: API calls from frontend to backend are blocked
**Solution**: Ensure backend CORS settings allow requests from frontend origin