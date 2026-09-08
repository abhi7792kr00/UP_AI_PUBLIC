from sqlalchemy.orm import Session

from app.repositories.government import transfer_repository
from app.schemas.government.transfer_schema import (
    TransferCreate,
    TransferUpdate,
)
from database.models.government.transfer import Transfer


def get_transfers(db: Session):
    return transfer_repository.get_all(db)


def get_transfer(
    db: Session,
    transfer_id: int,
):
    return transfer_repository.get_by_id(
        db,
        transfer_id,
    )


def create_transfer(
    db: Session,
    transfer_data: TransferCreate,
):
    transfer = Transfer(
        transfer_order_no=transfer_data.transfer_order_no,
        transfer_date=transfer_data.transfer_date,
        relieving_date=transfer_data.relieving_date,
        joining_date=transfer_data.joining_date,
        officer_id=transfer_data.officer_id,
        from_office_id=transfer_data.from_office_id,
        to_office_id=transfer_data.to_office_id,
        reason=transfer_data.reason,
        status=transfer_data.status,
    )

    return transfer_repository.create(
        db,
        transfer,
    )


def update_transfer(
    db: Session,
    transfer_id: int,
    transfer_data: TransferUpdate,
):
    transfer = transfer_repository.get_by_id(
        db,
        transfer_id,
    )

    if not transfer:
        return None

    update_data = transfer_data.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            transfer,
            key,
            value,
        )

    db.commit()
    db.refresh(transfer)

    return transfer


def delete_transfer(
    db: Session,
    transfer_id: int,
):
    transfer = transfer_repository.get_by_id(
        db,
        transfer_id,
    )

    if not transfer:
        return False

    transfer_repository.delete(
        db,
        transfer,
    )

    return True