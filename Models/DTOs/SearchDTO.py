from pydantic import BaseModel
from typing import Union, Optional

class DocumentResult(BaseModel):
   pageUrl: Optional[str]
   title: Optional[str]
   description: Optional[str]
   documentId: Union[str, int]
   segmentNumber: int
   finalScore: float
   cosineSimilarity: float
   modifiedDate: str

class SearchResult(BaseModel):
   pageId: int
   reference: Optional[str]
   title: Optional[str]
   description: Optional[str]
   lastModified: Optional[str]
   score: float

class HybridSearchResult(BaseModel):
   id: int
   reference: Optional[str]
   title: Optional[str]
   description: Optional[str]
   date: Optional[str]
   score: float