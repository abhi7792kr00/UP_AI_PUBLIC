from typing import Optional

from pydantic import BaseModel


class WorkflowTransitionBase(BaseModel):
    workflow_definition_id: int

    from_step_id: int

    to_step_id: int

    transition_name: str

    transition_code: str

    description: Optional[str] = None

    requires_remark: bool = False

    requires_attachment: bool = False


class WorkflowTransitionCreate(
    WorkflowTransitionBase
):
    pass


class WorkflowTransitionUpdate(BaseModel):
    transition_name: Optional[str] = None

    transition_code: Optional[str] = None

    description: Optional[str] = None

    requires_remark: Optional[bool] = None

    requires_attachment: Optional[bool] = None

    is_active: Optional[bool] = None


class WorkflowTransitionResponse(
    WorkflowTransitionBase
):
    id: int

    is_active: bool

    created_at: str

    updated_at: str

    model_config = {
        "from_attributes": True
    }