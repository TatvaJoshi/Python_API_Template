from fastapi import HTTPException
import torch
import torch.nn.functional as F
from DAL.Database.db_connection_reranker import get_db_rerank
from DAL.Database.hybrid_db_operations import fetch_hybrid_results
from DAL.Models.search import HybridSearchResult

class HybridSearchService:
    @staticmethod
    async def perform_hybrid_search(params, model, reranker_model, reranker_tokenizer):
        try:    
            embedding = model.encode(params.query)

            reference_condition = ""
            if params.option == "webpages":
                reference_condition = "AND d.reference LIKE '%.aspx'"
            elif params.option == "pdfs":
                reference_condition = "AND d.reference NOT LIKE '%.aspx%'"

            results = await fetch_hybrid_results(params, get_db_rerank, embedding, reference_condition)
            if not results:
                return []

            unique_results = HybridSearchService._get_unique_results(results)

            reranker_model.eval()
            pairs = [(params.query, item[1]) for item in unique_results]
            with torch.no_grad():
                inputs = reranker_tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
                scores = reranker_model(**inputs, return_dict=True).logits.view(-1, ).float()
                probabilities = F.softmax(scores, dim=0)
                probabilities_list = probabilities.tolist()

            results_with_scores = HybridSearchService._process_results(unique_results, probabilities_list)
            sorted_results = sorted(results_with_scores, key=lambda x: x.score, reverse=True)
            return sorted_results
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    @staticmethod
    def _get_unique_results(results):
        unique_results = {}
        for result in results:
            if result[0] not in unique_results:
                unique_results[result[0]] = result
        return list(unique_results.values())

    @staticmethod
    def _process_results(results, probabilities_list):
        return [
            HybridSearchResult(
                id=record[0],
                reference=record[2],
                title=record[3],
                description=record[4],
                date=record[5].strftime('%Y-%m-%d %H:%M:%S'),
                score=score * 100
            )
            for record, score in zip(results, probabilities_list)
        ]