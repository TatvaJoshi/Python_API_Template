from DAL.Database.db_connection_reranker import get_db_rerank
from typing import List
from DAL.Database.keyword_db_operations import fetch_keyword_search_results
from DAL.Models.search import SearchResult

class KeywordSearchService:
    @staticmethod
    async def perform_keyword_search(params) -> List[SearchResult]:
        results = await fetch_keyword_search_results(params, get_db_rerank)
        json_results = [
            {
                "Page_ID": result[0],
                "Reference": result[4],
                "Title": result[1],
                "Description": result[2],
                "Last_modified": result[3].strftime('%Y-%m-%d %H:%M:%S'),
                "score": result[5]
            }
            for result in results
        ]
        search_results = [SearchResult(**result) for result in json_results]
        return search_results
