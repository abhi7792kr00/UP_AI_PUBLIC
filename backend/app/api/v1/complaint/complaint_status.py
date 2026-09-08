from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.complaint import (
    ComplaintStatusCreate,
    ComplaintStatusUpdate,
    ComplaintStatusResponse,
)

from app.services.complaint import (
    complaint_status_service,
)

from database.models.complaint.complaint_status import (
    ComplaintStatus,
)


router = APIRouter(
    prefix="/complaint-statuses",
    tags=["Complaint Status"],
)


@router.get(
    "/",
    response_model=List[ComplaintStatusResponse],
)
def read_statuses(
    db: Session = Depends(get_db),
):
    return complaint_status_service.get_all(db)


@router.get(
    "/{status_id}",
    response_model=ComplaintStatusResponse,
)
def read_status(
    status_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_status_service.get_by_id(
        db,
        status_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint status not found",
        )

    return obj


@router.post(
    "/",
    response_model=ComplaintStatusResponse,
)
def create_status(
    status: ComplaintStatusCreate,
    db: Session = Depends(get_db),
):
    obj = ComplaintStatus(
        **status.model_dump()
    )

    return complaint_status_service.create(
        db,
        obj,
    )


@router.put(
    "/{status_id}",
    response_model=ComplaintStatusResponse,
)
def update_status(
    status_id: int,
    status: ComplaintStatusUpdate,
    db: Session = Depends(get_db),
):
    obj = complaint_status_service.get_by_id(
        db,
        status_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint status not found",
        )

    update_data = status.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return complaint_status_service.update(
        db,
        obj,
    )


@router.delete(
    "/{status_id}",
)
def delete_status(
    status_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_status_service.get_by_id(
        db,
        status_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint status not found",
        )

    complaint_status_service.delete(
        db,
        obj,
    )

    return {
        "message": "Complaint status deleted successfully"
    }