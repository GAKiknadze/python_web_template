from typing import Any, Self
from uuid import UUID

from sqlalchemy import UUID as SA_UUID
from sqlalchemy import TypeDecorator

from src.domain.common.entity import UuidEntityId


class UuidEntityIdType(TypeDecorator):
    impl = SA_UUID
    cache_ok = True

    def __init__(self, entity_id_class: type[UuidEntityId]):
        super().__init__()
        self.entity_id_class = entity_id_class

    def process_bind_param(self, value: Any, dialect: Any) -> UUID | None:
        if value is None:
            return None

        if isinstance(value, UuidEntityId):
            return value.value

        if isinstance(value, UUID):
            return value

        if isinstance(value, str):
            return UUID(value)

        raise ValueError(f"Unsupported type for UuidEntityId: {type(value)}")

    def process_result_value(self, value: Any, dialect: Any) -> UuidEntityId | None:
        if value is None:
            return None

        if isinstance(value, UUID):
            return self.entity_id_class(value)

        if isinstance(value, str):
            return self.entity_id_class(UUID(value))

        raise ValueError(f"Unsupported database value type: {type(value)}")

    def copy(self, **kw: Any) -> Self:
        kw.setdefault("entity_id_class", self.entity_id_class)
        return super().copy(**kw)

    @property
    def python_type(self):
        return self.entity_id_class
