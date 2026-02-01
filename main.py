import sys

import uvicorn
from dishka import make_async_container
from loguru import logger
from src.di.database import DBConfig, DBProvider
from src.infrastructure.config import get_settings
from src.interfaces.api import create_rest_app


def configure_logging(settings):
    """Configure logging with settings."""
    logger.remove()  # Remove default handler
    logger.add(
        sink=sys.stdout,
        level=settings.logging.level,
        format=settings.logging.format,
        serialize=settings.logging.serialize,
        diagnose=settings.logging.diagnose,
        backtrace=settings.logging.backtrace,
    )


def main():
    """Main application entry point."""
    settings = get_settings()

    # Configure logging
    configure_logging(settings)

    logger.info(f"Starting {settings.app.name} v{settings.app.version}")
    logger.info(f"Environment: {settings.app.environment}")
    logger.info(f"Debug mode: {settings.app.debug}")

    # Create database configuration
    db_config = DBConfig(url=settings.database.url)

    # Create DI container
    container = make_async_container(
        DBProvider(config=db_config),
    )

    # Create FastAPI application
    app = create_rest_app(container)

    # Run application
    uvicorn.run(
        app=app,
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.reload,
        workers=settings.app.workers,
    )


if __name__ == "__main__":
    main()
