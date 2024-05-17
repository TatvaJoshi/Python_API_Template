from fastapi import APIRouter
from BAL.Handlers.FeedbackHandler import FeedbackCollectionService
from Models.DTOs.FeedbackDTO import Feedback

router = APIRouter(
    prefix="/feedback", tags=["feedback_collection"], responses={404: {"description": "Not found"}}
)

@router.post("/feedback_collection/")
async def ReceiveFeedback(feedback: Feedback):
    """
    This endpoint is used to receive feedback from users about the model.
    The feedback is saved to the database and a success message is returned.

    Parameters:
        - feedback (Feedback): The feedback data received from the user.

    Returns:
        - dict: A dictionary with a success message.

    """
    # Write the feedback data to the database
    await FeedbackCollectionService.WriteFeedback(feedback.model_dump())
    return {"message": "Feedback received successfully"}
