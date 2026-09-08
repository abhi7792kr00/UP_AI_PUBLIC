from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.complaint import (
    ComplaintSubCategoryCreate,
    ComplaintSubCategoryUpdate,
    ComplaintSubCategoryResponse,
)

from app.services.complaint import (
    complaint_subcategory_service,
)

from database.models.complaint.complaint_subcategory import (
    ComplaintSubCategory,
)

router = APIRouter(
    prefix="/complaint-subcategories",
    tags=["Complaint SubCategory"],
)


@router.get(
    "/",
    response_model=List[ComplaintSubCategoryResponse],
)
def read_subcategories(
    db: Session = Depends(get_db),
):
    return complaint_subcategory_service.get_all(db)


@router.get(
    "/{subcategory_id}",
    response_model=ComplaintSubCategoryResponse,
)
def read_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_subcategory_service.get_by_id(
        db,
        subcategory_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint subcategory not found",
        )

    return obj


@router.post(
    "/",
    response_model=ComplaintSubCategoryResponse,
)
def create_subcategory(
    subcategory: ComplaintSubCategoryCreate,
    db: Session = Depends(get_db),
):
    obj = ComplaintSubCategory(
        **subcategory.model_dump()
    )

    return complaint_subcategory_service.create(
        db,
        obj,
    )


@router.put(
    "/{subcategory_id}",
    response_model=ComplaintSubCategoryResponse,
)
def update_subcategory(
    subcategory_id: int,
    subcategory: ComplaintSubCategoryUpdate,
    db: Session = Depends(get_db),
):
    obj = complaint_subcategory_service.get_by_id(
        db,
        subcategory_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint subcategory not found",
        )

    update_data = subcategory.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return complaint_subcategory_service.update(
        db,
        obj,
    )


@router.delete(
    "/{subcategory_id}",
)
def delete_subcategory(
    subcategory_id: int,
    db: Session = Depends(get_db),
):
    obj = complaint_subcategory_service.get_by_id(
        db,
        subcategory_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Complaint subcategory not found",
        )

    complaint_subcategory_service.delete(
        db,
        obj,
    )

    return {
        "message": "Complaint subcategory deleted successfully"
    }