"""Task SQLModel entity definition."""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task entity representing a todo item owned by a user."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=5000)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "user_id": "auth0|12345",
                "created_at": "2026-01-01T12:00:00Z",
                "updated_at": "2026-01-01T12:00:00Z"
            }
        }
