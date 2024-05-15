from BAL.Dependencies.dependencies import get_model_dependency, get_model_fast_dependency
from BAL.Services.vector_search_service import VectorSearchService
from DAL.Models.api_response import APIResponse, ErrorDetails
from DAL.Models.search import DocumentResult
from DAL.Validators.vector_search_parameters import VectorSearchParameters
from DAL.Database.db_connection import get_db
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
# from redis import asyncio as aioredis
from Helpers.config_logger import LoggerFactory
router = APIRouter(
    prefix="/search", tags=["search"], responses={404: {"description": "Not found"}}
)
router.file_console_logger = LoggerFactory().setup_file_console_logger()

@router.get("/vector_search/", summary="Search for documents in the document store", description="Search for documents in the document store based on query vector. Returns a list of documents sorted by cosine similarity with the query vector.")
async def vector_search(params: VectorSearchParameters = Depends(), model: object = Depends(get_model_dependency)):
    try:
        sorted_result_list = await VectorSearchService.search_vector(params, model, get_db)
        return APIResponse[List[DocumentResult]](isSuccess=True, response=sorted_result_list)
    except Exception as e:
        router.file_console_logger.info(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vector_search_fast/", summary="Search for documents in the document store with fast model", description="Search for documents in the document store based on query vector. Returns a list of documents sorted by cosine similarity with the query vector. This operation uses a faster model and the results are as accurate as the `vector_search` endpoint.")
async def vector_search_fast(params: VectorSearchParameters = Depends(), model: object = Depends(get_model_fast_dependency)):
    try:
        sorted_result_list = await VectorSearchService.search_documents(params, model, get_db)
        return APIResponse[List[DocumentResult]](isSuccess=True, response=sorted_result_list)
    except HTTPException as e:
        router.file_console_logger.info(e)
        error_details = ErrorDetails(errorCode=e.status_code, errorDetails=e.detail)
        return APIResponse[List[DocumentResult]](isSuccess=False, response=None, errors=error_details)
