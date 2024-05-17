from fastapi import HTTPException
from pydantic import BaseModel, Field, validator
from typing import List, Optional

#TODO: Make HTTPexception handling more robust.
class VectorSearchParameters(BaseModel):
    query: str = Field(..., min_length=1)
    option: Optional[str] = Field('', max_length=20)

    @validator('option')
    def validate_option(cls, value):
        valid_options = ['webpages', 'pdfs', '']
        if value not in valid_options:
            error_details = {'errorCode': 400, 'errorDetails': f'Option must be one of {valid_options}'}
            raise HTTPException(status_code=400, detail=error_details)
        return value
