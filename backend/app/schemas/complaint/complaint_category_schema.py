from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ComplaintCategoryBase(BaseModel):
    category_name: str

    category_code: str

    description: Optional[str] = None

    icon: Optional[str] = None

    color: Optional[str] = None


class ComplaintCategoryCreate(
    ComplaintCategoryBase
):
    pass


class ComplaintCategoryUpdate(BaseModel):
    category_name: Optional[str] = None

    category_code: Optional[str] = None

    description: Optional[str] = None

    icon: Optional[str] = None

    color: Optional[str] = None

    is_active: Optional[bool] = None


class ComplaintCategoryResponse(
    ComplaintCategoryBase
):
    id: int

    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
