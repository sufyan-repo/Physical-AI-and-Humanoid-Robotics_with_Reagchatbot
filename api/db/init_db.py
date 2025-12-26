"""
Database initialization script for chat tables.

This script creates the necessary tables for the chatbot functionality.
"""

import logging
import asyncpg
from api.db.connection import get_db_pool

logger = logging.getLogger(__name__)

# SQL queries to create tables
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_CHAT_SESSIONS_TABLE = """
CREATE TABLE IF NOT EXISTS chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_CHAT_MESSAGES_TABLE = """
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);
"""

CREATE_UPDATED_AT_FUNCTION = """
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';
"""

CREATE_SESSIONS_UPDATED_AT_TRIGGER = """
CREATE OR REPLACE TRIGGER update_chat_sessions_updated_at
    BEFORE UPDATE ON chat_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
"""

async def init_db():
    """Initialize the database with required tables."""
    logger.info("Initializing database tables...")

    pool = await get_db_pool()

    async with pool.acquire() as conn:
        # Create users table first (since chat_sessions references it)
        await conn.execute(CREATE_USERS_TABLE)
        logger.info("✓ Created/verified users table")

        # Create chat_sessions table
        await conn.execute(CREATE_CHAT_SESSIONS_TABLE)
        logger.info("✓ Created/verified chat_sessions table")

        # Create chat_messages table
        await conn.execute(CREATE_CHAT_MESSAGES_TABLE)
        logger.info("✓ Created/verified chat_messages table")

        # Create updated_at function
        await conn.execute(CREATE_UPDATED_AT_FUNCTION)
        logger.info("✓ Created/verified updated_at function")

        # Create updated_at trigger
        await conn.execute(CREATE_SESSIONS_UPDATED_AT_TRIGGER)
        logger.info("✓ Created/verified updated_at trigger")

    logger.info("Database initialization completed successfully!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())