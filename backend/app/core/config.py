"""Application configuration using Pydantic Settings"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Base Directory
    BASE_DIR: Path = Path(__file__).parent.parent.parent

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

    # LLM Provider Configuration
    LLM_PROVIDER: str = "azure"  # "openai" or "azure"

    # OpenAI API
    OPENAI_API_KEY: str = ""

    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4.1"
    AZURE_OPENAI_API_VERSION: str = "2024-12-01-preview"

    # Model Configuration
    DEFAULT_MODEL_NAME: str = "gpt-4.1"
    LLM_MODEL_NAME: str = "gpt-4.1"
    DEFAULT_TEMPERATURE: float = 0.1
    LLM_TEMPERATURE: float = 0.1
    DEFAULT_MAX_TOKENS: int = 4096
    LLM_MAX_TOKENS: int = 4096
    DEFAULT_TOP_P: float = 1.0
    LLM_TOP_P: float = 1.0

    # Storage - all application files stored here
    STORAGE_PATH: Path = Path("./storage")

    # ChromaDB - stored inside storage folder
    CHROMA_PATH: Path = Path("./storage/chroma_data")

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
