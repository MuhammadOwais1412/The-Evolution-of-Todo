# MCP Server Quickstart Guide

This guide provides instructions for setting up and running the MCP (Model Context Protocol) server for the Todo AI Chatbot.

## Prerequisites

- Python 3.11+
- Poetry package manager
- Access to Neon PostgreSQL database
- Better Auth service for authentication

## Installation

1. Navigate to the backend directory:
   ```bash
   cd Phase-3-todo-ai-chatbot/backend
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Update the `.env` file with your database URL and authentication settings.

## Starting the Server

### Running the MCP Server
```bash
# From backend directory
poetry run python src/mcp/server.py
```

The server will start on localhost:8000/mcp by default and provide the following tools:

1. `add_task` - Create new tasks
2. `list_tasks` - Retrieve user's tasks
3. `update_task` - Modify existing tasks
4. `complete_task` - Mark tasks as complete/incomplete
5. `delete_task` - Remove tasks

## Testing MCP Tools

### Using the Test Suite
```bash
# Run all MCP tests
poetry run pytest tests/mcp/

# Run specific tool tests
poetry run pytest tests/mcp/test_tools/test_add_task.py
```

### Manual Testing Example
```python
import requests

# Example usage of the add_task tool
response = requests.post("http://localhost:8000/mcp/add_task", json={
    "user_id": "some-uuid-here",
    "title": "Test task",
    "description": "Test description"
})

print(response.json())
```

## Development Guidelines

### Adding New MCP Tools
1. Create new tool function in `src/mcp/tools/task_operations.py`
2. Register the tool with the MCP server in `src/mcp/server.py`
3. Write tests in `tests/mcp/test_tools/`
4. Update data models if needed

### Authentication Validation
All MCP tools validate the user_id parameter against the authentication system. Use the provided auth validation utilities in `src/mcp/tools/auth_validation.py`.

### Database Operations
All MCP tools use the established SQLModel patterns with Neon PostgreSQL. Refer to existing patterns in the service layer for consistency.

## Configuration

The server uses configuration from the `.env` file:
- `MCP_SERVER_HOST`: Host address (default: localhost)
- `MCP_SERVER_PORT`: Port number (default: 8000)
- `MCP_SERVER_PATH`: Path for MCP endpoints (default: /mcp)

## Architecture

The MCP server follows a stateless architecture:
- No server-side session state or caching for conversation context
- Conversation context is reconstructed per request from the database
- All data is persisted to the Neon PostgreSQL database
- User isolation is enforced through user_id validation in all operations