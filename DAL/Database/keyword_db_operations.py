from typing import List, Tuple

async def fetch_keyword_search_results(params, get_db) -> List[Tuple]:
    reference_condition = ""
    if params.option == "webpages":
        reference_condition = "AND reference LIKE '%.aspx'"
    elif params.option == "pdfs":
        reference_condition = "AND reference NOT LIKE '%.aspx'"

    query = f"""
        SELECT id, title, description, last_modified, reference, ts_rank(document_with_idx_mutli_column, plainto_tsquery('{params.query}'))
        FROM ahs_ca_documents
        WHERE document_with_idx_mutli_column @@ plainto_tsquery('{params.query}') {reference_condition}
        ORDER BY ts_rank(document_with_idx_mutli_column, plainto_tsquery('{params.query}')) DESC
        LIMIT 20;
    """
    async with get_db() as conn:
        results = await conn.fetch(query)
    return results