from typing import List
from BAL.Dependencies.Dependencies import GetModelDependency, GetRerankTokenizerDependency, GetRerankerModelDependency
from BAL.Handlers.HybridSearchHandler import HybridSearchService
# from Helpers.globals import get_console_logger, get_file_logger
from fastapi import APIRouter, Depends,  HTTPException
# from fastapi_cache.decorator import cache
from DAL.Validators.VectorSearchParametersValidator import VectorSearchParameters
from Models.DTOs.SearchDTO import HybridSearchResult
from Models.RequestFeatures.ApiResponse import APIResponse

router = APIRouter(
    prefix="/hsearch", tags=["hybrid_search"], responses={404: {"description": "Not found"}}
)

@router.get("/hybrid_search/", summary="Hybrid Search for documents in the document store", description="Hybrid Search for documents in the document store based on query vector and keywords. Returns a list of documents sorted by relevance to the query vector and keywords. The results are sorted by a score that combines the cosine similarity with the query vector and the relevance of the keywords.")
async def HybridSearch(params: VectorSearchParameters = Depends(), model: object = Depends(GetModelDependency),rerankerModel:object=Depends(GetRerankerModelDependency),rerankerTokenizer:object=Depends(GetRerankTokenizerDependency)):
    try:
        json_results = await HybridSearchService.PerformHybridSearch(params, model, rerankerModel, rerankerTokenizer)
        return APIResponse[List[HybridSearchResult]](isSuccess=True, response=json_results)
    except Exception as e:
        # get_console_logger().critical(e)
        # get_file_logger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))
