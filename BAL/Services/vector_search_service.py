from typing import List
from fastapi import HTTPException
from DAL.Database.vector_db_operations import fetch_documents
from Helpers.globals import get_model
from Helpers.final_score_calc import calculate_score
from DAL.Models.search import DocumentResult
from DAL.Validators.vector_search_parameters import VectorSearchParameters

class VectorSearchService:
    @staticmethod
    async def search_documents(params, model, get_db) -> List[DocumentResult]:
        try:
            # Encode the user query
            embedding = model(params.query)[0][0]

            # Connect to the database
            reference_condition = ""
            if params.option == "webpages":
                reference_condition = "AND d.reference LIKE '%.aspx'"
            elif params.option == "pdfs":
                reference_condition = "AND d.reference NOT LIKE '%.aspx'"
                
            # Fetch documents from the database db script.
            results = await fetch_documents(get_db, embedding, reference_condition)

            return VectorSearchService._process_results(results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def search_vector(params, model, get_db)-> List[DocumentResult]:
        try:
            embedding = model.encode(params.query)

            reference_condition = ""
            if params.option == "webpages":
                reference_condition = "AND d.reference LIKE '%.aspx'"
            elif params.option == "pdfs":
                reference_condition = "AND d.reference NOT LIKE '%.aspx'"

            results = await fetch_documents(get_db, embedding.tolist(), reference_condition)

            return VectorSearchService._process_results(results)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
    @staticmethod
    def _process_results(results) -> List[DocumentResult]:
        unique_documents = {}
        for result in results:
            doc_id = result[3]
            if doc_id not in unique_documents:
                unique_documents[doc_id] = result

        document_results = [
            DocumentResult(
                page_url=value[0],
                Title=value[1],
                Description=value[2],
                document_id=key,
                segment_number=value[4],
                Final_Score=(85 * (1 - value[6])) + calculate_score(int(result[-1])) * 0.15,
                cosine_similarity=(1 - value[6]),
                Modified_Date=value[5].strftime('%Y-%m-%d %H:%M:%S')
            )
            for key, value in unique_documents.items()
        ]

        sorted_result_list = sorted(document_results, key=lambda x: x.Final_Score, reverse=True)
        return sorted_result_list