# Quickstart: MCP Server & Tool Layer

## Setup

### Prerequisites
- Python 3.11+
- Poetry (dependency management)
- Access to Neon PostgreSQL database
- Better Auth authentication service

### Installation
```bash
# Navigate to backend directory
cd backend/

# Install dependencies
poetry install

# Set up environment variables
cp .env.example .env
# Configure DATABASE_URL and other required variables
```

### Environment Configuration
```bash
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
AUTH_JWT_SECRET=your_jwt_secret_key
```

## Running the MCP Server

### Starting the Server
```bash
# From backend directory
poetry run python src/mcp/server.py
```

### Server Configuration
The MCP server will start on localhost:8000/mcp by default. The server implements the Model Context Protocol and provides the following tools:

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

### Manual Testing
```python
# Example usage of the add_task tool
import requests

response = requests.post("http://localhost:8000/mcp/add_task", json={
    "user_id": "some-uuid-here",
    "title": "Test task",
    "description": "Test description"
})
```

## Development

### Adding New MCP Tools
1. Create new tool function in `src/mcp/tools/task_operations.py`
2. Register the tool with the MCP server
3. Write tests in `tests/mcp/test_tools/`
4. Update data models if needed

### Authentication Validation
All MCP tools must validate the user_id parameter against the authentication system. Use the provided auth validation utilities in `src/mcp/tools/auth_validation.py`.

### Database Operations
All MCP tools must use the established SQLModel patterns with Neon PostgreSQL. Refer to existing patterns in the backend service layer for consistency.