from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.village_schema import (
    VillageCreate,
    VillageUpdate,
    VillageResponse,
)

from app.services.master.village_service import (
    village_service,
)


router = APIRouter(
    prefix="/villages",
    tags=["Villages"],
)


@router.get(
    "/",
    response_model=List[VillageResponse],
)
def read_villages(
    db: Session = Depends(get_db),
):
    return village_service.get_all(db)


# --------------------------------------------------
# Gram Panchayat → Villages
# IMPORTANT: must come before /{village_id}
# --------------------------------------------------

@router.get(
    "/gram-panchayat/{gram_panchayat_id}",
    response_model=List[VillageResponse],
)
def read_villages_by_gram_panchayat(
    gram_panchayat_id: int,
    db: Session = Depends(get_db),
):
    return village_service.get_by_gram_panchayat(
        db,
        gram_panchayat_id,
    )


@router.get(
    "/{village_id}",
    response_model=VillageResponse,
)
def read_village(
    village_id: int,
    db: Session = Depends(get_db),
):
    obj = village_service.get_by_id(
        db,
        village_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Village not found",
        )

    return obj


@router.post(
    "/",
    response_model=VillageResponse,
)
def create_village(
    village: VillageCreate,
    db: Session = Depends(get_db),
):
    return village_service.create(
        db,
        village,
    )


@router.put(
    "/{village_id}",
    response_model=VillageResponse,
)
def update_village(
    village_id: int,
    village: VillageUpdate,
    db: Session = Depends(get_db),
):
    obj = village_service.update(
        db,
        village_id,
        village,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Village not found",
        )

    return obj


@router.delete(
    "/{village_id}",
)
def delete_village(
    village_id: int,
    db: Session = Depends(get_db),
):
    obj = village_service.delete(
        db,
        village_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Village not found",
        )

    return {
        "message": "Village deleted successfully"
    }
