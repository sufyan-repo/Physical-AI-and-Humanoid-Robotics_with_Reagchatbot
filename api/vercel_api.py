"""
Vercel-specific entry point for the Physical AI Textbook Platform API.
This file adapts the FastAPI app for Vercel's serverless functions.
"""

import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

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

# Create FastAPI app (without lifespan for Vercel compatibility)
app = FastAPI(
    title="Physical AI Textbook Platform API",
    description="Backend API for the Physical AI Textbook with RAG chatbot",
    version="1.0.0",
)

# Configure CORS for Vercel deployment
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    # Add your Vercel deployment URL here after deployment
    # "https://your-project.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
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

# Create the Mangum handler for ASGI compatibility
handler = Mangum(app)

# For Vercel compatibility
def main(event, context):
    return handler(event, context)

# For direct usage with uvicorn or other ASGI servers
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))