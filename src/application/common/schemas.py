from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, TypeVar, Generic


class BaseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

class PaginationRequest(BaseSchema):
    limit: Literal[25, 50, 100] = Field(default=25)
    offset: int = Field(default=0, ge=0)


D_T = TypeVar("D_T")
F_T = TypeVar("F_T", bound="PaginationRequest")


class PaginationResponse(BaseSchema, Generic[D_T, F_T]):
    data: list[D_T]
    filters: F_T
    count: int
