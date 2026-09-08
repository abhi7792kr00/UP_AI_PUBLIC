from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class ComplaintFeedbackCreate(BaseModel):
    rating: int = Field(
        ...,
        ge=1,
        le=5,
    )

    feedback_text: Optional[str] = Field(
        default=None,
        max_length=1000,
    )

    is_satisfied: bool = True


class ComplaintFeedbackResponse(BaseModel):
    id: int

    complaint_id: int
    citizen_id: int

    rating: int
    feedback_text: Optional[str] = None
    is_satisfied: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
