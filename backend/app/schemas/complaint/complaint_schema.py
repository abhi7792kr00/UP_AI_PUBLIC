from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ComplaintBase(BaseModel):
    citizen_id: int

    category_id: int
    subcategory_id: Optional[int] = None

    subject: str
    description: str

    address: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    source: Optional[str] = None
    language: Optional[str] = None


class ComplaintCreate(ComplaintBase):
    pass


class ComplaintUpdate(BaseModel):
    category_id: Optional[int] = None
    subcategory_id: Optional[int] = None

    subject: Optional[str] = None
    description: Optional[str] = None

    address: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    source: Optional[str] = None
    language: Optional[str] = None


class AssignedOfficerResponse(BaseModel):
    id: int
    officer_name: str
    photo_url: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None
    designation_name: Optional[str] = None
    department_name: Optional[str] = None
    office_name: Optional[str] = None


class ComplaintResponse(ComplaintBase):
    id: int

    complaint_number: str

    priority_id: int
    status_id: int

    department_id: int
    office_id: int

    assigned_officer_id: Optional[int]

    assigned_officer: Optional[AssignedOfficerResponse] = None

    due_date: Optional[datetime]
    closed_at: Optional[datetime]

    is_otp_verified: bool
    is_public: bool

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }