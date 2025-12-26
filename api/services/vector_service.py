"""
Vector database service using Qdrant.

This module provides a wrapper for Qdrant operations including
collection management, vector upsertion, and semantic search.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from uuid import uuid4

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
)

logger = logging.getLogger(__name__)


class VectorService:
    """
    Service for vector database operations using Qdrant.

    Handles collection management, document indexing, and similarity search
    for the RAG chatbot.
    """

    def __init__(self):
        """Initialize Qdrant client with environment configuration."""
        self.url = os.getenv("QDRANT_URL")
        self.api_key = os.getenv("QDRANT_API_KEY")
        self.collection_name = os.getenv("QDRANT_COLLECTION_NAME", "physical_ai_textbook")

        if not self.url:
            raise RuntimeError("QDRANT_URL environment variable is not set")

        # API key is optional for local instances
        self.client = AsyncQdrantClient(
            url=self.url,
            api_key=self.api_key,
        )

        logger.info(f"Initialized VectorService with collection: {self.collection_name}")

    async def create_collection(self, vector_size: int = 768, force_recreate: bool = False) -> None:
        """
        Create a new collection for storing document embeddings.

        Args:
            vector_size: Dimension of the embedding vectors (default: 768 for text-embedding-004)
            force_recreate: If True, delete and recreate existing collection
        """
        try:
            # Check if collection exists
            collections = await self.client.get_collections()
            exists = any(c.name == self.collection_name for c in collections.collections)

            if exists:
                if force_recreate:
                    logger.warning(f"Deleting existing collection: {self.collection_name}")
                    await self.client.delete_collection(self.collection_name)
                else:
                    logger.info(f"Collection {self.collection_name} already exists")
                    return

            # Create collection with cosine distance for semantic similarity
            await self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

            logger.info(f"Created collection: {self.collection_name} (vector_size={vector_size})")

        except Exception as e:
            logger.error(f"Failed to create collection: {e}")
            raise

    async def upsert_documents(
        self,
        documents: List[Dict[str, Any]],
        embeddings: List[List[float]],
    ) -> None:
        """
        Insert or update document embeddings in the collection.

        Args:
            documents: List of document metadata dicts with keys:
                      - chapter_slug: str
                      - chunk_index: int
                      - content: str
                      - module_name: str (optional)
            embeddings: List of embedding vectors (same length as documents)

        Raises:
            ValueError: If documents and embeddings lengths don't match
        """
        if len(documents) != len(embeddings):
            raise ValueError(
                f"Documents ({len(documents)}) and embeddings ({len(embeddings)}) "
                "must have the same length"
            )

        if not documents:
            logger.warning("No documents to upsert")
            return

        # Create points with UUIDs as IDs
        points = [
            PointStruct(
                id=str(uuid4()),
                vector=embedding,
                payload=doc,
            )
            for doc, embedding in zip(documents, embeddings)
        ]

        try:
            await self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            logger.info(f"Upserted {len(points)} document chunks to {self.collection_name}")

        except Exception as e:
            logger.error(f"Failed to upsert documents: {e}")
            raise

    async def search(
        self,
        query_vector: List[float],
        limit: int = 5,
        chapter_slug: Optional[str] = None,
        module_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents using vector similarity.

        Args:
            query_vector: The embedding vector of the search query
            limit: Maximum number of results to return
            chapter_slug: Optional filter by specific chapter
            module_name: Optional filter by module

        Returns:
            List of search results with keys:
                - id: str
                - score: float
                - payload: Dict with document metadata
        """
        # Check if vector service is properly initialized
        if not self.client:
            logger.error("Vector service client not initialized")
            return []

        # Build filters if provided
        query_filter = None
        if chapter_slug or module_name:
            conditions = []
            if chapter_slug:
                conditions.append(
                    FieldCondition(
                        key="chapter_slug",
                        match=MatchValue(value=chapter_slug),
                    )
                )
            if module_name:
                conditions.append(
                    FieldCondition(
                        key="module_name",
                        match=MatchValue(value=module_name),
                    )
                )
            query_filter = Filter(must=conditions)

        try:
            # Use query_points for AsyncQdrantClient (new API)
            response = await self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                query_filter=query_filter,
            )
            results = response.points

            # Format results
            formatted = [
                {
                    "id": str(result.id),
                    "score": result.score,
                    "payload": result.payload,
                }
                for result in results
            ]

            logger.info(f"Found {len(formatted)} results for search query")
            return formatted

        except Exception as e:
            logger.error(f"Search failed: {e}")
            # Return empty list instead of raising exception to prevent complete failure
            return []

    async def delete_by_chapter(self, chapter_slug: str) -> None:
        """
        Delete all document chunks for a specific chapter.

        Useful when updating chapter content.

        Args:
            chapter_slug: The chapter slug to delete
        """
        try:
            # Qdrant doesn't have a direct delete by filter,
            # so we search first, then delete by IDs
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="chapter_slug",
                        match=MatchValue(value=chapter_slug),
                    )
                ]
            )

            # Scroll through all matching points
            points = await self.client.scroll(
                collection_name=self.collection_name,
                scroll_filter=search_filter,
                limit=10000,
            )

            if points[0]:  # points is tuple (records, next_page_offset)
                point_ids = [str(p.id) for p in points[0]]
                await self.client.delete(
                    collection_name=self.collection_name,
                    points_selector=point_ids,
                )
                logger.info(f"Deleted {len(point_ids)} chunks for chapter: {chapter_slug}")
            else:
                logger.info(f"No chunks found for chapter: {chapter_slug}")

        except Exception as e:
            logger.error(f"Failed to delete chapter chunks: {e}")
            raise

    async def close(self) -> None:
        """Close the Qdrant client connection."""
        if self.client:
            await self.client.close()
            logger.info("Closed Qdrant client connection")