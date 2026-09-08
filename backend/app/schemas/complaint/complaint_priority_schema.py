from pydantic import BaseModel
from pydantic import ConfigDict


class ComplaintPriorityBase(
    BaseModel,
):
    priority_name: str

    priority_code: str

    sla_days: int

    color: str | None = None

    description: str | None = None


class ComplaintPriorityCreate(
    ComplaintPriorityBase,
):
    pass


class ComplaintPriorityUpdate(
    BaseModel,
):
    priority_name: str | None = None

    priority_code: str | None = None

    sla_days: int | None = None

    color: str | None = None

    description: str | None = None


class ComplaintPriorityResponse(
    ComplaintPriorityBase,
):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )