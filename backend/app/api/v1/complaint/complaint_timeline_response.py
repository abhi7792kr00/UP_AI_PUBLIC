from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class ComplaintTimelineResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int

    workflow_definition_id: int

    workflow_step_id: int

    reference_number: str

    action: str

    remarks: str | None = None

    performed_by: int | None = None

    created_at: datetime

    updated_at: datetime
