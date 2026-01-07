from typing import TypeVar

from pydantic import BaseModel

from src.domain.common.entity import EntityId

from ..models.base import Base as SQLBaseModel

MODEL_T = TypeVar("MODEL_T", bound=SQLBaseModel)
ENTITY_T = TypeVar("ENTITY_T", bound=BaseModel)
ENTITY_ID_T = TypeVar("ENTITY_ID_T", bound=EntityId)
