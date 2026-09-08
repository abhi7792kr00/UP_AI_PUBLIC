from typing import Optional

from pydantic import BaseModel


class LocalityBase(BaseModel):
    locality_name: str
    locality_code: str

    ward_id: int

    pincode: Optional[str] = None


class LocalityCreate(LocalityBase):
    pass


class LocalityUpdate(BaseModel):
    locality_name: Optional[str] = None
    locality_code: Optional[str] = None

    ward_id: Optional[int] = None

    pincode: Optional[str] = None


class LocalityResponse(LocalityBase):
    id: int

    is_active: bool

    created_at: str
    updated_at: str

    model_config = {
        "from_attributes": True
    }