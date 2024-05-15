from typing import Generic, TypeVar, Union

from fastapi import HTTPException
from pydantic import BaseModel

T = TypeVar("T")


class ErrorDetails(BaseModel):
    errorCode: int
    errorDetails: str


class APIResponse(BaseModel, Generic[T]):
    isSuccess: bool
    response: Union[T, None] = None
    errors: Union[ErrorDetails, None] = None


class CustomHTTPException(HTTPException):
    def __init__(self, api_response: APIResponse):
        self.api_response = api_response
        super().__init__(status_code=api_response.errors.errorCode, detail=api_response.errors.errorDetails)