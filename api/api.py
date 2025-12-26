"""
Vercel-compatible API endpoint for the Physical AI Textbook Platform.
This follows Vercel's Python function pattern.
"""

import os
import json
from mangum import Mangum
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Import your existing FastAPI app components
from api.main import app

# Add CORS middleware for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the Mangum adapter
handler = Mangum(app, lifespan="off")

# For Vercel Python function compatibility
def main_func(event, context):
    return handler(event, context)

# If you want to run this locally for testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )