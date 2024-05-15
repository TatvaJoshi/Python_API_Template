from fastapi import APIRouter
from DAL.Models.feedback import Feedback
from BAL.Services.feedback_service import FeedbackCollectionService

router = APIRouter(
    prefix="/feedback", tags=["feedback_collection"], responses={404: {"description": "Not found"}}
)

@router.post("/feedback_collection/")
async def receive_feedback(feedback: Feedback):
    """
    This endpoint is used to receive feedback from users about the model.
    The feedback is saved to the database and a success message is returned.

    Parameters:
        - feedback (Feedback): The feedback data received from the user.

    Returns:
        - dict: A dictionary with a success message.

    """
    # Write the feedback data to the database
    await FeedbackCollectionService.write_feedback(feedback.model_dump())
    return {"message": "Feedback received successfully"}
