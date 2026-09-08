from datetime import date

from pydantic import BaseModel
from pydantic import ConfigDict


class TrainingCreate(BaseModel):
    training_order_no: str
    officer_id: int
    training_name: str
    institute_name: str
    start_date: date
    end_date: date
    duration_days: int
    certificate_no: str
    remarks: str | None = None
    status: str


class TrainingResponse(BaseModel):
    training_order_no: str
    officer_id: int
    training_name: str
    institute_name: str
    start_date: date
    end_date: date
    duration_days: int
    certificate_no: str
    remarks: str | None = None
    status: str
    id: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True,
    )


class TrainingUpdate(BaseModel):
    training_order_no: str | None = None
    officer_id: int | None = None
    training_name: str | None = None
    institute_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    duration_days: int | None = None
    certificate_no: str | None = None
    remarks: str | None = None
    status: str | None = None

    model_config = ConfigDict(
        from_attributes=True,
    )
class TrainingUpdate(BaseModel):
    training_order_no: str | None = None
    officer_id: int | None = None
    training_name: str | None = None
    institute_name: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    duration_days: int | None = None
    certificate_no: str | None = None
    remarks: str | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)