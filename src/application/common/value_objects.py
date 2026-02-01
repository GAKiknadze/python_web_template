from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Self

from src.domain.common.entity import UuidEntityId

EventId = UuidEntityId


class EventType(str, Enum):
    """Типы событий для outbox pattern"""

    MESSAGE = "message"  # Сообщение пользователю (email, sms и т.д.)
    USER_ACTION = "user_action"  # Действие пользователя
    AUDIT_LOG = "audit_log"  # Лог действий для аудита
    NOTIFICATION = "notification"  # Уведомление
    WEBHOOK = "webhook"  # Webhook событие
    CUSTOM = "custom"  # Пользовательское событие


@dataclass(frozen=True)
class OutboxEvent:
    """Базовый класс для всех событий в outbox pattern"""

    id: EventId
    event_type: EventType
    payload: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        event_type: EventType,
        payload: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> Self:
        return cls(
            id=EventId(),
            event_type=event_type,
            payload=payload,
            metadata=metadata or {},
        )

    @classmethod
    def create_message(
        cls,
        to: str,
        send_type: str,
        body: str,
        subject: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Self:
        """Создает событие для отправки сообщения (email, sms и т.д.)"""
        payload = {
            "to": to,
            "send_type": send_type,
            "body": body,
            "subject": subject,
        }
        return cls.create(
            event_type=EventType.MESSAGE,
            payload=payload,
            metadata=metadata or {},
        )

    @classmethod
    def create_user_action(
        cls,
        user_id: str,
        action: str,
        resource: str | None = None,
        details: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Self:
        """Создает событие для записи действия пользователя"""
        payload = {
            "user_id": user_id,
            "action": action,
            "resource": resource,
            "details": details or {},
        }
        return cls.create(
            event_type=EventType.USER_ACTION,
            payload=payload,
            metadata=metadata or {},
        )

    @classmethod
    def create_audit_log(
        cls,
        entity_type: str,
        entity_id: str,
        operation: str,
        user_id: str | None = None,
        changes: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Self:
        """Создает событие для аудит лога"""
        payload = {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "operation": operation,
            "user_id": user_id,
            "changes": changes or {},
        }
        return cls.create(
            event_type=EventType.AUDIT_LOG,
            payload=payload,
            metadata=metadata or {},
        )

    @classmethod
    def create_webhook(
        cls,
        url: str,
        method: str = "POST",
        headers: dict[str, str] | None = None,
        body: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Self:
        """Создает событие для отправки webhook"""
        payload = {
            "url": url,
            "method": method,
            "headers": headers or {},
            "body": body or {},
        }
        return cls.create(
            event_type=EventType.WEBHOOK,
            payload=payload,
            metadata=metadata or {},
        )

    @classmethod
    def create_notification(
        cls,
        user_id: str,
        title: str,
        message: str,
        notification_type: str = "info",
        link: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Self:
        """Создает событие для отправки уведомления"""
        payload = {
            "user_id": user_id,
            "title": title,
            "message": message,
            "notification_type": notification_type,
            "link": link,
        }
        return cls.create(
            event_type=EventType.NOTIFICATION,
            payload=payload,
            metadata=metadata or {},
        )
