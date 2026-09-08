from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict


class RetirementCreate(BaseModel):
    retirement_order_no: str
    retirement_date: date
    officer_id: int
    retirement_type: str
    age_at_retirement: int
    pension_status: str
    remarks: str | None = None
    status: str


class RetirementResponse(BaseModel):
    retirement_order_no: str
    retirement_date: date
    officer_id: int
    retirement_type: str
    age_at_retirement: int
    pension_status: str
    remarks: str | None = None
    status: str
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class RetirementUpdate(BaseModel):
    retirement_order_no: str | None = None
    retirement_date: date | None = None
    officer_id: int | None = None
    retirement_type: str | None = None
    age_at_retirement: int | None = None
    pension_status: str | None = None
    remarks: str | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)