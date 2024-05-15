from typing import List, Tuple

async def fetch_documents(get_db, embedding, reference_condition) -> List[Tuple]:
    query = f"""
    SELECT d.reference, d.title, d.description, e.ahs_ca_documents, e.segment_number, d.last_modified, (embedding <=> $1) as cosine_similarity, d.elapsed_days
    FROM ahs_ca_tokenized_embeddings_gte e
    LEFT JOIN ahs_ca_documents d ON d.id = e.ahs_ca_documents
    WHERE 1=1 {reference_condition}
    ORDER BY cosine_similarity LIMIT 40;
    """
    async with get_db() as conn:
        results = await conn.fetch(query, str(embedding))
    return results