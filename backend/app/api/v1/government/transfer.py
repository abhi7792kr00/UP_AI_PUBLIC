from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.transfer_schema import (
    TransferCreate,
    TransferUpdate,
    TransferResponse,
)

from app.services.government.transfer_service import (
    get_transfers,
    get_transfer,
    create_transfer,
    update_transfer,
    delete_transfer,
)

router = APIRouter(
    prefix="/transfers",
    tags=["Transfer"],
)


@router.get(
    "/",
    response_model=list[TransferResponse],
)
def read_transfers(
    db: Session = Depends(get_db),
):
    return get_transfers(db)


@router.get(
    "/{transfer_id}",
    response_model=TransferResponse,
)
def read_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
):
    transfer = get_transfer(
        db,
        transfer_id,
    )

    if not transfer:
        raise HTTPException(
            status_code=404,
            detail="Transfer not found",
        )

    return transfer


@router.post(
    "/",
    response_model=TransferResponse,
)
def create_new_transfer(
    transfer: TransferCreate,
    db: Session = Depends(get_db),
):
    return create_transfer(
        db,
        transfer,
    )


@router.put(
    "/{transfer_id}",
    response_model=TransferResponse,
)
def update_existing_transfer(
    transfer_id: int,
    transfer: TransferUpdate,
    db: Session = Depends(get_db),
):
    updated = update_transfer(
        db,
        transfer_id,
        transfer,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Transfer not found",
        )

    return updated


@router.delete(
    "/{transfer_id}",
)
def delete_existing_transfer(
    transfer_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_transfer(
        db,
        transfer_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Transfer not found",
        )

    return {
        "message": "Transfer deleted successfully"
    }