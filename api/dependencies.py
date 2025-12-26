"""
Dependency injection functions for FastAPI endpoints.

This module provides dependency functions that can be used
across routers without creating circular imports.
"""

import logging
from typing import Optional
from api.services import VectorService, CohereService, RAGService

logger = logging.getLogger(__name__)

# Global service instances (initialized in main.py lifespan)
_vector_service: Optional[VectorService] = None


def set_vector_service(service: VectorService) -> None:
    """
    Set the global vector service instance.

    Called during application startup.

    Args:
        service: The initialized vector service
    """
    global _vector_service
    _vector_service = service


def get_vector_service() -> VectorService:
    """
    Dependency to get the global vector service instance.

    Returns:
        VectorService: The initialized vector service

    Raises:
        RuntimeError: If vector service is not initialized
    """
    if _vector_service is None:
        raise RuntimeError("Vector service not initialized")
    return _vector_service


async def get_rag_service() -> RAGService:
    """
    Dependency to get RAG service instance.

    Returns:
        RAGService: The initialized RAG service

    Raises:
        RuntimeError: If vector service is not initialized or if services fail to initialize
    """
    try:
        vector_service = get_vector_service()
        # Test vector service connection
        try:
            await vector_service.client.get_collections()
            logger.debug("Vector service connection verified")
        except Exception as vec_error:
            logger.warning(f"Vector service connection test failed: {vec_error}")
            # Continue anyway, will use fallback behavior

        cohere_service = CohereService()
        # Test cohere service with a simple embedding
        try:
            await cohere_service.generate_embedding("test")
            logger.debug("Cohere service connection verified")
        except Exception as coh_error:
            logger.warning(f"Cohere service connection test failed: {coh_error}")
            # Continue anyway, will use fallback behavior

        return RAGService(vector_service, cohere_service)
    except Exception as e:
        logger.error(f"Failed to initialize RAG service: {e}")
        raise RuntimeError(f"RAG service initialization failed: {e}") from e