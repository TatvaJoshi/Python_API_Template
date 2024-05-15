from typing import List
from BAL.Dependencies.dependencies import get_model_dependency, get_rerank_tokenizer_dependency, get_reranker_model_dependency
from BAL.Services.hybrid_search_service import HybridSearchService
# from Helpers.globals import get_console_logger, get_file_logger
from fastapi import APIRouter, Depends,  HTTPException
# from fastapi_cache.decorator import cache
from DAL.Models.search import HybridSearchResult
from DAL.Models.api_response import APIResponse
from DAL.Validators.vector_search_parameters import VectorSearchParameters

router = APIRouter(
    prefix="/hsearch", tags=["hybrid_search"], responses={404: {"description": "Not found"}}
)

@router.get("/hybrid_search/", summary="Hybrid Search for documents in the document store", description="Hybrid Search for documents in the document store based on query vector and keywords. Returns a list of documents sorted by relevance to the query vector and keywords. The results are sorted by a score that combines the cosine similarity with the query vector and the relevance of the keywords.")
async def Hybrid_Search(params: VectorSearchParameters = Depends(), model: object = Depends(get_model_dependency),reranker_model:object=Depends(get_reranker_model_dependency),reranker_tokenizer:object=Depends(get_rerank_tokenizer_dependency)):
    try:
        json_results = await HybridSearchService.perform_hybrid_search(params, model, reranker_model, reranker_tokenizer)
        return APIResponse[List[HybridSearchResult]](isSuccess=True, response=json_results)
    except Exception as e:
        # get_console_logger().critical(e)
        # get_file_logger().critical(e)
        raise HTTPException(status_code=500, detail=str(e))
