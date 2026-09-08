from typing import Optional

from pydantic import BaseModel


class WorkflowDefinitionBase(BaseModel):
    workflow_name: str

    workflow_code: str

    module_name: str

    description: Optional[str] = None

    is_default: bool = False


class WorkflowDefinitionCreate(
    WorkflowDefinitionBase
):
    pass


class WorkflowDefinitionUpdate(BaseModel):
    workflow_name: Optional[str] = None

    workflow_code: Optional[str] = None

    module_name: Optional[str] = None

    description: Optional[str] = None

    is_default: Optional[bool] = None

    is_active: Optional[bool] = None


class WorkflowDefinitionResponse(
    WorkflowDefinitionBase
):
    id: int

    is_active: bool

    created_at: str

    updated_at: str

    model_config = {
        "from_attributes": True
    }