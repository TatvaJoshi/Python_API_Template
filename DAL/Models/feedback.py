from pydantic import BaseModel
from typing import List, Optional

class Feedback(BaseModel):
    user_query: str
    documents: List[str]
    search_type: str
    resultFound: bool
    feedback: int
    comment: Optional[str]
