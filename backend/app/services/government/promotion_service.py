from sqlalchemy.orm import Session

from app.repositories.government import promotion_repository
from app.schemas.government.promotion_schema import (
    PromotionCreate,
    PromotionUpdate,
)
from database.models.government.promotion import Promotion


def get_promotions(db: Session):
    return promotion_repository.get_all(db)


def get_promotion(
    db: Session,
    promotion_id: int,
):
    return promotion_repository.get_by_id(
        db,
        promotion_id,
    )


def create_promotion(
    db: Session,
    promotion_data: PromotionCreate,
):
    promotion = Promotion(
        promotion_order_no=promotion_data.promotion_order_no,
        promotion_date=promotion_data.promotion_date,
        officer_id=promotion_data.officer_id,
        old_designation_id=promotion_data.old_designation_id,
        new_designation_id=promotion_data.new_designation_id,
        remarks=promotion_data.remarks,
        status=promotion_data.status,
    )

    return promotion_repository.create(
        db,
        promotion,
    )


def update_promotion(
    db: Session,
    promotion_id: int,
    promotion_data: PromotionUpdate,
):
    promotion = promotion_repository.get_by_id(
        db,
        promotion_id,
    )

    if not promotion:
        return None

    update_data = promotion_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            promotion,
            key,
            value,
        )

    db.commit()
    db.refresh(promotion)

    return promotion


def delete_promotion(
    db: Session,
    promotion_id: int,
):
    promotion = promotion_repository.get_by_id(
        db,
        promotion_id,
    )

    if not promotion:
        return False

    promotion_repository.delete(
        db,
        promotion,
    )

    return True