from typing import Optional

from pydantic import BaseModel


class ReferenceTypeBase(BaseModel):
    module_name: str

    module_code: str

    description: Optional[str] = None


class ReferenceTypeCreate(
    ReferenceTypeBase
):
    pass


class ReferenceTypeUpdate(BaseModel):
    module_name: Optional[str] = None

    module_code: Optional[str] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None


class ReferenceTypeResponse(
    ReferenceTypeBase
):
    id: int

    is_active: bool

    created_at: str

    updated_at: str

    model_config = {
        "from_attributes": True
    }