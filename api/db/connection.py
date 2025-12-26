"""
Database connection pool management for Neon Postgres.

This module provides async connection pooling using asyncpg,
optimized for Neon's serverless architecture with pooled connections.
"""

import asyncpg
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Global connection pool
_pool: Optional[asyncpg.Pool] = None


async def get_db_pool() -> asyncpg.Pool:
    """
    Get or create the database connection pool.

    Uses Neon's pooled connection endpoint for better performance
    in serverless environments.

    Returns:
        asyncpg.Pool: The database connection pool

    Raises:
        RuntimeError: If DATABASE_URL is not configured
    """
    global _pool

    if _pool is None:
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise RuntimeError("DATABASE_URL environment variable is not set")

        # Verify we're using pooled connection (should end with -pooler)
        if "-pooler" not in database_url:
            logger.warning(
                "DATABASE_URL does not appear to use Neon's pooled connection. "
                "Consider using the pooled endpoint (ends with -pooler) for better performance."
            )

        logger.info("Creating database connection pool...")

        # Create pool with settings optimized for Neon
        _pool = await asyncpg.create_pool(
            database_url,
            min_size=1,          # Minimum connections
            max_size=10,         # Maximum connections
            max_queries=50000,   # Max queries per connection
            max_inactive_connection_lifetime=300,  # 5 minutes
            command_timeout=60,  # 60 second timeout
        )

        logger.info("Database connection pool created successfully")

    return _pool


async def close_db_pool() -> None:
    """
    Close the database connection pool.

    Should be called on application shutdown to gracefully
    close all connections.
    """
    global _pool

    if _pool is not None:
        logger.info("Closing database connection pool...")
        await _pool.close()
        _pool = None
        logger.info("Database connection pool closed")


@asynccontextmanager
async def get_connection() -> AsyncGenerator[asyncpg.Connection, None]:
    """
    Get a database connection from the pool.

    This is an async context manager that returns a connection
    and automatically releases it when done.

    Usage:
        async with get_connection() as conn:
            result = await conn.fetchrow("SELECT * FROM users WHERE id = $1", user_id)

    Yields:
        asyncpg.Connection: A database connection
    """
    pool = await get_db_pool()
    async with pool.acquire() as connection:
        yield connection