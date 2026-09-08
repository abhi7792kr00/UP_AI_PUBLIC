from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TehsilBase(BaseModel):
    district_id: int

    tehsil_name: str

    tehsil_code: str


class TehsilCreate(TehsilBase):
    pass


class TehsilUpdate(BaseModel):
    district_id: Optional[int] = None

    tehsil_name: Optional[str] = None

    tehsil_code: Optional[str] = None

    is_active: Optional[bool] = None


class TehsilResponse(TehsilBase):
    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }