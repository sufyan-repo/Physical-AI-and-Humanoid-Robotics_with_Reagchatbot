"""
Pydantic models for user profiles.

Defines request/response models for user profile management.
"""

from typing import Optional
from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    """User profile with experience levels and preferences."""

    id: int = Field(..., description="Profile ID")
    user_id: int = Field(..., description="Associated user ID")
    programming_experience_level: Optional[str] = Field(
        None,
        description="Programming experience: 'beginner', 'intermediate', 'advanced'",
    )
    robotics_experience_level: Optional[str] = Field(
        None,
        description="Robotics experience: 'beginner', 'intermediate', 'advanced'",
    )
    available_hardware: Optional[str] = Field(
        None,
        description="Available robot hardware (e.g., 'LeRobot', 'Custom Arm', 'None')",
    )
    preferred_language: str = Field(
        default="en",
        description="Preferred language code (e.g., 'en', 'es', 'zh')",
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 123,
                "programming_experience_level": "intermediate",
                "robotics_experience_level": "beginner",
                "available_hardware": "LeRobot",
                "preferred_language": "en",
            }
        }


class UserProfileUpdate(BaseModel):
    """Request body for updating user profile."""

    programming_experience_level: Optional[str] = Field(
        None,
        description="Programming experience: 'beginner', 'intermediate', 'advanced'",
    )
    robotics_experience_level: Optional[str] = Field(
        None,
        description="Robotics experience: 'beginner', 'intermediate', 'advanced'",
    )
    available_hardware: Optional[str] = Field(
        None,
        description="Available robot hardware",
    )
    preferred_language: Optional[str] = Field(
        None,
        description="Preferred language code",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "programming_experience_level": "advanced",
                "robotics_experience_level": "intermediate",
                "available_hardware": "Custom 6-DOF Arm",
                "preferred_language": "en",
            }
        }