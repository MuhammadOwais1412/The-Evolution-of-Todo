"""FastAPI application with CORS middleware and task endpoints."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db import init_db
from src.config import get_settings


settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup/shutdown events."""
    # Startup: Initialize database tables
    await init_db()

    # Initialize AI agent service
    from src.api.routes.ai_chat import _ai_agent_service_instance

    yield

    # Shutdown: Clean up resources
    if _ai_agent_service_instance is not None:
        await _ai_agent_service_instance.shutdown()


# Create FastAPI application
app = FastAPI(
    title="Todo Backend API",
    description="REST API for multi-user todo application with JWT authentication",
    version="0.1.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://the-evolution-of-todo-ai.vercel.app",  # Production Vercel frontend
        "http://localhost:3000",  # Local development
        "http://localhost:3001",  # Alternative local dev port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import and include routers
from src.api.tasks import router as tasks_router
from src.api.routes.ai_chat import router as ai_chat_router
from src.api.routes.chat import router as chat_router

# Include task router
app.include_router(tasks_router)

# Include AI chat router
app.include_router(ai_chat_router)

# Include chat UI router
app.include_router(chat_router)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"status": "healthy", "message": "Todo Backend API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
