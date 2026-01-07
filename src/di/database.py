from dishka import Provider, Scope, provide
from pydantic import BaseModel
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from src.application.common.unit_of_work import IUnitOfWork
from src.infrastructure.unit_of_work import UnitOfWork


class DBConfig(BaseModel):
    url: str


class DBProvider(Provider):
    def __init__(self, config: DBConfig):
        self._config = config
    
    @provide(scope=Scope.APP)
    def get_engine(self) -> AsyncEngine:
        if getattr(self, "_engine", None) is None:
            self._engine = create_async_engine(self._config.url)
        return self._engine
    
    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def get_session(self, engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSession(engine, expire_on_commit=False) as session:
            yield session
    
    @provide(scope=Scope.REQUEST, provides=IUnitOfWork)
    async def get_unit_of_work(self, session: AsyncSession) -> AsyncGenerator[IUnitOfWork, None]:
        async with UnitOfWork(session=session) as uow:
            yield uow
