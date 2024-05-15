from pydantic import BaseModel
from typing import Union,Optional
class DocumentResult(BaseModel):
    page_url: Optional[str]
    Title: Optional[str]
    Description: Optional[str]
    document_id: Union[str, int]
    segment_number: int
    Final_Score: float
    cosine_similarity: float
    Modified_Date: str

class SearchResult(BaseModel):
    Page_ID: int
    Reference: Optional[str]
    Title: Optional[str]
    Description: Optional[str]
    Last_modified: Optional[str]
    score: float

class HybridSearchResult(BaseModel):
    id: int
    reference: Optional[str]
    title: Optional[str]
    description: Optional[str]
    date: Optional[str]
    score: float