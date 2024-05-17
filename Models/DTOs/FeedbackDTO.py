from pydantic import BaseModel
from typing import List, Optional

class Feedback(BaseModel):
   userQuery: str
   documents: List[str]
   searchType: str
   resultFound: bool
   feedback: int
   comment: Optional[str]