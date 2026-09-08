from datetime import date
from typing import Optional

from pydantic import BaseModel


class CitizenBase(BaseModel):
    user_id: int

    father_name: Optional[str] = None
    mother_name: Optional[str] = None

    gender: Optional[str] = None
    dob: Optional[date] = None

    address: str
    pincode: Optional[str] = None

    state_id: int
    district_id: int

    tehsil_id: Optional[int] = None
    block_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None
    village_id: Optional[int] = None

    municipal_body_id: Optional[int] = None
    ward_id: Optional[int] = None
    locality_id: Optional[int] = None


class CitizenCreate(CitizenBase):
    pass


class CitizenUpdate(BaseModel):
    father_name: Optional[str] = None
    mother_name: Optional[str] = None

    gender: Optional[str] = None
    dob: Optional[date] = None

    address: Optional[str] = None
    pincode: Optional[str] = None

    state_id: Optional[int] = None
    district_id: Optional[int] = None

    tehsil_id: Optional[int] = None
    block_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None
    village_id: Optional[int] = None

    municipal_body_id: Optional[int] = None
    ward_id: Optional[int] = None
    locality_id: Optional[int] = None


class CitizenResponse(CitizenBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }