"""Tests for configuration settings."""

import pytest
from pydantic import ValidationError
from src.infrastructure.config.settings import (
    APISettings,
    AppSettings,
    CORSSettings,
    DatabaseSettings,
    LoggingSettings,
    Settings,
)


def test_database_settings_defaults():
    """Test database settings with default values."""
    db_settings = DatabaseSettings()

    assert db_settings.host == "localhost"
    assert db_settings.port == 5432
    assert db_settings.user == "postgres"
    assert db_settings.name == "app_db"
    assert db_settings.echo is False
    assert db_settings.pool_size == 5


def test_database_settings_url_generation():
    """Test database URL generation."""
    db_settings = DatabaseSettings(
        host="db.example.com",
        port=5433,
        user="testuser",
        password="testpass",
        name="testdb",
    )

    expected_url = "postgresql+asyncpg://testuser:testpass@db.example.com:5433/testdb"
    assert db_settings.url == expected_url


def test_app_settings_defaults():
    """Test app settings with default values."""
    app_settings = AppSettings()

    assert app_settings.name == "Python Web Template"
    assert app_settings.version == "0.1.0"
    assert app_settings.debug is False
    assert app_settings.environment == "development"
    assert app_settings.host == "0.0.0.0"
    assert app_settings.port == 8000
    assert app_settings.workers == 1


def test_app_settings_environment_validation():
    """Test app settings environment validation."""
    # Valid environments
    for env in ["development", "staging", "production"]:
        app_settings = AppSettings(environment=env)
        assert app_settings.environment == env

    # Invalid environment should raise validation error
    with pytest.raises(ValidationError):
        AppSettings(environment="invalid")


def test_logging_settings_defaults():
    """Test logging settings with default values."""
    log_settings = LoggingSettings()

    assert log_settings.level == "INFO"
    assert log_settings.serialize is False
    assert log_settings.diagnose is True
    assert log_settings.backtrace is True


def test_logging_settings_level_validation():
    """Test logging level validation."""
    valid_levels = ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    for level in valid_levels:
        log_settings = LoggingSettings(level=level)
        assert log_settings.level == level

    # Invalid level should raise validation error
    with pytest.raises(ValidationError):
        LoggingSettings(level="INVALID")


def test_cors_settings_defaults():
    """Test CORS settings with default values."""
    cors_settings = CORSSettings()

    assert cors_settings.enabled is True
    assert cors_settings.allow_origins == ["*"]
    assert cors_settings.allow_credentials is True
    assert cors_settings.allow_methods == ["*"]
    assert cors_settings.allow_headers == ["*"]


def test_cors_settings_string_to_list_conversion():
    """Test CORS settings convert comma-separated strings to lists."""
    cors_settings = CORSSettings(
        allow_origins="https://example.com,https://test.com",
        allow_methods="GET,POST,PUT,DELETE",
        allow_headers="Content-Type,Authorization",
    )

    assert cors_settings.allow_origins == ["https://example.com", "https://test.com"]
    assert cors_settings.allow_methods == ["GET", "POST", "PUT", "DELETE"]
    assert cors_settings.allow_headers == ["Content-Type", "Authorization"]


def test_api_settings_defaults():
    """Test API settings with default values."""
    api_settings = APISettings()

    assert api_settings.prefix == "/api/v1"
    assert api_settings.docs_url == "/docs"
    assert api_settings.redoc_url == "/redoc"
    assert api_settings.openapi_url == "/openapi.json"
    assert api_settings.title == "Python Web Template API"


def test_settings_composition():
    """Test main Settings class composition."""
    settings = Settings()

    # Check all subsettings are present
    assert isinstance(settings.app, AppSettings)
    assert isinstance(settings.database, DatabaseSettings)
    assert isinstance(settings.logging, LoggingSettings)
    assert isinstance(settings.cors, CORSSettings)
    assert isinstance(settings.api, APISettings)


def test_settings_with_custom_values():
    """Test Settings with custom values."""
    settings = Settings()

    # Should use defaults from subsettings
    assert settings.app.name == "Python Web Template"
    assert settings.database.host == "localhost"
    assert settings.logging.level == "INFO"


def test_database_settings_custom_config():
    """Test database settings with custom configuration."""
    db_settings = DatabaseSettings(
        host="custom-host",
        port=3306,
        user="customuser",
        password="custompass",
        name="customdb",
        echo=True,
        pool_size=10,
        max_overflow=20,
    )

    assert db_settings.host == "custom-host"
    assert db_settings.port == 3306
    assert db_settings.user == "customuser"
    assert db_settings.password == "custompass"
    assert db_settings.name == "customdb"
    assert db_settings.echo is True
    assert db_settings.pool_size == 10
    assert db_settings.max_overflow == 20


def test_app_settings_port_validation():
    """Test app settings port is an integer."""
    app_settings = AppSettings(port=9000)
    assert app_settings.port == 9000
    assert isinstance(app_settings.port, int)

    # String number should be converted to int
    app_settings = AppSettings(port="8080")
    assert app_settings.port == 8080
    assert isinstance(app_settings.port, int)


def test_cors_disabled():
    """Test CORS can be disabled."""
    cors_settings = CORSSettings(enabled=False)
    assert cors_settings.enabled is False


def test_api_settings_docs_disabled():
    """Test API docs can be disabled by setting to None."""
    api_settings = APISettings(
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    assert api_settings.docs_url is None
    assert api_settings.redoc_url is None
    assert api_settings.openapi_url is None
