import uvicorn
from dishka import make_async_container
from pydantic import Field
from pydantic_settings import BaseSettings
from src.di.database import DBConfig, DBProvider
from src.interfaces.api import create_rest_app


class AppSettings(BaseSettings):
    database: DBConfig = Field(...)

    class Config:
        extra = "ignore"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = AppSettings()  # pyright: ignore[reportCallIssue]

container = make_async_container(
    DBProvider(config=settings.database),
)

app = create_rest_app(container)


if __name__ == "__main__":
    uvicorn.run(app=app)
