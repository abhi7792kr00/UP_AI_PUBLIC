from datetime import date
from typing import Optional

from pydantic import BaseModel


class PostingBase(BaseModel):
    posting_order_no: str
    joining_date: date
    relieving_date: Optional[date] = None
    remarks: Optional[str] = None

    officer_id: int
    department_id: int
    designation_id: int
    office_id: int


class PostingCreate(PostingBase):
    pass


class PostingUpdate(BaseModel):
    posting_order_no: Optional[str] = None
    joining_date: Optional[date] = None
    relieving_date: Optional[date] = None
    remarks: Optional[str] = None

    officer_id: Optional[int] = None
    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    office_id: Optional[int] = None


class PostingResponse(PostingBase):
    id: int
    is_current: bool
    is_active: bool

    model_config = {
        "from_attributes": True
    }
