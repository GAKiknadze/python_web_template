from typing import Protocol


class SaveMethod[ENTITY_ID](Protocol):
    async def save(self, value: ENTITY_ID) -> ENTITY_ID: ...


class GetByIdMethodMixin[ENTITY_T, ENTITY_ID_T](Protocol):
    async def get_by_id(self, value: ENTITY_ID_T) -> ENTITY_T | None: ...


class DeleteByIdMethodMixin[ENTITY_ID](Protocol):
    async def delete_by_id(self, value: ENTITY_ID) -> None: ...


class SoftDeleteByIdMethodMixin[ENTITY_ID](Protocol):
    async def soft_delete_by_id(self, value: ENTITY_ID) -> None: ...
