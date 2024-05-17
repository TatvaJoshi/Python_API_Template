from typing import List, Tuple

async def FetchDocuments(getDb, embedding, referenceCondition) -> List[Tuple]:
    query = f"""
    SELECT d.reference, d.title, d.description, e.ahs_ca_documents, e.segment_number, d.last_modified, (embedding <=> $1) as cosine_similarity, d.elapsed_days
    FROM ahs_ca_tokenized_embeddings_gte e
    LEFT JOIN ahs_ca_documents d ON d.id = e.ahs_ca_documents
    WHERE 1=1 {referenceCondition}
    ORDER BY cosine_similarity LIMIT 40;
    """
    async with getDb() as conn:
        results = await conn.fetch(query, str(embedding))
    return results