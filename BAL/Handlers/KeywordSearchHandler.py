from DAL.Database.DbConnectionReranker import GetDbRerank
from typing import List
from DAL.Repositories.KeywordDbRepo import FetchKeywordSearchResults
from Models.DTOs.SearchDTO import SearchResult

class KeywordSearchService:
   @staticmethod
   async def PerformKeywordSearch(params) -> List[SearchResult]:
       results = await FetchKeywordSearchResults(params, GetDbRerank)
       jsonResults = [
           {
               "pageId": result[0],
               "reference": result[4],
               "title": result[1],
               "description": result[2],
               "lastModified": result[3].strftime('%Y-%m-%d %H:%M:%S'),
               "score": result[5]
           }
           for result in results
       ]
       searchResults = [SearchResult(**result) for result in jsonResults]
       return searchResults