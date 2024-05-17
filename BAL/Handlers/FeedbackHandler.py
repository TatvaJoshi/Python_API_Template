import json
from datetime import datetime
from DAL.Repositories.FeedbackDbRepo import WriteFeedbackToDb
from Helpers.TimeMeasure import TimerContextManager
from DAL.Database.DbConnection import GetDb
from typing import List, Optional


class FeedbackCollectionService:
    @staticmethod
    async def WriteFeedback(data):
        with TimerContextManager("Feedback Insert took"):
            await WriteFeedbackToDb(data, GetDb)
