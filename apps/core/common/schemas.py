from enum import Enum
from pydantic import BaseModel, Field


class SortEnum(str, Enum):
    DESC = "desc"
    ASC = "asc"


class PaginationBase(BaseModel):
    page: int = Field(1)
    limit: int = Field(10)

    def get_offset(self):
        return (self.page - 1) * self.limit
