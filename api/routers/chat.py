from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime
import asyncpg

from api.db.connection import get_connection
from api.dependencies import get_rag_service
from api.services.rag_service import RAGService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="", tags=["chat"])

class ChatRequest(BaseModel):
    user_id: Optional[int] = None
    session_id: Optional[int] = None
    message: str


async def ensure_session_exists(session_id: int, user_id: Optional[int]) -> bool:
    """
    Check if session exists, create it if it doesn't.

    Args:
        session_id: The session ID to check/create
        user_id: The user ID associated with the session (can be None for anonymous users)

    Returns:
        bool: True if session exists or was created successfully
    """
    async with get_connection() as conn:
        # Check if session exists
        session = await conn.fetchrow(
            "SELECT id FROM chat_sessions WHERE id = $1", session_id
        )

        if session:
            logger.debug(f"Session {session_id} exists for user {user_id}")
            return True

        # Session doesn't exist, create it
        try:
            # Only insert user_id if it's a valid user (not 0 or null)
            if user_id and user_id != 0:
                await conn.execute(
                    "INSERT INTO chat_sessions (id, user_id) VALUES ($1, $2)",
                    session_id, user_id
                )
            else:
                # Create session without user_id for anonymous users
                await conn.execute(
                    "INSERT INTO chat_sessions (id) VALUES ($1)",
                    session_id
                )
            logger.info(f"Created new session {session_id} for user {user_id}")
            return True
        except asyncpg.UniqueViolationError:
            # Another request might have created the session concurrently
            logger.warning(f"Session {session_id} already exists (concurrent creation)")
            return True
        except Exception as e:
            logger.error(f"Error creating session {session_id} for user {user_id}: {e}")
            return False


@router.post("/")
async def handle_chat_message(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Handle incoming chat messages, store them in the database, and generate AI response.

    If session_id is not provided or doesn't exist, creates a new session automatically.
    """
    try:
        session_id = request.session_id

        # If no session_id provided, create a new session
        if session_id is None:
            async with get_connection() as conn:
                # Create a new session for the user (user_id can be null for anonymous users)
                # Only insert user_id if it's a valid user (not 0 or null)
                if request.user_id and request.user_id != 0:
                    result = await conn.fetchrow(
                        "INSERT INTO chat_sessions (user_id) VALUES ($1) RETURNING id",
                        request.user_id
                    )
                else:
                    # Create session without user_id for anonymous users
                    result = await conn.fetchrow(
                        "INSERT INTO chat_sessions DEFAULT VALUES RETURNING id"
                    )
                session_id = result["id"]
                logger.info(f"Created new session {session_id} for user {request.user_id}")
        else:
            # Ensure the provided session exists
            session_exists = await ensure_session_exists(session_id, request.user_id)
            if not session_exists:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to ensure session exists"
                )

        # Insert the user message into the database
        async with get_connection() as conn:
            await conn.execute(
                """
                INSERT INTO chat_messages (session_id, role, content, created_at)
                VALUES ($1, $2, $3, $4)
                """,
                session_id, "user", request.message, datetime.utcnow()
            )
            logger.info(f"Inserted user message for session {session_id}")

        # Generate AI response using RAG service
        logger.info(f"Generating AI response for message: {request.message[:50]}...")
        try:
            rag_response = await rag_service.answer_question(
                question=request.message,
                top_k=5
            )
            # Check if response is valid
            if not rag_response or "answer" not in rag_response:
                logger.error("Invalid response from RAG service")
                raise Exception("Invalid response from RAG service")
        except Exception as rag_error:
            logger.error(f"Error in RAG service: {rag_error}")
            # Return a helpful error response to the frontend
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI service error: {str(rag_error)}"
            )

        # Insert the AI response into the database
        try:
            async with get_connection() as conn:
                await conn.execute(
                    """
                    INSERT INTO chat_messages (session_id, role, content, created_at, metadata)
                    VALUES ($1, $2, $3, $4, $5)
                    """,
                    session_id, "assistant", rag_response["answer"], datetime.utcnow(),
                    {"sources": rag_response["sources"]}
                )
                logger.info(f"Inserted AI response for session {session_id}")
        except Exception as db_error:
            logger.error(f"Database error when inserting AI response: {db_error}")
            # Still return the response even if DB insertion fails
            pass  # For now, we'll continue even if DB insertion fails

        # Return the session_id, AI response, and sources
        return {
            "status": "success",
            "session_id": session_id,
            "response": rag_response["answer"],
            "sources": rag_response["sources"]
        }

    except asyncpg.ForeignKeyViolationError as e:
        logger.error(f"Foreign key violation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid session_id: session does not exist"
        )
    except asyncpg.UniqueViolationError as e:
        logger.error(f"Unique constraint violation: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A session with this ID already exists but was not properly handled"
        )
    except Exception as e:
        logger.error(f"Unexpected error in handle_chat_message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )