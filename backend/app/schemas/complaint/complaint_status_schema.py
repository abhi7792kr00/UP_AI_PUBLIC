from pydantic import BaseModel
from pydantic import ConfigDict


class ComplaintStatusBase(
    BaseModel,
):
    status_name: str

    status_code: str

    display_order: int = 1

    is_final: bool = False

    allow_reopen: bool = False

    color: str | None = None

    description: str | None = None


class ComplaintStatusCreate(
    ComplaintStatusBase,
):
    pass


class ComplaintStatusUpdate(
    BaseModel,
):
    status_name: str | None = None

    status_code: str | None = None

    display_order: int | None = None

    is_final: bool | None = None

    allow_reopen: bool | None = None

    color: str | None = None

    description: str | None = None


class ComplaintStatusResponse(
    ComplaintStatusBase,
):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )