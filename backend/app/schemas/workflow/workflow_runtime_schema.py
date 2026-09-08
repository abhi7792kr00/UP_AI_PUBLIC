from typing import Optional

from pydantic import BaseModel


class WorkflowExecuteRequest(BaseModel):
    reference_number: str

    workflow_id: int

    current_step_id: int

    next_step_id: int

    performed_by: int

    remarks: Optional[str] = None

    attachment: Optional[str] = None


class WorkflowExecuteResponse(BaseModel):
    success: bool

    message: str

    current_step_id: int