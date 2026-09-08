from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DivisionBase(BaseModel):
    state_id: int

    division_name: str

    division_code: str


class DivisionCreate(DivisionBase):
    pass


class DivisionUpdate(BaseModel):
    state_id: Optional[int] = None

    division_name: Optional[str] = None

    division_code: Optional[str] = None

    is_active: Optional[bool] = None


class DivisionResponse(DivisionBase):
    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }