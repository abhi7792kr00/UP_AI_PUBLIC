from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.district_schema import (
    DistrictCreate,
    DistrictResponse,
    DistrictUpdate,
)

from app.services.master.district_service import (
    district_service,
)

router = APIRouter(
    prefix="/districts",
    tags=["Districts"],
)


@router.get(
    "/",
    response_model=List[DistrictResponse],
)
def read_districts(
    db: Session = Depends(get_db),
):
    return district_service.get_all(db)


@router.get(
    "/{district_id}",
    response_model=DistrictResponse,
)
def read_district(
    district_id: int,
    db: Session = Depends(get_db),
):
    district = district_service.get_by_id(
        db,
        district_id,
    )

    if not district:
        raise HTTPException(
            status_code=404,
            detail="District not found",
        )

    return district


@router.post(
    "/",
    response_model=DistrictResponse,
)
def create_district(
    district: DistrictCreate,
    db: Session = Depends(get_db),
):
    return district_service.create(
        db,
        district,
    )


@router.put(
    "/{district_id}",
    response_model=DistrictResponse,
)
def update_district(
    district_id: int,
    district: DistrictUpdate,
    db: Session = Depends(get_db),
):
    obj = district_service.update(
        db,
        district_id,
        district,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="District not found",
        )

    return obj


@router.delete(
    "/{district_id}",
)
def delete_district(
    district_id: int,
    db: Session = Depends(get_db),
):
    obj = district_service.delete(
        db,
        district_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="District not found",
        )

    return {
        "message": "District deleted successfully"
    }