from src.application.common.unit_of_work import IUnitOfWork, OutboxEvent


class UnitOfWork(IUnitOfWork):
    def __init__(self, session):
        self._session = session
        self._events: list[OutboxEvent] = []

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.rollback()

    async def register_event(self, event: OutboxEvent) -> None:
        """Регистрирует событие для отправки через outbox pattern"""
        self._events.append(event)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
        self._events.clear()
