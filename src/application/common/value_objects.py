from dataclasses import dataclass, field
from typing import Self

from src.domain.common.entity import UuidEntityId

MessageId = UuidEntityId


@dataclass(frozen=True)
class OutboxMessage:
    id: MessageId
    to: str
    send_type: str
    body: str
    subject: str | None = field(default=None)

    @classmethod
    def create(cls, to: str, send_type: str, body: str, subject: str | None = None) -> Self:
        return cls(id=MessageId(), to=to, send_type=send_type, body=body, subject=subject)
