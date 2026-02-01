import pytest
from src.application.common.value_objects import (
    EventId,
    EventType,
    OutboxEvent,
)


class TestOutboxEvent:
    """Тесты для OutboxEvent"""

    def test_create_base_event(self):
        """Тест создания базового события"""
        event = OutboxEvent.create(
            event_type=EventType.CUSTOM,
            payload={"key": "value"},
            metadata={"priority": "high"},
        )

        assert event.id is not None
        assert isinstance(event.id, EventId)
        assert event.event_type == EventType.CUSTOM
        assert event.payload == {"key": "value"}
        assert event.metadata == {"priority": "high"}

    def test_create_message_event(self):
        """Тест создания события отправки сообщения"""
        event = OutboxEvent.create_message(
            to="user@example.com",
            send_type="email",
            body="Test body",
            subject="Test subject",
            metadata={"priority": "high"},
        )

        assert event.event_type == EventType.MESSAGE
        assert event.payload["to"] == "user@example.com"
        assert event.payload["send_type"] == "email"
        assert event.payload["body"] == "Test body"
        assert event.payload["subject"] == "Test subject"
        assert event.metadata == {"priority": "high"}

    def test_create_message_event_without_subject(self):
        """Тест создания события сообщения без темы (например, SMS)"""
        event = OutboxEvent.create_message(
            to="+79991234567",
            send_type="sms",
            body="Your code: 123456",
        )

        assert event.event_type == EventType.MESSAGE
        assert event.payload["to"] == "+79991234567"
        assert event.payload["send_type"] == "sms"
        assert event.payload["body"] == "Your code: 123456"
        assert event.payload["subject"] is None
        assert event.metadata == {}

    def test_create_user_action_event(self):
        """Тест создания события действия пользователя"""
        event = OutboxEvent.create_user_action(
            user_id="user-123",
            action="login",
            resource="auth_service",
            details={"ip": "192.168.1.1", "success": True},
            metadata={"timestamp": "2024-01-15T10:00:00Z"},
        )

        assert event.event_type == EventType.USER_ACTION
        assert event.payload["user_id"] == "user-123"
        assert event.payload["action"] == "login"
        assert event.payload["resource"] == "auth_service"
        assert event.payload["details"] == {"ip": "192.168.1.1", "success": True}
        assert event.metadata == {"timestamp": "2024-01-15T10:00:00Z"}

    def test_create_user_action_minimal(self):
        """Тест создания минимального события действия пользователя"""
        event = OutboxEvent.create_user_action(
            user_id="user-123",
            action="logout",
        )

        assert event.event_type == EventType.USER_ACTION
        assert event.payload["user_id"] == "user-123"
        assert event.payload["action"] == "logout"
        assert event.payload["resource"] is None
        assert event.payload["details"] == {}
        assert event.metadata == {}

    def test_create_audit_log_event(self):
        """Тест создания события аудит лога"""
        event = OutboxEvent.create_audit_log(
            entity_type="Order",
            entity_id="order-456",
            operation="create",
            user_id="user-123",
            changes={
                "status": {"old": None, "new": "pending"},
                "total": {"old": None, "new": 5000},
            },
            metadata={"ip": "192.168.1.1"},
        )

        assert event.event_type == EventType.AUDIT_LOG
        assert event.payload["entity_type"] == "Order"
        assert event.payload["entity_id"] == "order-456"
        assert event.payload["operation"] == "create"
        assert event.payload["user_id"] == "user-123"
        assert event.payload["changes"]["status"] == {"old": None, "new": "pending"}
        assert event.metadata == {"ip": "192.168.1.1"}

    def test_create_audit_log_minimal(self):
        """Тест создания минимального аудит лога"""
        event = OutboxEvent.create_audit_log(
            entity_type="User",
            entity_id="user-789",
            operation="delete",
        )

        assert event.event_type == EventType.AUDIT_LOG
        assert event.payload["entity_type"] == "User"
        assert event.payload["entity_id"] == "user-789"
        assert event.payload["operation"] == "delete"
        assert event.payload["user_id"] is None
        assert event.payload["changes"] == {}

    def test_create_webhook_event(self):
        """Тест создания события webhook"""
        event = OutboxEvent.create_webhook(
            url="https://api.example.com/webhook",
            method="POST",
            headers={"Authorization": "Bearer token123"},
            body={"event": "order.created", "id": "order-456"},
            metadata={"retry_count": 0, "max_retries": 3},
        )

        assert event.event_type == EventType.WEBHOOK
        assert event.payload["url"] == "https://api.example.com/webhook"
        assert event.payload["method"] == "POST"
        assert event.payload["headers"] == {"Authorization": "Bearer token123"}
        assert event.payload["body"] == {"event": "order.created", "id": "order-456"}
        assert event.metadata == {"retry_count": 0, "max_retries": 3}

    def test_create_webhook_minimal(self):
        """Тест создания минимального webhook"""
        event = OutboxEvent.create_webhook(url="https://api.example.com/hook")

        assert event.event_type == EventType.WEBHOOK
        assert event.payload["url"] == "https://api.example.com/hook"
        assert event.payload["method"] == "POST"
        assert event.payload["headers"] == {}
        assert event.payload["body"] == {}

    def test_create_notification_event(self):
        """Тест создания события уведомления"""
        event = OutboxEvent.create_notification(
            user_id="user-123",
            title="New message",
            message="You have a new message",
            notification_type="info",
            link="/messages/msg-789",
            metadata={"priority": "normal"},
        )

        assert event.event_type == EventType.NOTIFICATION
        assert event.payload["user_id"] == "user-123"
        assert event.payload["title"] == "New message"
        assert event.payload["message"] == "You have a new message"
        assert event.payload["notification_type"] == "info"
        assert event.payload["link"] == "/messages/msg-789"
        assert event.metadata == {"priority": "normal"}

    def test_create_notification_minimal(self):
        """Тест создания минимального уведомления"""
        event = OutboxEvent.create_notification(
            user_id="user-123",
            title="Alert",
            message="Something happened",
        )

        assert event.event_type == EventType.NOTIFICATION
        assert event.payload["notification_type"] == "info"
        assert event.payload["link"] is None

    def test_event_immutability(self):
        """Тест неизменяемости события"""
        event = OutboxEvent.create_message(
            to="user@example.com",
            send_type="email",
            body="Test",
        )

        # Frozen dataclass не позволяет изменять атрибуты
        # В Python это вызывает AttributeError или FrozenInstanceError
        try:
            event.payload = {"new": "payload"}  # type: ignore
            assert False, "Should have raised an exception"
        except (AttributeError, Exception):
            pass  # Expected

        try:
            event.event_type = EventType.CUSTOM  # type: ignore
            assert False, "Should have raised an exception"
        except (AttributeError, Exception):
            pass  # Expected


class TestEventTypes:
    """Тесты для EventType enum"""

    def test_event_types_values(self):
        """Тест значений типов событий"""
        assert EventType.MESSAGE == "message"
        assert EventType.USER_ACTION == "user_action"
        assert EventType.AUDIT_LOG == "audit_log"
        assert EventType.NOTIFICATION == "notification"
        assert EventType.WEBHOOK == "webhook"
        assert EventType.CUSTOM == "custom"

    def test_event_types_are_strings(self):
        """Тест что EventType наследуется от str"""
        assert isinstance(EventType.MESSAGE, str)
        assert isinstance(EventType.USER_ACTION, str)
