from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReferenceSequenceBase(BaseModel):
    reference_format_id: int

    sequence_period: str

    period_value: str

    current_sequence: int = 0


class ReferenceSequenceCreate(
    ReferenceSequenceBase
):
    pass


class ReferenceSequenceUpdate(BaseModel):
    current_sequence: Optional[int] = None

    last_generated_at: Optional[
        datetime
    ] = None


class ReferenceSequenceResponse(
    ReferenceSequenceBase
):
    id: int

    last_generated_at: Optional[
        datetime
    ]

    created_at: str

    updated_at: str

    model_config = {
        "from_attributes": True
    }