from fastapi import HTTPException
import torch
import torch.nn.functional as F
from DAL.Database.DbConnectionReranker import GetDbRerank
from DAL.Repositories.HybridDbRepo import FetchHybridResults
from Models.DTOs.SearchDTO import HybridSearchResult

class HybridSearchService:
   @staticmethod
   async def PerformHybridSearch(params, model, rerankerModel, rerankerTokenizer):
       try:
           embedding = model.encode(params.query)
           referenceCondition = ""
           if params.option == "webpages":
               referenceCondition = "AND d.reference LIKE '%.aspx'"
           elif params.option == "pdfs":
               referenceCondition = "AND d.reference NOT LIKE '%.aspx%'"

           results = await FetchHybridResults(params, GetDbRerank, embedding, referenceCondition)
           if not results:
               return []

           uniqueResults = HybridSearchService._GetUniqueResults(results)
           rerankerModel.eval()
           pairs = [(params.query, item[1]) for item in uniqueResults]

           with torch.no_grad():
               inputs = rerankerTokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
               scores = rerankerModel(**inputs, return_dict=True).logits.view(-1, ).float()
               probabilities = F.softmax(scores, dim=0)
               probabilitiesList = probabilities.tolist()

           resultsWithScores = HybridSearchService._ProcessResults(uniqueResults, probabilitiesList)
           sortedResults = sorted(resultsWithScores, key=lambda x: x.score, reverse=True)
           return sortedResults
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

   @staticmethod
   def _GetUniqueResults(results):
       uniqueResults = {}
       for result in results:
           if result[0] not in uniqueResults:
               uniqueResults[result[0]] = result
       return list(uniqueResults.values())

   @staticmethod
   def _ProcessResults(results, probabilitiesList):
       return [
           HybridSearchResult(
               id=record[0],
               reference=record[2],
               title=record[3],
               description=record[4],
               date=record[5].strftime('%Y-%m-%d %H:%M:%S'),
               score=score * 100
           )
           for record, score in zip(results, probabilitiesList)
       ]