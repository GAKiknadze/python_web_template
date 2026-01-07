from .types import ENTITY_T, ENTITY_ID_T
from typing import Generic, Any
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class SaveMethodMixin(Generic[ENTITY_T], ABC):
    _session: AsyncSession
    
    @abstractmethod
    def entity_to_model(self, entity: ENTITY_T) -> Any: ...
    
    @abstractmethod
    def model_to_entity(self, model: Any) -> ENTITY_T: ...
    
    async def save(self, value: ENTITY_T) -> ENTITY_T:
        model = self.entity_to_model(value)
        merged_model = await self._session.merge(model)
        await self._session.flush()
        await self._session.refresh(merged_model)
        return self.model_to_entity(merged_model)


class GetByIdMethodMixin(Generic[ENTITY_T, ENTITY_ID_T], ABC):
    _session: AsyncSession
    _model_cls: type
    
    @abstractmethod
    def model_to_entity(self, model: Any) -> ENTITY_T: ...
    
    async def get_by_id(self, value: ENTITY_ID_T) -> ENTITY_T | None:
        model = await self._session.get(self._model_cls, value)
        return self.model_to_entity(model) if model else None


class DeleteByIdMethodMixin(Generic[ENTITY_T, ENTITY_ID_T], ABC):
    _session: AsyncSession
    _model_cls: type
    
    async def delete_by_id(self, value: ENTITY_ID_T) -> None:
        model = await self._session.get(self._model_cls, value)
        if model is None:
            return
        await self._session.delete(model)
