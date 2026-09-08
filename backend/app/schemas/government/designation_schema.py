from typing import Optional

from pydantic import BaseModel


class DesignationBase(BaseModel):
    designation_name: str
    designation_code: str
    description: Optional[str] = None
    department_id: int


class DesignationCreate(DesignationBase):
    pass


class DesignationUpdate(BaseModel):
    designation_name: Optional[str] = None
    designation_code: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[int] = None


class DesignationResponse(DesignationBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }