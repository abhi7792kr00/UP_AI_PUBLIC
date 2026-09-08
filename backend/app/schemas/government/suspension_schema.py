from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict


class SuspensionCreate(BaseModel):
    suspension_order_no: str
    suspension_date: date
    officer_id: int
    reason: str
    duration_days: int
    status: str


class SuspensionResponse(BaseModel):
    suspension_order_no: str
    suspension_date: date
    officer_id: int
    reason: str
    duration_days: int
    status: str
    id: int
    is_active: bool

class SuspensionUpdate(BaseModel):
    suspension_order_no: str | None = None
    suspension_date: date | None = None
    officer_id: int | None = None
    reason: str | None = None
    duration_days: int | None = None
    status: str | None = None    

    model_config = ConfigDict(from_attributes=True)