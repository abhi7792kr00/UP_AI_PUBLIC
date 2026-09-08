from sqlalchemy.orm import Session

from database.models.government.promotion import Promotion


def get_all(db: Session):
    return db.query(Promotion).all()


def get_by_id(
    db: Session,
    promotion_id: int,
):
    return (
        db.query(Promotion)
        .filter(
            Promotion.id == promotion_id
        )
        .first()
    )


def get_by_order_no(
    db: Session,
    order_no: str,
):
    return (
        db.query(Promotion)
        .filter(
            Promotion.promotion_order_no == order_no
        )
        .first()
    )


def create(
    db: Session,
    promotion: Promotion,
):
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion


def delete(
    db: Session,
    promotion: Promotion,
):
    db.delete(promotion)
    db.commit()