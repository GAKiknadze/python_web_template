from fastapi.responses import JSONResponse
from loguru import logger


async def all_exceptions_handler(*args, **kwargs) -> JSONResponse:  # noqa: RUF029
    logger.error("An error occurred: args={}, kwargs={}", args, kwargs)
    return JSONResponse({"args": str(args), "kwargs": str(kwargs)})
