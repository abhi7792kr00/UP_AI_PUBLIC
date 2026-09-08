from datetime import datetime

from pydantic import BaseModel


class OfficerComplaintResponse(BaseModel):
    id: int
    complaint_number: str

    citizen_id: int

    category_id: int
    subcategory_id: int | None

    priority_id: int
    status_id: int

    department_id: int
    office_id: int

    subject: str
    description: str

    address: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    due_date: datetime | None = None
    closed_at: datetime | None = None

    source: str | None = None
    language: str | None = None

    is_public: bool
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }