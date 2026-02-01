"""Application settings configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="postgres", description="Database password")
    name: str = Field(default="app_db", description="Database name")
    echo: bool = Field(default=False, description="Echo SQL queries")
    pool_size: int = Field(default=5, description="Database connection pool size")
    max_overflow: int = Field(default=10, description="Max overflow connections")

    @property
    def url(self) -> str:
        """Generate database URL."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class AppSettings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    name: str = Field(default="Python Web Template", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    description: str = Field(
        default="A template for building web applications with Python",
        description="Application description",
    )
    debug: bool = Field(default=False, description="Debug mode")
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Environment",
    )
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, description="API port")
    reload: bool = Field(default=False, description="Auto-reload on code changes")
    workers: int = Field(default=1, description="Number of worker processes")


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    level: Literal["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level",
    )
    format: str = Field(
        default=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        description="Log format",
    )
    serialize: bool = Field(default=False, description="Serialize logs as JSON")
    diagnose: bool = Field(default=True, description="Enable diagnostic information")
    backtrace: bool = Field(default=True, description="Enable backtrace in logs")


class CORSSettings(BaseSettings):
    """CORS configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="CORS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    enabled: bool = Field(default=True, description="Enable CORS")
    allow_origins: list[str] = Field(
        default=["*"],
        description="Allowed origins",
    )
    allow_credentials: bool = Field(default=True, description="Allow credentials")
    allow_methods: list[str] = Field(default=["*"], description="Allowed methods")
    allow_headers: list[str] = Field(default=["*"], description="Allowed headers")

    @field_validator("allow_origins", "allow_methods", "allow_headers", mode="before")
    @classmethod
    def split_str(cls, v):
        """Split comma-separated string into list."""
        if isinstance(v, str):
            return [item.strip() for item in v.split(",")]
        return v


class APISettings(BaseSettings):
    """API configuration settings."""

    model_config = SettingsConfigDict(
        env_prefix="API_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    prefix: str = Field(default="/api/v1", description="API prefix")
    docs_url: str | None = Field(default="/docs", description="Swagger docs URL")
    redoc_url: str | None = Field(default="/redoc", description="ReDoc URL")
    openapi_url: str | None = Field(default="/openapi.json", description="OpenAPI URL")
    title: str = Field(default="Python Web Template API", description="API title")
    summary: str = Field(
        default="REST API for Python Web Template",
        description="API summary",
    )


class Settings(BaseSettings):
    """Main application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app: AppSettings = Field(default_factory=AppSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    cors: CORSSettings = Field(default_factory=CORSSettings)
    api: APISettings = Field(default_factory=APISettings)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
