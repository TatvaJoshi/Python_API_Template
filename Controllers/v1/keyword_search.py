from fastapi import APIRouter, Depends, HTTPException, Request, Query
from typing import List
from DAL.Models.search import SearchResult
from DAL.Models.api_response import APIResponse
from DAL.Validators.vector_search_parameters import VectorSearchParameters
# from Helpers.globals import get_console_logger, get_file_logger
from BAL.Services.keyword_search_service import KeywordSearchService

router = APIRouter(
    prefix="/ksearch", tags=["keyword_search"], responses={404: {"description": "Not found"}}
)

@router.get("/keyword_search/", summary="Search for documents in the document store based on keywords", description="Search for documents in the document store based on query keywords. Returns a list of documents sorted by relevance to the query keywords.")
async def Keyword_Search(params: VectorSearchParameters = Depends()):
    try:
        json_results = await KeywordSearchService.perform_keyword_search(params)
        return APIResponse[List[SearchResult]](isSuccess=True, response=json_results)
    except Exception as e:
        router.file_console_logger.info("Sdsds")

        raise HTTPException(status_code=500, detail=str(e))
