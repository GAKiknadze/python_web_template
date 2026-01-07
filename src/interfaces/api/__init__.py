from contextlib import asynccontextmanager

from dishka import AsyncContainer
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from loguru import logger

from .exception_handlers import all_exceptions_handler
from .v1 import router as v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application and initializing Dishka container.")
    yield
    logger.info("Shutting down application and closing Dishka container.")
    await app.state.dishka_container.close()


def create_rest_app(container: AsyncContainer) -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    setup_dishka(container=container, app=app)

    app.include_router(v1_router, prefix="/v1")

    app.add_exception_handler(Exception, all_exceptions_handler)

    return app
