from abc import abstractmethod
from typing import Generic, TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema


class Entity(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


T = TypeVar("T")


class EntityId(Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T | None = None) -> None:
        if value is None:
            self._value = self._new()
        else:
            self._value = value

    @classmethod
    def _new(cls) -> T:
        raise NotImplementedError(f"{cls.__name__}._new() must be implemented or overridden")

    @property
    def value(self) -> T:
        return self._value

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and str(self.value) == str(other.value)

    def __hash__(self) -> int:
        return hash(self._value)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._value!r})"

    @classmethod
    @abstractmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: GetCoreSchemaHandler) -> CoreSchema: ...


class UuidEntityId(EntityId[UUID]):
    @classmethod
    def _new(cls) -> UUID:
        return uuid4()

    @property
    def hex(self) -> str:
        return self._value.hex

    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: GetCoreSchemaHandler) -> CoreSchema:
        # Создаем схему, которая принимает как UUID-совместимые значения,
        # так и уже существующие экземпляры UuidEntityId
        from_uuid_schema = core_schema.chain_schema(
            [
                core_schema.uuid_schema(),
                core_schema.with_info_after_validator_function(lambda v, i: cls(v), core_schema.any_schema()),
            ]
        )

        # Схема для существующих экземпляров
        instance_schema = core_schema.is_instance_schema(cls)

        # Объединяем обе схемы
        return core_schema.union_schema(
            [instance_schema, from_uuid_schema],
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance.value),
                return_schema=core_schema.str_schema(),
            ),
        )
