from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from src.infrastructure.config import get_settings

from .exception_handlers import all_exceptions_handler
from .v1 import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application and initializing Dishka container.")
    yield
    logger.info("Shutting down application and closing Dishka container.")
    await app.state.dishka_container.close()


def create_rest_app(container: AsyncContainer) -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.api.title,
        description=settings.app.description,
        version=settings.app.version,
        summary=settings.api.summary,
        docs_url=settings.api.docs_url,
        redoc_url=settings.api.redoc_url,
        openapi_url=settings.api.openapi_url,
        debug=settings.app.debug,
        lifespan=lifespan,
    )

    # Setup CORS
    if settings.cors.enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors.allow_origins,
            allow_credentials=settings.cors.allow_credentials,
            allow_methods=settings.cors.allow_methods,
            allow_headers=settings.cors.allow_headers,
        )

    setup_dishka(container=container, app=app)

    app.include_router(v1_router, prefix=settings.api.prefix)

    app.add_exception_handler(Exception, all_exceptions_handler)

    return app
