from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.master.locality_schema import (
    LocalityCreate,
    LocalityUpdate,
)

from app.services.master.locality_service import (
    locality_service,
)

router = APIRouter(
    prefix="/localities",
    tags=["Localities"],
)


@router.get("/")
def read_localities(
    db: Session = Depends(get_db),
):
    return locality_service.get_all(db)


@router.get("/{locality_id}")
def read_locality(
    locality_id: int,
    db: Session = Depends(get_db),
):
    return locality_service.get_by_id(
        db,
        locality_id,
    )


@router.post("/")
def create_locality(
    locality: LocalityCreate,
    db: Session = Depends(get_db),
):
    return locality_service.create(
        db,
        locality,
    )


@router.put("/{locality_id}")
def update_locality(
    locality_id: int,
    locality: LocalityUpdate,
    db: Session = Depends(get_db),
):
    return locality_service.update(
        db,
        locality_id,
        locality,
    )


@router.delete("/{locality_id}")
def delete_locality(
    locality_id: int,
    db: Session = Depends(get_db),
):
    return locality_service.delete(
        db,
        locality_id,
    )