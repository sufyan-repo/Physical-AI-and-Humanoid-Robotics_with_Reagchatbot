"""
Pydantic models for chat functionality.

Defines request/response models for the RAG chatbot API.
"""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """A single chat message in a conversation."""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    created_at: Optional[datetime] = Field(None, description="Message timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "What is inverse kinematics?",
                "created_at": "2024-01-15T10:30:00Z",
            }
        }


class ChatRequest(BaseModel):
    """Request body for chat API."""

    message: str = Field(..., min_length=1, max_length=5000, description="User's message")
    session_id: Optional[int] = Field(None, description="Session ID for conversation continuity")
    selected_text: Optional[str] = Field(None, description="Text selected by user for context")
    chapter_slug: Optional[str] = Field(None, description="Current chapter slug for context")
    user_id: Optional[int] = Field(None, description="User ID if authenticated")

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Can you explain this concept in simpler terms?",
                "session_id": 42,
                "selected_text": "The Jacobian matrix is used to map joint velocities to end-effector velocities.",
                "chapter_slug": "module-2-kinematics-intro",
                "user_id": 123,
            }
        }


class ChatResponse(BaseModel):
    """Response body for chat API."""

    response: str = Field(..., description="AI assistant's response")
    session_id: int = Field(..., description="Session ID for this conversation")
    sources: List[str] = Field(default_factory=list, description="Source chapters used in response")

    class Config:
        json_schema_extra = {
            "example": {
                "response": "Inverse kinematics (IK) is the process of determining joint angles needed to achieve a desired end-effector position...",
                "session_id": 42,
                "sources": ["module-2-kinematics-intro", "module-2-ik-basics"],
            }
        }


class ChatSession(BaseModel):
    """A chat conversation session."""

    id: int = Field(..., description="Session ID")
    user_id: Optional[int] = Field(None, description="User ID if authenticated")
    created_at: datetime = Field(..., description="Session creation timestamp")
    messages: List[ChatMessage] = Field(default_factory=list, description="Messages in this session")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 42,
                "user_id": 123,
                "created_at": "2024-01-15T10:00:00Z",
                "messages": [
                    {
                        "role": "user",
                        "content": "What is inverse kinematics?",
                        "created_at": "2024-01-15T10:30:00Z",
                    },
                    {
                        "role": "assistant",
                        "content": "Inverse kinematics (IK) is...",
                        "created_at": "2024-01-15T10:30:05Z",
                    },
                ],
            }
        }