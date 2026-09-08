from datetime import date
from typing import Optional

from pydantic import BaseModel


class TransferBase(BaseModel):
    transfer_order_no: str
    transfer_date: date

    relieving_date: Optional[date] = None
    joining_date: Optional[date] = None

    officer_id: int
    from_office_id: int
    to_office_id: int

    reason: Optional[str] = None
    status: Optional[str] = "Pending"


class TransferCreate(TransferBase):
    pass


class TransferUpdate(BaseModel):
    transfer_order_no: Optional[str] = None
    transfer_date: Optional[date] = None

    relieving_date: Optional[date] = None
    joining_date: Optional[date] = None

    officer_id: Optional[int] = None
    from_office_id: Optional[int] = None
    to_office_id: Optional[int] = None

    reason: Optional[str] = None
    status: Optional[str] = None


class TransferResponse(TransferBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }