from sqlalchemy.orm import Session

from database.models.government.transfer import Transfer


def get_all(db: Session):
    return db.query(Transfer).all()


def get_by_id(
    db: Session,
    transfer_id: int,
):
    return (
        db.query(Transfer)
        .filter(
            Transfer.id == transfer_id
        )
        .first()
    )


def get_by_order_no(
    db: Session,
    transfer_order_no: str,
):
    return (
        db.query(Transfer)
        .filter(
            Transfer.transfer_order_no == transfer_order_no
        )
        .first()
    )


def create(
    db: Session,
    transfer: Transfer,
):
    db.add(transfer)
    db.commit()
    db.refresh(transfer)
    return transfer


def delete(
    db: Session,
    transfer: Transfer,
):
    db.delete(transfer)
    db.commit()