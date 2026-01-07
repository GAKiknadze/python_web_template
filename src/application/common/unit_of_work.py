from typing import Protocol
from .value_objects import OutboxMessage


class IUnitOfWork(Protocol):
    _messages: list[OutboxMessage] = []
    
    async def __aenter__(self) -> "IUnitOfWork":
        ...

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        ...
    
    async def register_outbox_message(self, message: OutboxMessage) -> None:
        self._messages.append(message)

    async def commit(self) -> None:
        ...

    async def rollback(self) -> None:
        ...