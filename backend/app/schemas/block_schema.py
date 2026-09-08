from datetime import datetime

from pydantic import BaseModel, Field


class BlockBase(BaseModel):
    block_name: str
    block_code: str


class BlockCreate(BlockBase):
    tehsil_ids: list[int] = Field(
        default_factory=list,
    )


class BlockUpdate(BaseModel):
    block_name: str | None = None
    block_code: str | None = None
    tehsil_ids: list[int] | None = None
    is_active: bool | None = None


class BlockResponse(BlockBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    tehsil_ids: list[int] = Field(
        default_factory=list,
    )

    model_config = {
        "from_attributes": True,
    }
