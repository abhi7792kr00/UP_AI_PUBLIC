from datetime import date

from pydantic import BaseModel


class ServiceHistoryResponse(BaseModel):
    event_type: str
    event_date: date
    title: str
    reference_no: str | None = None
    remarks: str | None = None

    model_config = {
        "from_attributes": True
    }