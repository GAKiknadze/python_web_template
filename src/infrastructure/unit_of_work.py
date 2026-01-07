from src.application.common.unit_of_work import IUnitOfWork, OutboxMessage

class UnitOfWork(IUnitOfWork):
    def __init__(self, session):
        self._session = session
        self._messages: list[OutboxMessage] = []

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.rollback()

    async def register_outbox_message(self, message: OutboxMessage) -> None:
        self._messages.append(message)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
        self._messages.clear()
