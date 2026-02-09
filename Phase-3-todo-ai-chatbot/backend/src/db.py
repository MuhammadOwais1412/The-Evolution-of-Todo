"""Database engine and session setup."""
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

from src.config import get_settings
# Import all models to register them with SQLModel metadata
from src.models import *  # noqa: F401, F403

settings = get_settings()

# Sanitize the database URL for asyncpg compatibility
raw_url = settings.database_url
parsed = urlparse(raw_url)
query = parse_qs(parsed.query)

# Remove asyncpg-incompatible query parameters
query.pop("sslmode", None)
query.pop("channel_binding", None)

database_url = urlunparse(
    parsed._replace(query=urlencode(query, doseq=True))
)

# Create async engine for PostgreSQL with asyncpg
engine = create_async_engine(
    database_url,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,
    max_overflow=10,
    connect_args={"ssl": True},  # Enable SSL explicitly
)

# Async session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    """Dependency for getting async database session."""
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
