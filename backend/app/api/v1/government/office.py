from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.office_schema import (
    OfficeCreate,
    OfficeUpdate,
    OfficeResponse,
)

from app.services.government.office_service import (
    get_offices,
    get_office,
    create_office,
    update_office,
    delete_office,
)

router = APIRouter(
    prefix="/offices",
    tags=["Office"],
)


@router.get(
    "/",
    response_model=list[OfficeResponse],
)
def read_offices(
    db: Session = Depends(get_db),
):
    return get_offices(db)


@router.get(
    "/{office_id}",
    response_model=OfficeResponse,
)
def read_office(
    office_id: int,
    db: Session = Depends(get_db),
):
    office = get_office(db, office_id)

    if not office:
        raise HTTPException(
            status_code=404,
            detail="Office not found",
        )

    return office


@router.post(
    "/",
    response_model=OfficeResponse,
)
def create_new_office(
    office: OfficeCreate,
    db: Session = Depends(get_db),
):
    return create_office(
        db,
        office,
    )


@router.put(
    "/{office_id}",
    response_model=OfficeResponse,
)
def update_existing_office(
    office_id: int,
    office: OfficeUpdate,
    db: Session = Depends(get_db),
):
    updated = update_office(
        db,
        office_id,
        office,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Office not found",
        )

    return updated


@router.delete(
    "/{office_id}",
)
def delete_existing_office(
    office_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_office(
        db,
        office_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Office not found",
        )

    return {
        "message": "Office deleted successfully"
    }