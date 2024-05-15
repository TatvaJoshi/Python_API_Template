from typing import List, Tuple

async def fetch_hybrid_results(params, get_db, embedding, reference_condition) -> List[Tuple]:
    query1 = f"""
    (
        SELECT e.ahs_ca_documents, e.chunk, d.reference, d.title, d.description, d.last_modified
        FROM ahs_ca_tokenized_embeddings_gte e
        LEFT JOIN ahs_ca_documents d ON d.id = e.ahs_ca_documents
        WHERE 1=1 {reference_condition}
        ORDER BY embedding <=> '{embedding.tolist()}' LIMIT 10
    )
    UNION
    (
        SELECT e.ahs_ca_documents, e.chunk, d.reference, d.title, d.description, d.last_modified
        FROM ahs_ca_tokenized_embeddings_gte e
        LEFT JOIN ahs_ca_documents d ON d.id = e.ahs_ca_documents
        WHERE document_with_idx @@ plainto_tsquery('{params.query}') {reference_condition}
        ORDER BY ts_rank(document_with_idx, plainto_tsquery('{params.query}')) DESC LIMIT 10
    );
    """
    async with get_db() as conn:
        results = await conn.fetch(query1)
    return results