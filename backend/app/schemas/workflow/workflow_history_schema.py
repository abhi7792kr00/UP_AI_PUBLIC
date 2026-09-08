from typing import Optional

from pydantic import BaseModel


class WorkflowHistoryBase(BaseModel):
    workflow_definition_id: int

    workflow_step_id: int

    reference_number: str

    action: str

    remarks: Optional[str] = None

    performed_by: Optional[int] = None


class WorkflowHistoryCreate(
    WorkflowHistoryBase
):
    pass


class WorkflowHistoryUpdate(BaseModel):
    remarks: Optional[str] = None

    performed_by: Optional[int] = None

    is_active: Optional[bool] = None


class WorkflowHistoryResponse(
    WorkflowHistoryBase
):
    id: int

    is_active: bool

    created_at: str

    updated_at: str

    model_config = {
        "from_attributes": True
    }