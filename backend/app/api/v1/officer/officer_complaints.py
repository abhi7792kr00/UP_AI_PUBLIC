from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.current_user import get_current_user

from database.models.auth.user import User

from app.schemas.officer.officer_complaint_schema import (
    OfficerComplaintResponse,
)

from app.services.complaint import complaint_service


router = APIRouter(
    prefix="/officer",
    tags=["Officer Complaints"],
)


@router.get(
    "/complaints",
    response_model=list[OfficerComplaintResponse],
    summary="Get Officer Assigned Complaints",
    description="Get active complaints assigned to the logged-in officer.",
)
def get_officer_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    if current_user.officer_id is None:
        raise HTTPException(
            status_code=403,
            detail="User is not linked to an officer.",
        )

    return complaint_service.get_assigned_complaints_for_officer(
        db=db,
        officer_id=current_user.officer_id,
    )