from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ComplaintTransitionResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    complaint_number: str

    previous_status_id: int
    new_status_id: int

    action: str

    remarks: str | None = None

    performed_by: int | None = None

    transitioned_at: datetime
