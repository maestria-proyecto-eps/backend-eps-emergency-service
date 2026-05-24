from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import Response as RS
from fastapi import status

T = TypeVar("T")

class Response(GenericModel,Generic[T]):
    hasError: bool
    message: str
    data: Optional[T] = None

    @classmethod
    def ok(cls, data: T, message: str = "Operación exitosa") -> "Response[T]":
        return cls(hasError=False, message=message, data=data)

    @classmethod
    def error(cls, message: str) -> "Response[T]":
        return cls(hasError=True, message=message, data=None)
    
    def toHttpResponse(self, statusCode=status.HTTP_200_OK):
        if statusCode == status.HTTP_204_NO_CONTENT:
            return RS(status_code=statusCode)

        return JSONResponse(
            status_code=statusCode,
            content=jsonable_encoder(self)
        )