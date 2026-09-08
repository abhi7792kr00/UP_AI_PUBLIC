from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class VillageBase(BaseModel):
    gram_panchayat_id: Optional[int] = None

    village_name: str

    village_code: str


class VillageCreate(VillageBase):
    pass


class VillageUpdate(BaseModel):
    gram_panchayat_id: Optional[int] = None

    village_name: Optional[str] = None

    village_code: Optional[str] = None

    is_active: Optional[bool] = None


class VillageResponse(VillageBase):
    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
