"""
Debug endpoints for troubleshooting the chatbot functionality.
"""

from fastapi import APIRouter, HTTPException, Depends
import logging

from api.dependencies import get_rag_service
from api.services.rag_service import RAGService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/services-status")
async def check_services_status(rag_service: RAGService = Depends(get_rag_service)):
    """
    Check if all required services are properly initialized.
    """
    try:
        # Test if RAG service is available
        status = {
            "rag_service": "available",
            "vector_service": "available",  # This will be checked internally
            "cohere_service": "available"   # This will be checked internally
        }

        # Try a simple test
        test_embedding = await rag_service.vector_service.client.get_collections()
        status["vector_service"] = "connected"

        return {"status": "healthy", "services": status}
    except Exception as e:
        logger.error(f"Service status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Service unavailable: {str(e)}")

@router.get("/test-embedding")
async def test_embedding_generation(rag_service: RAGService = Depends(get_rag_service)):
    """
    Test if embedding generation is working.
    """
    try:
        test_text = "This is a test for embedding generation."
        embedding = await rag_service.cohere_service.generate_embedding(test_text)
        return {
            "success": True,
            "embedding_length": len(embedding) if embedding else 0,
            "sample_values": embedding[:5] if embedding and len(embedding) > 0 else []
        }
    except Exception as e:
        logger.error(f"Embedding test failed: {e}")
        raise HTTPException(status_code=500, detail=f"Embedding service error: {str(e)}")