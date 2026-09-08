from sqlalchemy.orm import Session

from database.models.government.leave import Leave


def get_all(db: Session):
    return db.query(Leave).all()


def get_by_id(
    db: Session,
    leave_id: int,
):
    return (
        db.query(Leave)
        .filter(
            Leave.id == leave_id
        )
        .first()
    )


def get_by_order_no(
    db: Session,
    order_no: str,
):
    return (
        db.query(Leave)
        .filter(
            Leave.leave_order_no == order_no
        )
        .first()
    )


def create(
    db: Session,
    leave: Leave,
):
    db.add(leave)
    db.commit()
    db.refresh(leave)
    return leave


def delete(
    db: Session,
    leave: Leave,
):
    db.delete(leave)
    db.commit()