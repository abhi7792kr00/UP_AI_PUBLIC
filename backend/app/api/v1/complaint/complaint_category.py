from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.complaint import (
    ComplaintCategoryCreate,
    ComplaintCategoryUpdate,
    ComplaintCategoryResponse,
)

from app.services.complaint import (
    complaint_category_service,
)

from database.models.complaint.complaint_category import (
    ComplaintCategory,
)


router = APIRouter(
    prefix="/complaint-categories",
    tags=["Complaint Category"],
)


@router.get(
    "/",
    response_model=List[ComplaintCategoryResponse],
)
def read_categories(
    db: Session = Depends(get_db),
):
    return complaint_category_service.get_all(db)


@router.get(
    "/{category_id}",
    response_model=ComplaintCategoryResponse,
)
def read_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_category_service.get_by_id(
        db,
        category_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint category not found",
        )

    return obj


@router.post(
    "/",
    response_model=ComplaintCategoryResponse,
)
def create_category(
    category: ComplaintCategoryCreate,
    db: Session = Depends(get_db),
):
    obj = ComplaintCategory(
        **category.model_dump()
    )

    return complaint_category_service.create(
        db,
        obj,
    )


@router.put(
    "/{category_id}",
    response_model=ComplaintCategoryResponse,
)
def update_category(
    category_id: int,
    category: ComplaintCategoryUpdate,
    db: Session = Depends(get_db),
):
    obj = complaint_category_service.get_by_id(
        db,
        category_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint category not found",
        )

    update_data = category.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return complaint_category_service.update(
        db,
        obj,
    )


@router.delete(
    "/{category_id}",
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_category_service.get_by_id(
        db,
        category_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint category not found",
        )

    complaint_category_service.delete(
        db,
        obj,
    )

    return {
        "message": "Complaint category deleted successfully"
    }