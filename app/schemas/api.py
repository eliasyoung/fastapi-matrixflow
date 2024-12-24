from typing import  Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class CustomJSONResponse(BaseModel, Generic[T]):
    code: int
    data: T
