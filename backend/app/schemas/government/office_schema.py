from typing import Optional

from pydantic import BaseModel


class OfficeBase(BaseModel):
    office_name: str
    office_code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    department_id: int
    district_id: int | None = None
    tehsil_id: int | None = None
    block_id: int | None = None
    municipal_body_id: int | None = None
    ward_id: int | None = None
    locality_id: int | None = None


class OfficeCreate(OfficeBase):
    pass


class OfficeUpdate(BaseModel):
    office_name: Optional[str] = None
    office_code: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    department_id: Optional[int] = None
    district_id: Optional[int] = None
    tehsil_id: Optional[int] = None
    block_id: Optional[int] = None
    municipal_body_id: Optional[int] = None
    ward_id: Optional[int] = None
    locality_id: Optional[int] = None


class OfficeResponse(OfficeBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }