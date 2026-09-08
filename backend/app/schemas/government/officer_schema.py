from typing import Optional

from pydantic import BaseModel


class OfficerBase(BaseModel):
    officer_name: str
    employee_code: str
    mobile: Optional[str] = None
    email: Optional[str] = None

    department_id: int
    designation_id: int
    office_id: int


class OfficerCreate(OfficerBase):
    pass


class OfficerUpdate(BaseModel):
    officer_name: Optional[str] = None
    employee_code: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[str] = None

    department_id: Optional[int] = None
    designation_id: Optional[int] = None
    office_id: Optional[int] = None


class OfficerResponse(OfficerBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }