from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.reference import (
    ReferenceTypeCreate,
    ReferenceTypeUpdate,
    ReferenceTypeResponse,
)

from app.services.reference.reference_type_service import (
    reference_type_service,
)

from app.repositories.reference.reference_type_repository import (
    reference_type_repository,
)

from database.models.reference.reference_type import (
    ReferenceType,
)

router = APIRouter(
    prefix="/reference-types",
    tags=["Reference Type"],
)


@router.get(
    "/",
    response_model=List[ReferenceTypeResponse],
)
def read_reference_types(
    db: Session = Depends(get_db),
):
    return reference_type_service.get_all(db)


@router.get(
    "/{reference_type_id}",
    response_model=ReferenceTypeResponse,
)
def read_reference_type(
    reference_type_id: int,
    db: Session = Depends(get_db),
):
    obj = reference_type_service.get_by_id(
        db,
        reference_type_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Reference type not found",
        )

    return obj


@router.post(
    "/",
    response_model=ReferenceTypeResponse,
)
def create_reference_type(
    reference_type: ReferenceTypeCreate,
    db: Session = Depends(get_db),
):
    if reference_type_repository.exists_by_module_code(
        db,
        reference_type.module_code,
    ):
        raise HTTPException(
            status_code=400,
            detail="Module code already exists",
        )

    obj = ReferenceType(
        **reference_type.model_dump()
    )

    return reference_type_service.create(
        db,
        obj,
    )


@router.put(
    "/{reference_type_id}",
    response_model=ReferenceTypeResponse,
)
def update_reference_type(
    reference_type_id: int,
    reference_type: ReferenceTypeUpdate,
    db: Session = Depends(get_db),
):
    obj = reference_type_service.get_by_id(
        db,
        reference_type_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Reference type not found",
        )

    update_data = reference_type.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return reference_type_service.update(
        db,
        obj,
    )


@router.delete(
    "/{reference_type_id}",
)
def delete_reference_type(
    reference_type_id: int,
    db: Session = Depends(get_db),
):
    obj = reference_type_service.get_by_id(
        db,
        reference_type_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Reference type not found",
        )

    reference_type_service.delete(
        db,
        obj,
    )

    return {
        "message": "Reference type deleted successfully"
    }