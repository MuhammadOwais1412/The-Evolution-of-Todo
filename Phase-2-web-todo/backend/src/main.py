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
    yield
    # Shutdown: Clean up resources if needed
    pass


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
        "https://todo-web-application-rust.vercel.app",  # Production Vercel frontend
        "http://localhost:3000",  # Local development
        "http://localhost:3001",  # Alternative local dev port
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Import and include routers
from src.api.tasks import router as tasks_router

# Include task router
app.include_router(tasks_router)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"status": "healthy", "message": "Todo Backend API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
