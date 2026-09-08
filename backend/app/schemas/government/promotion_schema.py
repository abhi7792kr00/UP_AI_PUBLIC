from datetime import date
from typing import Optional

from pydantic import BaseModel


class PromotionBase(BaseModel):
    promotion_order_no: str
    promotion_date: date

    officer_id: int

    old_designation_id: int
    new_designation_id: int

    remarks: Optional[str] = None

    status: str = "Pending"


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    promotion_order_no: Optional[str] = None
    promotion_date: Optional[date] = None

    officer_id: Optional[int] = None

    old_designation_id: Optional[int] = None
    new_designation_id: Optional[int] = None

    remarks: Optional[str] = None

    status: Optional[str] = None


class PromotionResponse(PromotionBase):
    id: int

    is_active: bool

    model_config = {
        "from_attributes": True
    }