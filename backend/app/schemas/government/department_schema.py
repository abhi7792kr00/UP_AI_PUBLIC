from typing import Optional

from pydantic import BaseModel


class DepartmentBase(BaseModel):
    department_name: str
    department_code: str
    description: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    department_code: Optional[str] = None
    description: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    id: int
    is_active: bool

    model_config = {
        "from_attributes": True
    }