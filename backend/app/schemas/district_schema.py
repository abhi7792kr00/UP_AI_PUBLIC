from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class DistrictBase(BaseModel):
    division_id: int

    district_name: str

    district_code: str


class DistrictCreate(DistrictBase):
    pass


class DistrictUpdate(BaseModel):
    division_id: Optional[int] = None

    district_name: Optional[str] = None

    district_code: Optional[str] = None

    is_active: Optional[bool] = None


class DistrictResponse(DistrictBase):
    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }