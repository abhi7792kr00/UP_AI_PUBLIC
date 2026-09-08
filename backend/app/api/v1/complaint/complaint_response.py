from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ComplaintResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    complaint_number: str

    citizen_id: int

    category_id: int
    priority_id: int
    status_id: int

    department_id: int
    office_id: int

    subject: str
    description: str

    address: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    source: str | None = None
    language: str | None = None

    is_public: bool

    created_at: datetime
    updated_at: datetime