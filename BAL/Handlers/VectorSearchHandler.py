from typing import List
from fastapi import HTTPException
from DAL.Repositories.VectorDbRepo import FetchDocuments
from DAL.Validators.VectorSearchParametersValidator import VectorSearchParameters
from Helpers.FinalScoreCalc import ScoreCalculator
from Models.DTOs.SearchDTO import DocumentResult

class VectorSearchService:
   @staticmethod
   async def SearchDocuments(params, model, getDb) -> List[DocumentResult]:
       try:
           embedding = model(params.query)[0][0]
           referenceCondition = ""
           if params.option == "webpages":
               referenceCondition = "AND d.reference LIKE '%.aspx'"
           elif params.option == "pdfs":
               referenceCondition = "AND d.reference NOT LIKE '%.aspx'"

           results = await FetchDocuments(getDb, embedding, referenceCondition)
           return VectorSearchService._ProcessResults(results)
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

   @staticmethod
   async def SearchVector(params, model, getDb) -> List[DocumentResult]:
       try:
           embedding = model.encode(params.query)
           referenceCondition = ""
           if params.option == "webpages":
               referenceCondition = "AND d.reference LIKE '%.aspx'"
           elif params.option == "pdfs":
               referenceCondition = "AND d.reference NOT LIKE '%.aspx'"

           results = await FetchDocuments(getDb, embedding.tolist(), referenceCondition)
           return VectorSearchService._ProcessResults(results)
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))

   @staticmethod
   def _ProcessResults(results) -> List[DocumentResult]:
       uniqueDocuments = {}
       for result in results:
           docId = result[3]
           if docId not in uniqueDocuments:
               uniqueDocuments[docId] = result

       documentResults = [
           DocumentResult(
               pageUrl=value[0],
               title=value[1],
               description=value[2],
               documentId=key,
               segmentNumber=value[4],
               finalScore=(85 * (1 - value[6])) + ScoreCalculator().CalculateScore(int(result[-1])) * 0.15,
               cosineSimilarity=(1 - value[6]),
               modifiedDate=value[5].strftime('%Y-%m-%d %H:%M:%S')
           )
           for key, value in uniqueDocuments.items()
       ]

       sortedResultList = sorted(documentResults, key=lambda x: x.finalScore, reverse=True)
       return sortedResultList