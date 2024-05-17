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
   def __init__(self, apiResponse: APIResponse):
       self.apiResponse = apiResponse
       super().__init__(status_code=apiResponse.errors.errorCode, detail=apiResponse.errors.errorDetails)