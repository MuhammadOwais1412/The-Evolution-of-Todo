# Quickstart Guide: AI Agent & Chat Orchestration

## Overview
This guide explains how to set up and run the AI agent for todo management that operates through MCP tools with stateless architecture.

## Prerequisites
- Python 3.11+
- Poetry or uv for dependency management
- Access to Google Gemini API via OpenAI-compatible endpoint
- Existing Phase III Part A MCP tools running
- Better Auth authentication system
- Neon PostgreSQL database

## Environment Setup
```bash
# Navigate to backend directory
cd Phase-3-todo-ai-chatbot/backend

# Install dependencies
uv pip install openai google-generativeai python-dotenv

# Set up environment variables in .env
GEMINI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://your-gemini-proxy-url.com/v1  # OpenAI-compatible endpoint for Gemini
```

## Core Components

### 1. AI Agent Service
Located in `src/ai/agent_service.py`, this is the main component that:
- Receives natural language input from users
- Maps user intent to appropriate MCP tools
- Maintains conversation context by fetching from database
- Logs all tool calls for audit trail

### 2. MCP Tool Orchestrator
Located in `src/ai/tool_orchestrator.py`, this component:
- Validates user permissions for each tool call
- Calls the appropriate MCP tool from Part A
- Ensures all operations pass through the MCP layer
- Returns results back to the AI agent

### 3. Context Reconstruction Module
Located in `src/ai/context_reconstructor.py`, this module:
- Fetches user's conversation history from database
- Builds the context needed for the AI agent
- Maintains stateless operation without server-side storage

### 4. Audit Logger
Located in `src/ai/audit_logger.py`, this service:
- Logs all tool calls made by the AI agent
- Stores metadata about each operation
- Provides tamper-evident logs for audit trail

## API Endpoint
The AI agent is accessible via:
```
POST /api/ai/chat
Authentication: Bearer token (JWT from Better Auth)
Content-Type: application/json

Request:
{
  "user_id": "uuid-string",
  "message": "natural language command"
}

Response:
{
  "status": "success|error",
  "response": "ai-generated response to user",
  "tool_calls": [...],
  "requires_confirmation": boolean
}
```

## Implementation Notes
- The AI agent operates statelessly; no conversation state is stored on the server
- All operations must go through MCP tools; no direct database access
- Every tool call is logged for audit purposes
- User isolation is maintained through user_id validation
- Google Gemini is accessed via OpenAI-compatible API endpoint