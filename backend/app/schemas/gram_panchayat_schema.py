from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class GramPanchayatBase(
    BaseModel
):
    block_id: int

    gram_panchayat_name: str

    gram_panchayat_code: str


class GramPanchayatCreate(
    GramPanchayatBase
):
    pass


class GramPanchayatUpdate(
    BaseModel
):
    block_id: Optional[int] = None

    gram_panchayat_name: Optional[str] = None

    gram_panchayat_code: Optional[str] = None

    is_active: Optional[bool] = None


class GramPanchayatResponse(
    BaseModel
):
    id: int

    block_id: Optional[int] = None

    gram_panchayat_name: str

    gram_panchayat_code: str

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
