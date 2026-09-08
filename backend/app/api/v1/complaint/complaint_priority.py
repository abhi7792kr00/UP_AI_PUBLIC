from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.complaint import (
    ComplaintPriorityCreate,
    ComplaintPriorityUpdate,
    ComplaintPriorityResponse,
)

from app.services.complaint import (
    complaint_priority_service,
)

from database.models.complaint.complaint_priority import (
    ComplaintPriority,
)


router = APIRouter(
    prefix="/complaint-priorities",
    tags=["Complaint Priority"],
)


@router.get(
    "/",
    response_model=List[ComplaintPriorityResponse],
)
def read_priorities(
    db: Session = Depends(get_db),
):
    return complaint_priority_service.get_all(db)


@router.get(
    "/{priority_id}",
    response_model=ComplaintPriorityResponse,
)
def read_priority(
    priority_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_priority_service.get_by_id(
        db,
        priority_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint priority not found",
        )

    return obj


@router.post(
    "/",
    response_model=ComplaintPriorityResponse,
)
def create_priority(
    priority: ComplaintPriorityCreate,
    db: Session = Depends(get_db),
):
    obj = ComplaintPriority(
        **priority.model_dump()
    )

    return complaint_priority_service.create(
        db,
        obj,
    )


@router.put(
    "/{priority_id}",
    response_model=ComplaintPriorityResponse,
)
def update_priority(
    priority_id: int,
    priority: ComplaintPriorityUpdate,
    db: Session = Depends(get_db),
):
    obj = complaint_priority_service.get_by_id(
        db,
        priority_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint priority not found",
        )

    update_data = priority.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return complaint_priority_service.update(
        db,
        obj,
    )


@router.delete(
    "/{priority_id}",
)
def delete_priority(
    priority_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_priority_service.get_by_id(
        db,
        priority_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint priority not found",
        )

    complaint_priority_service.delete(
        db,
        obj,
    )

    return {
        "message": "Complaint priority deleted successfully"
    }