from datetime import date
from typing import Optional

from pydantic import BaseModel


class LeaveBase(BaseModel):
    leave_order_no: str
    leave_type: str

    start_date: date
    end_date: date

    total_days: int

    reason: Optional[str] = None

    status: str = "Pending"

    approved_by: Optional[int] = None

    officer_id: int

    remarks: Optional[str] = None


class LeaveCreate(LeaveBase):
    pass


class LeaveUpdate(BaseModel):
    leave_order_no: Optional[str] = None
    leave_type: Optional[str] = None

    start_date: Optional[date] = None
    end_date: Optional[date] = None

    total_days: Optional[int] = None

    reason: Optional[str] = None

    status: Optional[str] = None

    approved_by: Optional[int] = None

    officer_id: Optional[int] = None

    remarks: Optional[str] = None


class LeaveResponse(LeaveBase):
    id: int

    is_active: bool

    model_config = {
        "from_attributes": True
    }