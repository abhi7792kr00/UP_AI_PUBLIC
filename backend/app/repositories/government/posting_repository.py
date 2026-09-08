from sqlalchemy.orm import Session

from database.models.government.posting import Posting


def get_all(db: Session):
    return db.query(Posting).all()


def get_by_id(
    db: Session,
    posting_id: int,
):
    return (
        db.query(Posting)
        .filter(
            Posting.id == posting_id
        )
        .first()
    )


def get_by_order_no(
    db: Session,
    posting_order_no: str,
):
    return (
        db.query(Posting)
        .filter(
            Posting.posting_order_no == posting_order_no
        )
        .first()
    )


def create(
    db: Session,
    posting: Posting,
):
    db.add(posting)
    db.commit()
    db.refresh(posting)
    return posting


def delete(
    db: Session,
    posting: Posting,
):
    db.delete(posting)
    db.commit()