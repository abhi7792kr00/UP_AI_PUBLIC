from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.officer_schema import (
    OfficerCreate,
    OfficerUpdate,
    OfficerResponse,
)

from app.services.government.officer_service import (
    get_officers,
    get_officer,
    create_officer,
    update_officer,
    delete_officer,
)

router = APIRouter(
    prefix="/officers",
    tags=["Officer"],
)


@router.get(
    "/",
    response_model=list[OfficerResponse],
)
def read_officers(
    db: Session = Depends(get_db),
):
    return get_officers(db)


@router.get(
    "/{officer_id}",
    response_model=OfficerResponse,
)
def read_officer(
    officer_id: int,
    db: Session = Depends(get_db),
):
    officer = get_officer(
        db,
        officer_id,
    )

    if not officer:
        raise HTTPException(
            status_code=404,
            detail="Officer not found",
        )

    return officer


@router.post(
    "/",
    response_model=OfficerResponse,
)
def create_new_officer(
    officer: OfficerCreate,
    db: Session = Depends(get_db),
):
    return create_officer(
        db,
        officer,
    )


@router.put(
    "/{officer_id}",
    response_model=OfficerResponse,
)
def update_existing_officer(
    officer_id: int,
    officer: OfficerUpdate,
    db: Session = Depends(get_db),
):
    updated = update_officer(
        db,
        officer_id,
        officer,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Officer not found",
        )

    return updated


@router.delete(
    "/{officer_id}",
)
def delete_existing_officer(
    officer_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_officer(
        db,
        officer_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Officer not found",
        )

    return {
        "message": "Officer deleted successfully"
    }
