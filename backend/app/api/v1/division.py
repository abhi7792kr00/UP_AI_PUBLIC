from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.division_schema import (
    DivisionCreate,
    DivisionResponse,
    DivisionUpdate,
)

from app.services.master.division_service import (
    division_service,
)

router = APIRouter(
    prefix="/divisions",
    tags=["Divisions"],
)


@router.get(
    "/",
    response_model=List[DivisionResponse],
)
def read_divisions(
    db: Session = Depends(get_db),
):
    return division_service.get_all(db)


@router.get(
    "/{division_id}",
    response_model=DivisionResponse,
)
def read_division(
    division_id: int,
    db: Session = Depends(get_db),
):
    division = division_service.get_by_id(
        db,
        division_id,
    )

    if not division:
        raise HTTPException(
            status_code=404,
            detail="Division not found",
        )

    return division


@router.post(
    "/",
    response_model=DivisionResponse,
)
def create_division(
    division: DivisionCreate,
    db: Session = Depends(get_db),
):
    return division_service.create(
        db,
        division,
    )


@router.put(
    "/{division_id}",
    response_model=DivisionResponse,
)
def update_division(
    division_id: int,
    division: DivisionUpdate,
    db: Session = Depends(get_db),
):
    obj = division_service.update(
        db,
        division_id,
        division,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Division not found",
        )

    return obj


@router.delete(
    "/{division_id}",
)
def delete_division(
    division_id: int,
    db: Session = Depends(get_db),
):
    obj = division_service.delete(
        db,
        division_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="Division not found",
        )

    return {
        "message": "Division deleted successfully"
    }