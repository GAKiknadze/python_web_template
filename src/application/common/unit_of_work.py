from typing import Protocol

from .value_objects import OutboxEvent


class IUnitOfWork(Protocol):
    _events: list[OutboxEvent]

    async def __aenter__(self) -> "IUnitOfWork": ...

    async def __aexit__(self, exc_type, exc_value, traceback) -> None: ...

    async def register_event(self, event: OutboxEvent) -> None:
        """Регистрирует событие для отправки через outbox pattern"""
        self._events.append(event)

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...
