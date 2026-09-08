from typing import Optional

from pydantic import BaseModel


class WorkflowStepBase(BaseModel):
    workflow_definition_id: int

    step_name: str

    step_code: str

    step_order: int

    description: Optional[str] = None

    is_initial: bool = False

    is_final: bool = False

    requires_assignment: bool = False

    allows_rejection: bool = False


class WorkflowStepCreate(
    WorkflowStepBase
):
    pass


class WorkflowStepUpdate(BaseModel):
    step_name: Optional[str] = None

    step_code: Optional[str] = None

    step_order: Optional[int] = None

    description: Optional[str] = None

    is_initial: Optional[bool] = None

    is_final: Optional[bool] = None

    requires_assignment: Optional[bool] = None

    allows_rejection: Optional[bool] = None

    is_active: Optional[bool] = None


class WorkflowStepResponse(
    WorkflowStepBase
):
    id: int

    is_active: bool

    created_at: str

    updated_at: str

    model_config = {
        "from_attributes": True
    }