from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.master.ward_schema import (
    WardCreate,
    WardUpdate,
    WardResponse,
)

from app.services.master.ward_service import (
    ward_service,
)

from database.models.master.ward import Ward


router = APIRouter(
    prefix="/wards",
    tags=["Wards"],
)


@router.get(
    "/",
    response_model=list[WardResponse],
)
def read_wards(
    db: Session = Depends(get_db),
):
    return ward_service.get_all(db)


@router.get(
    "/{ward_id}",
    response_model=WardResponse,
)
def read_ward(
    ward_id: int,
    db: Session = Depends(get_db),
):
    ward = ward_service.get_by_id(
        db,
        ward_id,
    )

    if not ward:
        raise HTTPException(
            status_code=404,
            detail="Ward not found",
        )

    return ward


@router.post(
    "/",
    response_model=WardResponse,
)
def create_ward(
    ward: WardCreate,
    db: Session = Depends(get_db),
):
    ward_obj = Ward(
        **ward.model_dump()
    )

    return ward_service.create(
        db,
        ward_obj,
    )


@router.put(
    "/{ward_id}",
    response_model=WardResponse,
)
def update_ward(
    ward_id: int,
    ward: WardUpdate,
    db: Session = Depends(get_db),
):
    db_obj = ward_service.get_by_id(
        db,
        ward_id,
    )

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="Ward not found",
        )

    update_data = ward.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            db_obj,
            key,
            value,
        )

    return ward_service.update(
        db,
        db_obj,
    )


@router.delete(
    "/{ward_id}",
)
def delete_ward(
    ward_id: int,
    db: Session = Depends(get_db),
):
    db_obj = ward_service.get_by_id(
        db,
        ward_id,
    )

    if not db_obj:
        raise HTTPException(
            status_code=404,
            detail="Ward not found",
        )

    ward_service.delete(
        db,
        db_obj,
    )

    return {
        "message": "Ward deleted successfully"
    }