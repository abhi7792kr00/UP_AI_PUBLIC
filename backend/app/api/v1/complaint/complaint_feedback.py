from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.dependencies.current_user import (
    get_current_user,
)

from app.schemas.complaint.complaint_feedback_schema import (
    ComplaintFeedbackCreate,
    ComplaintFeedbackResponse,
)

from app.services.complaint.complaint_feedback_service import (
    complaint_feedback_service,
)

from app.services.citizen.citizen_service import (
    citizen_service,
)


router = APIRouter(
    prefix="/citizen/complaints",
    tags=["Citizen Complaint Feedback"],
)


@router.post(
    "/{complaint_number}/feedback",
    response_model=ComplaintFeedbackResponse,
)
def create_complaint_feedback(
    complaint_number: str,
    feedback: ComplaintFeedbackCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    citizen = citizen_service.get_by_user_id(
        db,
        current_user.id,
    )

    if citizen is None:
        raise HTTPException(
            status_code=404,
            detail="Citizen profile not found.",
        )

    try:

        return (
            complaint_feedback_service
            .create_feedback(
                db=db,
                complaint_number=complaint_number,
                citizen_id=citizen.id,
                rating=feedback.rating,
                feedback_text=feedback.feedback_text,
                is_satisfied=feedback.is_satisfied,
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{complaint_number}/feedback",
    response_model=ComplaintFeedbackResponse,
)
def get_complaint_feedback(
    complaint_number: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    citizen = citizen_service.get_by_user_id(
        db,
        current_user.id,
    )

    if citizen is None:
        raise HTTPException(
            status_code=404,
            detail="Citizen profile not found.",
        )

    try:

        return (
            complaint_feedback_service
            .get_feedback_for_complaint(
                db=db,
                complaint_number=complaint_number,
                citizen_id=citizen.id,
            )
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )
