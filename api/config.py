"""
Configuration loader for the Physical AI Textbook Platform API.

Loads and validates environment variables using Pydantic settings.
"""

import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = Field(..., description="PostgreSQL connection string")

    # Qdrant Vector Database
    qdrant_url: str = Field(..., description="Qdrant server URL")
    qdrant_api_key: str | None = Field(None, description="Qdrant API key (optional for local)")
    qdrant_collection_name: str = Field(
        default="physical_ai_textbook",
        description="Qdrant collection name",
    )

    # Google Gemini AI
    gemini_api_key: str = Field(..., description="Google Gemini API key")
    gemini_embedding_model: str = Field(
        default="text-embedding-004",
        description="Gemini embedding model",
    )
    gemini_chat_model: str = Field(
        default="gemini-1.5-flash",
        description="Gemini chat model",
    )

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    cors_origins: str = Field(
        default="http://localhost:3000,http://localhost:8000",
        description="Comma-separated CORS origins",
    )

    # Authentication (Better-Auth)
    auth_secret: str = Field(..., description="Auth secret key")
    auth_trust_host: bool = Field(default=True, description="Trust host header")

    # Frontend URLs
    site_url: str = Field(default="http://localhost:3000", description="Site URL")
    base_url: str = Field(default="/", description="Base URL path")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @validator("cors_origins")
    def parse_cors_origins(cls, v: str) -> List[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in v.split(",") if origin.strip()]

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]
        return self.cors_origins


# Global settings instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """
    Get or create the global settings instance.

    Returns:
        Settings: The application settings
    """
    global _settings

    if _settings is None:
        _settings = Settings()

    return _settings


def reload_settings() -> Settings:
    """
    Force reload settings from environment.

    Useful for testing or when environment changes.

    Returns:
        Settings: The reloaded settings
    """
    global _settings
    _settings = Settings()
    return _settings