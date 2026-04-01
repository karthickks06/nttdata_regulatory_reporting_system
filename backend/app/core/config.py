"""Application configuration using Pydantic Settings"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application Settings
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/regulatory_reporting"

    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # OpenAI API
    OPENAI_API_KEY: str = ""

    # Storage
    STORAGE_PATH: Path = Path("./storage")

    # ChromaDB
    CHROMA_PATH: Path = Path("./chroma_data")

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    MAX_REQUESTS_PER_MINUTE: int = 60

    # Cleanup Settings
    CLEANUP_INTERVAL_HOURS: int = 24
    SESSION_EXPIRY_DAYS: int = 7
    CACHE_EXPIRY_HOURS: int = 1
    RATE_LIMIT_EXPIRY_HOURS: int = 1
    TEMP_FILE_EXPIRY_DAYS: int = 1

    # Agent Settings
    AGENT_TIMEOUT_SECONDS: int = 300
    MAX_AGENT_RETRIES: int = 3

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Global settings instance
settings = Settings()
