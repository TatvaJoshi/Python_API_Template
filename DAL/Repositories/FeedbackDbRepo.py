from datetime import datetime
import json

async def WriteFeedbackToDb(data, getDb):
    query = """
        INSERT INTO user_feedback (user_query, results, search_type, result_found, feedback, comment, timestamp)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
    """
    async with getDb() as conn:
        await conn.execute(
            query,
            data['user_query'],
            json.dumps(data['documents']),
            data['search_type'],
            data['resultFound'],
            data['feedback'],
            data['comment'],
            datetime.now()
        )