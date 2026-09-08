from typing import Optional

from pydantic import BaseModel


class ReferenceFormatBase(BaseModel):
    reference_type_id: int

    format_name: str

    prefix: str

    separator: str = "-"

    sequence_length: int = 6

    description: Optional[str] = None


class ReferenceFormatCreate(
    ReferenceFormatBase
):
    pass


class ReferenceFormatUpdate(BaseModel):
    format_name: Optional[str] = None

    prefix: Optional[str] = None

    separator: Optional[str] = None

    sequence_length: Optional[int] = None

    description: Optional[str] = None

    is_active: Optional[bool] = None


class ReferenceFormatResponse(
    ReferenceFormatBase
):
    id: int

    is_active: bool

    created_at: str

    updated_at: str

    model_config = {
        "from_attributes": True
    }