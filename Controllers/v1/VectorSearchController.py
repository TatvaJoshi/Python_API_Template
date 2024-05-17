from BAL.Dependencies.Dependencies import GetModelDependency, GetModelFastDependency
from BAL.Handlers.VectorSearchHandler import VectorSearchService
from DAL.Validators.VectorSearchParametersValidator import VectorSearchParameters
from DAL.Database.DbConnection import GetDb
from fastapi import APIRouter, Depends, HTTPException
from typing import Any, List, Dict
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from fastapi_cache.decorator import cache
# from redis import asyncio as aioredis
from Helpers.ConfigLogger import LoggerFactory
from Models.DTOs.SearchDTO import DocumentResult
from Models.RequestFeatures.ApiResponse import APIResponse, ErrorDetails
router = APIRouter(
    prefix="/search", tags=["search"], responses={404: {"description": "Not found"}}
)
# router.file_console_logger = LoggerFactory().setup_file_console_logger()

@router.get("/vector_search/", summary="Search for documents in the document store", description="Search for documents in the document store based on query vector. Returns a list of documents sorted by cosine similarity with the query vector.")
async def VectorSearch(params: VectorSearchParameters = Depends(), model: object = Depends(GetModelDependency),logger:Any=Depends(LoggerFactory().SetupFileConsoleLogger)):
    try:
        sorted_result_list = await VectorSearchService.SearchVector(params, model, GetDb)
        return APIResponse[List[DocumentResult]](isSuccess=True, response=sorted_result_list)
    except Exception as e:
        logger.debug(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vector_search_fast/", summary="Search for documents in the document store with fast model", description="Search for documents in the document store based on query vector. Returns a list of documents sorted by cosine similarity with the query vector. This operation uses a faster model and the results are as accurate as the `vector_search` endpoint.")
async def vector_search_fast(params: VectorSearchParameters = Depends(), model: object = Depends(GetModelFastDependency),logger:Any=Depends(LoggerFactory().SetupFileConsoleLogger)):
    try:
        sorted_result_list = await VectorSearchService.SearchDocuments(params, model, GetDb)
        return APIResponse[List[DocumentResult]](isSuccess=True, response=sorted_result_list)
    except HTTPException as e:
        logger.debug(e)
        error_details = ErrorDetails(errorCode=e.status_code, errorDetails=e.detail)
        return APIResponse[List[DocumentResult]](isSuccess=False, response=None, errors=error_details)
