from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.reference import (
    ReferenceFormatCreate,
    ReferenceFormatUpdate,
    ReferenceFormatResponse,
)

from app.services.reference.reference_format_service import (
    reference_format_service,
)

from app.services.reference.reference_type_service import (
    reference_type_service,
)

from app.repositories.reference.reference_format_repository import (
    reference_format_repository,
)

from database.models.reference.reference_format import (
    ReferenceFormat,
)

router = APIRouter(
    prefix="/reference-formats",
    tags=["Reference Format"],
)


@router.get(
    "/",
    response_model=List[ReferenceFormatResponse],
)
def read_reference_formats(
    db: Session = Depends(get_db),
):
    return reference_format_service.get_all(db)


@router.get(
    "/{reference_format_id}",
    response_model=ReferenceFormatResponse,
)
def read_reference_format(
    reference_format_id: int,
    db: Session = Depends(get_db),
):
    obj = reference_format_service.get_by_id(
        db,
        reference_format_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Reference format not found",
        )

    return obj


@router.post(
    "/",
    response_model=ReferenceFormatResponse,
)
def create_reference_format(
    reference_format: ReferenceFormatCreate,
    db: Session = Depends(get_db),
):
    if not reference_type_service.exists(
        db,
        reference_format.reference_type_id,
    ):
        raise HTTPException(
            status_code=404,
            detail="Reference type not found",
        )

    if reference_format_repository.exists_by_prefix(
        db,
        reference_format.prefix,
    ):
        raise HTTPException(
            status_code=400,
            detail="Prefix already exists",
        )

    obj = ReferenceFormat(
        **reference_format.model_dump()
    )

    return reference_format_service.create(
        db,
        obj,
    )


@router.put(
    "/{reference_format_id}",
    response_model=ReferenceFormatResponse,
)
def update_reference_format(
    reference_format_id: int,
    reference_format: ReferenceFormatUpdate,
    db: Session = Depends(get_db),
):
    obj = reference_format_service.get_by_id(
        db,
        reference_format_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Reference format not found",
        )

    update_data = reference_format.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return reference_format_service.update(
        db,
        obj,
    )


@router.delete(
    "/{reference_format_id}",
)
def delete_reference_format(
    reference_format_id: int,
    db: Session = Depends(get_db),
):
    obj = reference_format_service.get_by_id(
        db,
        reference_format_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Reference format not found",
        )

    reference_format_service.delete(
        db,
        obj,
    )

    return {
        "message": "Reference format deleted successfully"
    }