from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WorkflowAssignmentBase(BaseModel):
    workflow_definition_id: int

    workflow_step_id: int

    reference_number: str

    assigned_to: int

    assigned_by: Optional[int] = None

    assignment_type: str = "MANUAL"

    remarks: Optional[str] = None

    is_completed: bool = False


class WorkflowAssignmentCreate(
    WorkflowAssignmentBase
):
    pass


class WorkflowAssignmentUpdate(BaseModel):
    assigned_to: Optional[int] = None

    assigned_by: Optional[int] = None

    assignment_type: Optional[str] = None

    remarks: Optional[str] = None

    is_completed: Optional[bool] = None

    is_active: Optional[bool] = None


class WorkflowAssignmentResponse(
    WorkflowAssignmentBase
):
    id: int

    is_active: bool

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True
    }