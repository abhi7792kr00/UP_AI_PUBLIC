from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WardBase(BaseModel):
    ward_name: str
    ward_number: int

    municipal_body_id: int

    population: Optional[int] = None


class WardCreate(WardBase):
    pass


class WardUpdate(BaseModel):
    ward_name: Optional[str] = None
    ward_number: Optional[int] = None

    municipal_body_id: Optional[int] = None

    population: Optional[int] = None


class WardResponse(WardBase):
    id: int

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }