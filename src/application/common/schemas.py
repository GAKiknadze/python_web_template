from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class PaginationRequest(BaseSchema):
    limit: Literal[25, 50, 100] = Field(default=25)
    offset: int = Field(default=0, ge=0)


class PaginationResponse[D_T, F_T: PaginationRequest](BaseSchema):
    data: list[D_T]
    filters: F_T
    count: int
