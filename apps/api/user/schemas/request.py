from typing import Optional
from pydantic import Field, BaseModel, EmailStr
from apps.core.common.schemas import PaginationBase, SortEnum


class ListUserFilter(PaginationBase):
    name: Optional[str] = Field(None, description="Partial Search")
    email: Optional[str] = Field(None, description="Partial Search")
    is_active: Optional[bool] = Field(True, description="Check active user or not")
    sort: Optional[SortEnum] = Field(
        SortEnum.ASC, description="Ascending or Descending"
    )


class CreateUser(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
