from typing import Generic, TypeVar, List
from pydantic import BaseModel, computed_field
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResponse(GenericModel, Generic[T]):
    data: List[T]
    page: int
    pages: int
    
    @computed_field
    @property
    def hasElements(self) -> bool:
        return len(self.data) > 0