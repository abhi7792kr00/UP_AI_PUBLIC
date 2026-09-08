from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class StateBase(BaseModel):
    state_name: str

    state_code: str


class StateCreate(StateBase):
    pass


class StateUpdate(BaseModel):
    state_name: Optional[str] = None

    state_code: Optional[str] = None

    is_active: Optional[bool] = None


class StateResponse(StateBase):
    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }