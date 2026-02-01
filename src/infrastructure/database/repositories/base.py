from typing import Generic, get_args, get_origin

from sqlalchemy.ext.asyncio import AsyncSession

from .types import ENTITY_T, MODEL_T


class BaseRepository(Generic[MODEL_T, ENTITY_T]):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._model_cls = self._get_concrete_type(0)
        self._entity_cls = self._get_concrete_type(1)

    def _get_concrete_type(self, index: int) -> type:
        # Проходим по MRO, чтобы найти первый Generic-базовый класс с параметрами
        for base in getattr(self.__class__, "__orig_bases__", ()):
            origin = get_origin(base)
            if origin is not None and issubclass(origin, BaseRepository):
                args = get_args(base)
                if len(args) == 2:
                    return args[index]
        raise TypeError(
            "Cannot determine concrete types. "
            "Make sure your repository subclass inherits from BaseRepository[Model, Entity]."
        )

    def model_to_entity(self, value: MODEL_T) -> ENTITY_T:
        return self._entity_cls.model_validate(value, from_attributes=True)

    def entity_to_model(self, value: ENTITY_T) -> MODEL_T:
        data = value.model_dump()
        return self._model_cls(**data)
