from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.complaint import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
)

from app.services.complaint import (
    complaint_service,
)

from database.models.complaint.complaint import Complaint


router = APIRouter(
    prefix="/complaints",
    tags=["Complaint"],
)


@router.get(
    "/",
    response_model=list[ComplaintResponse],
)
def read_complaints(
    db: Session = Depends(get_db),
):
    return complaint_service.get_all(db)


@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def read_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    complaint = complaint_service.get_by_id(
        db,
        complaint_id,
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return complaint


@router.post(
    "/",
    response_model=ComplaintResponse,
)
def create_complaint(
    complaint: ComplaintCreate,
    db: Session = Depends(get_db),
):
    complaint_obj = Complaint(
        **complaint.model_dump()
    )

    return complaint_service.create(
        db,
        complaint_obj,
    )


@router.put(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def update_complaint(
    complaint_id: int,
    complaint: ComplaintUpdate,
    db: Session = Depends(get_db),
):
    db_obj = complaint_service.get_by_id(
        db,
        complaint_id,
    )

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    update_data = complaint.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_obj,
            key,
            value,
        )

    return complaint_service.update(
        db,
        db_obj,
    )


@router.delete(
    "/{complaint_id}",
)
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    db_obj = complaint_service.get_by_id(
        db,
        complaint_id,
    )

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    complaint_service.delete(
        db,
        db_obj,
    )

    return {
        "message": "Complaint deleted successfully"
    }