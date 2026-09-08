from typing import Optional

from pydantic import BaseModel


class CitizenComplaintCreate(BaseModel):

    category_id: int
    subcategory_id: Optional[int] = None

    subject: str
    description: str

    priority_id: Optional[int] = None

    state_id: int
    division_id: Optional[int] = None
    district_id: int

    tehsil_id: Optional[int] = None
    block_id: Optional[int] = None
    gram_panchayat_id: Optional[int] = None
    village_id: Optional[int] = None

    municipal_body_id: Optional[int] = None
    ward_id: Optional[int] = None
    locality_id: Optional[int] = None

    address: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    pincode: Optional[str] = None

    mobile_number: Optional[str] = None
    email: Optional[str] = None

    has_attachment: bool = False

    source: str = "WEB"
    language: Optional[str] = None

    visibility: str = "PUBLIC"
