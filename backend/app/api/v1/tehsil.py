from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.tehsil_schema import (
    TehsilCreate,
    TehsilResponse,
    TehsilUpdate,
)

from app.services.master.tehsil_service import (
    tehsil_service,
)


router = APIRouter(
    prefix="/tehsils",
    tags=["Tehsils"],
)


# --------------------------------------------------
# Get all tehsils
# --------------------------------------------------

@router.get(
    "/",
    response_model=List[TehsilResponse],
)
def read_tehsils(
    db: Session = Depends(get_db),
):
    return tehsil_service.get_all(db)


# --------------------------------------------------
# District → Tehsils
# IMPORTANT:
# This route must come before /{tehsil_id}
# --------------------------------------------------

@router.get(
    "/district/{district_id}",
    response_model=List[TehsilResponse],
)
def read_tehsils_by_district(
    district_id: int,
    db: Session = Depends(get_db),
):
    return tehsil_service.get_by_district(
        db,
        district_id,
    )


# --------------------------------------------------
# Get one tehsil
# --------------------------------------------------

@router.get(
    "/{tehsil_id}",
    response_model=TehsilResponse,
)
def read_tehsil(
    tehsil_id: int,
    db: Session = Depends(get_db),
):
    tehsil = tehsil_service.get_by_id(
        db,
        tehsil_id,
    )

    if not tehsil:
        raise HTTPException(
            status_code=404,
            detail="Tehsil not found",
        )

    return tehsil


# --------------------------------------------------
# Create tehsil
# --------------------------------------------------

@router.post(
    "/",
    response_model=TehsilResponse,
)
def create_tehsil(
    tehsil: TehsilCreate,
    db: Session = Depends(get_db),
):
    return tehsil_service.create(
        db,
        tehsil,
    )


# --------------------------------------------------
# Update tehsil
# --------------------------------------------------

@router.put(
    "/{tehsil_id}",
    response_model=TehsilResponse,
)
def update_tehsil(
    tehsil_id: int,
    tehsil: TehsilUpdate,
    db: Session = Depends(get_db),
):
    obj = tehsil_service.update(
        db,
        tehsil_id,
        tehsil,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Tehsil not found",
        )

    return obj


# --------------------------------------------------
# Delete tehsil
# --------------------------------------------------

@router.delete(
    "/{tehsil_id}",
)
def delete_tehsil(
    tehsil_id: int,
    db: Session = Depends(get_db),
):
    obj = tehsil_service.delete(
        db,
        tehsil_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Tehsil not found",
        )

    return {
        "message": "Tehsil deleted successfully"
    }