from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.promotion_schema import (
    PromotionCreate,
    PromotionUpdate,
    PromotionResponse,
)

from app.services.government.promotion_service import (
    get_promotions,
    get_promotion,
    create_promotion,
    update_promotion,
    delete_promotion,
)

router = APIRouter(
    prefix="/promotions",
    tags=["Promotion"],
)


@router.get(
    "/",
    response_model=list[PromotionResponse],
)
def read_promotions(
    db: Session = Depends(get_db),
):
    return get_promotions(db)


@router.get(
    "/{promotion_id}",
    response_model=PromotionResponse,
)
def read_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
):
    promotion = get_promotion(
        db,
        promotion_id,
    )

    if not promotion:
        raise HTTPException(
            status_code=404,
            detail="Promotion not found",
        )

    return promotion


@router.post(
    "/",
    response_model=PromotionResponse,
)
def create_new_promotion(
    promotion: PromotionCreate,
    db: Session = Depends(get_db),
):
    return create_promotion(
        db,
        promotion,
    )


@router.put(
    "/{promotion_id}",
    response_model=PromotionResponse,
)
def update_existing_promotion(
    promotion_id: int,
    promotion: PromotionUpdate,
    db: Session = Depends(get_db),
):
    updated = update_promotion(
        db,
        promotion_id,
        promotion,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Promotion not found",
        )

    return updated


@router.delete(
    "/{promotion_id}",
)
def delete_existing_promotion(
    promotion_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_promotion(
        db,
        promotion_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Promotion not found",
        )

    return {
        "message": "Promotion deleted successfully"
    }