from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.suspension_schema import (
    SuspensionCreate,
    SuspensionUpdate,
    SuspensionResponse,
)

from app.services.government.suspension_service import (
    create_suspension,
    get_suspensions,
    get_suspension,
    update_suspension,
    delete_suspension,
)

router = APIRouter(
    prefix="/suspensions",
    tags=["Suspension"],
)


@router.get(
    "/",
    response_model=list[SuspensionResponse],
)
def read_suspensions(
    db: Session = Depends(get_db),
):
    return get_suspensions(db)


@router.get(
    "/{suspension_id}",
    response_model=SuspensionResponse,
)
def read_suspension(
    suspension_id: int,
    db: Session = Depends(get_db),
):
    suspension = get_suspension(
        db,
        suspension_id,
    )

    if suspension is None:
        raise HTTPException(
            status_code=404,
            detail="Suspension not found",
        )

    return suspension


@router.post(
    "/",
    response_model=SuspensionResponse,
)
def create_new_suspension(
    suspension: SuspensionCreate,
    db: Session = Depends(get_db),
):
    return create_suspension(
        db,
        suspension,
    )


@router.put(
    "/{suspension_id}",
    response_model=SuspensionResponse,
)
def update_existing_suspension(
    suspension_id: int,
    suspension: SuspensionUpdate,
    db: Session = Depends(get_db),
):
    updated = update_suspension(
        db,
        suspension_id,
        suspension,
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Suspension not found",
        )

    return updated


@router.delete(
    "/{suspension_id}",
)
def delete_existing_suspension(
    suspension_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_suspension(
        db,
        suspension_id,
    )

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Suspension not found",
        )

    return {
        "message": "Suspension deleted successfully"
    }