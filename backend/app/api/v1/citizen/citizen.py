from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.citizen.citizen_schema import (
    CitizenCreate,
    CitizenUpdate,
    CitizenResponse,
)

from app.services.citizen import CitizenService

router = APIRouter(
    prefix="/citizens",
    tags=["Citizen"],
)


@router.get(
    "/",
    response_model=list[CitizenResponse],
)
def read_citizens(
    db: Session = Depends(get_db),
):
    return CitizenService.get_all_citizens(db)


@router.get(
    "/{citizen_id}",
    response_model=CitizenResponse,
)
def read_citizen(
    citizen_id: int,
    db: Session = Depends(get_db),
):
    try:
        return CitizenService.get_citizen(
            db,
            citizen_id,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.post(
    "/",
    response_model=CitizenResponse,
)
def create_new_citizen(
    citizen: CitizenCreate,
    db: Session = Depends(get_db),
):
    try:
        return CitizenService.create_citizen(
            db,
            citizen,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.put(
    "/{citizen_id}",
    response_model=CitizenResponse,
)
def update_existing_citizen(
    citizen_id: int,
    citizen: CitizenUpdate,
    db: Session = Depends(get_db),
):
    try:
        return CitizenService.update_citizen(
            db,
            citizen_id,
            citizen,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.delete(
    "/{citizen_id}",
)
def delete_existing_citizen(
    citizen_id: int,
    db: Session = Depends(get_db),
):
    try:
        CitizenService.delete_citizen(
            db,
            citizen_id,
        )

        return {
            "message": "Citizen deleted successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )