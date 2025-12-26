"""
FastAPI application entry point for Physical AI Textbook Platform.

This module initializes the FastAPI app, configures CORS, registers routers,
and handles startup/shutdown events for database and vector store connections.
"""

import os
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.db import get_db_pool, close_db_pool
from api.db.init_db import init_db
from api.services import VectorService
from api.dependencies import set_vector_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager for startup and shutdown events.

    Handles:
    - Database connection pool initialization
    - Vector service initialization
    - Qdrant collection verification
    - Graceful shutdown of connections
    """
    # Startup
    logger.info("Starting up Physical AI Textbook API...")

    try:
        # Initialize database pool
        pool = await get_db_pool()
        logger.info(f"✓ Database pool initialized: {pool}")

        # Initialize database tables
        await init_db()
        logger.info("✓ Database tables initialized")

        # Initialize vector service
        vector_service = VectorService()
        set_vector_service(vector_service)  # Set global instance
        logger.info("✓ Vector service initialized")

        # Verify/create Qdrant collection
        # Use 1024 for newer Cohere models
        await vector_service.create_collection(vector_size=1024, force_recreate=False)
        logger.info("✓ Qdrant collection verified")

        logger.info("🚀 Application startup complete")

    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

    yield  # Application runs here

    # Shutdown
    logger.info("Shutting down Physical AI Textbook API...")

    try:
        await vector_service.close()
        logger.info("✓ Vector service closed")

        await close_db_pool()
        logger.info("✓ Database pool closed")

        logger.info("👋 Application shutdown complete")

    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")


# Create FastAPI app
app = FastAPI(
    title="Physical AI Textbook Platform API",
    description="Backend API for the Physical AI Textbook with RAG chatbot",
    version="1.0.0",
    lifespan=lifespan,
)


# Configure CORS - add all localhost variants for development
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")
# Strip whitespace from origins
allowed_origins = [origin.strip() for origin in allowed_origins]

# Add environment-specific origins
environment = os.getenv("ENVIRONMENT", "development")
if environment == "production":
    # Add production-specific origins
    prod_origins = os.getenv("PROD_CORS_ORIGINS", "").strip()
    if prod_origins:
        allowed_origins.extend([origin.strip() for origin in prod_origins.split(",") if origin.strip()])

logger.info(f"CORS allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight for 10 minutes
)


# Health check endpoint
@app.get("/health", tags=["system"])
async def health_check():
    """Check API health status."""
    from api.dependencies import get_vector_service

    try:
        vector_service = get_vector_service()
        vector_status = "connected"
    except RuntimeError:
        vector_status = "not initialized"

    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "database": "connected",
            "vector_store": vector_status,
        },
    }


# Root endpoint
@app.get("/", tags=["system"])
async def root():
    """API root endpoint."""
    return {
        "message": "Physical AI Textbook Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Import and include routers
from api.routers import chat, debug

app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(debug.router, prefix="/api", tags=["debug"])

# Simple test endpoint for frontend connectivity
@app.get("/api/test")
async def test_connection():
    """Simple endpoint to test frontend-backend connectivity."""
    return {"status": "connected", "message": "Backend is reachable from frontend"}