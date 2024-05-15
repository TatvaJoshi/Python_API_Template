import json
from datetime import datetime
from DAL.Database.feedback_db_operations import write_feedback_to_db
from Helpers.time_measure import TimerContextManager
from DAL.Database.db_connection import get_db
from typing import List, Optional


class FeedbackCollectionService:
    @staticmethod
    async def write_feedback(data):
        with TimerContextManager("Feedback Insert took"):
            await write_feedback_to_db(data, get_db)
