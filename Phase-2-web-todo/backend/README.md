# Todo Backend

FastAPI backend for multi-user todo application with PostgreSQL persistence.

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- Neon PostgreSQL database

### Installation

```bash
# Install dependencies with UV
uv sync

# Install development dependencies
uv sync --extra dev
```

### Configuration

1. Copy `.env.example` to `.env`
2. Update `DATABASE_URL` with your Neon connection string
3. Set `BETTER_AUTH_SECRET` with your JWT secret

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

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── config.py         # Configuration
│   ├── db.py             # Database setup
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py       # Task SQLModel
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py
│   └── api/
│       ├── __init__.py
│       ├── deps.py       # JWT, DB dependencies
│       └── tasks.py      # Task endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_tasks.py
├── pyproject.toml
├── .env.example
└── .gitignore
```

## Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List tasks |
| POST | `/api/{user_id}/tasks` | Create task |
| GET | `/api/{user_id}/tasks/{task_id}` | Get single task |
| PUT | `/api/{user_id}/tasks/{task_id}` | Update task |
| DELETE | `/api/{user_id}/tasks/{task_id}` | Delete task |
| PATCH | `/api/{user_id}/tasks/{task_id}/complete` | Toggle completion |
