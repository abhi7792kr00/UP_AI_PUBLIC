from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.schemas.government.designation_schema import (
    DesignationCreate,
    DesignationResponse,
    DesignationUpdate,
)
from app.services.government.designation_service import (
    create_designation,
    delete_designation,
    get_designation,
    get_designations,
    update_designation,
)

router = APIRouter(
    prefix="/designations",
    tags=["Designation"],
)


@router.get(
    "/",
    response_model=list[DesignationResponse],
)
def read_designations(
    db: Session = Depends(get_db),
):
    return get_designations(db)


@router.get(
    "/{designation_id}",
    response_model=DesignationResponse,
)
def read_designation(
    designation_id: int,
    db: Session = Depends(get_db),
):
    designation = get_designation(
        db,
        designation_id,
    )

    if not designation:
        raise HTTPException(
            status_code=404,
            detail="Designation not found",
        )

    return designation


@router.post(
    "/",
    response_model=DesignationResponse,
)
def create_new_designation(
    designation: DesignationCreate,
    db: Session = Depends(get_db),
):
    return create_designation(
        db,
        designation,
    )


@router.put(
    "/{designation_id}",
    response_model=DesignationResponse,
)
def update_existing_designation(
    designation_id: int,
    designation: DesignationUpdate,
    db: Session = Depends(get_db),
):
    updated = update_designation(
        db,
        designation_id,
        designation,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Designation not found",
        )

    return updated


@router.delete(
    "/{designation_id}",
)
def delete_existing_designation(
    designation_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_designation(
        db,
        designation_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Designation not found",
        )

    return {
        "message": "Designation deleted successfully"
    }