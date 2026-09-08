from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class MunicipalBodyType(str, Enum):
    NAGAR_NIGAM = "NAGAR_NIGAM"
    NAGAR_PALIKA_PARISHAD = "NAGAR_PALIKA_PARISHAD"
    NOTIFIED_AREA_COUNCIL = "NOTIFIED_AREA_COUNCIL"
    NAGAR_PANCHAYAT = "NAGAR_PANCHAYAT"
    CANTONMENT_BOARD = "CANTONMENT_BOARD"


class MunicipalBodyBase(BaseModel):
    body_name: str
    body_code: str
    body_type: MunicipalBodyType

    district_id: int

    headquarters: Optional[str] = None


class MunicipalBodyCreate(MunicipalBodyBase):
    pass


class MunicipalBodyUpdate(BaseModel):
    body_name: Optional[str] = None
    body_code: Optional[str] = None
    body_type: Optional[MunicipalBodyType] = None

    district_id: Optional[int] = None

    headquarters: Optional[str] = None


class MunicipalBodyResponse(MunicipalBodyBase):
    id: int

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }