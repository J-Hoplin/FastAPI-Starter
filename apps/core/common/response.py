from typing import Generic, List, TypeVar
from pydantic import BaseModel


# Paginated Response Base
# Define Pydantic Model for list item model
T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    total: int
    items: List[T]
