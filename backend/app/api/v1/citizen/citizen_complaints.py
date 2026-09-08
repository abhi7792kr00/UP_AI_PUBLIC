from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.current_user import get_current_user

from app.services.citizen.citizen_complaint_service import (
    citizen_complaint_service,
)

from database.models.auth.user import User

from app.schemas.complaint.complaint_schema import (
    ComplaintResponse,
)
from app.schemas.citizen.citizen_complaint_schema import (
    CitizenComplaintCreate,
)

router = APIRouter(
    prefix="/citizen/complaints",
    tags=["Citizen Complaints"],
)


@router.get(
    "/",
    response_model=list[ComplaintResponse],
)
def get_my_complaints(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    try:
        return citizen_complaint_service.get_my_complaints(
            db=db,
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.get(
    "/{complaint_number}",
    response_model=ComplaintResponse,
)
def get_my_complaint(
    complaint_number: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    try:
        return citizen_complaint_service.get_my_complaint(
            db=db,
            user_id=current_user.id,
            complaint_number=complaint_number,
        )

    except ValueError as exc:

        if "authorized" in str(exc).lower():
            raise HTTPException(
                status_code=403,
                detail=str(exc),
            )

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

@router.post(
    "/",
    response_model=ComplaintResponse,
)
def create_my_complaint(
    complaint: CitizenComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):

    try:
        return citizen_complaint_service.create_complaint(
            db=db,
            user_id=current_user.id,
            request=complaint,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )