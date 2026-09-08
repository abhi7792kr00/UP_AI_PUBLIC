from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.engines.workflow import (
    WorkflowContext,
)

from app.schemas.workflow import (
    WorkflowExecuteRequest,
    WorkflowExecuteResponse,
)

from app.services.workflow import (
    workflow_runtime_service,
)


router = APIRouter(
    tags=["Workflow Runtime"],
)


@router.post(
    "/execute",
    response_model=WorkflowExecuteResponse,
)
def execute_workflow(
    request: WorkflowExecuteRequest,
    db: Session = Depends(get_db),
):

    context = WorkflowContext(
        workflow=None,
        current_step=None,
        next_step=None,
        transition=None,
        reference_number=request.reference_number,
        remarks=request.remarks,
        attachment=request.attachment,
        performed_by=request.performed_by,
    )

    workflow_runtime_service.execute(
        db,
        context,
    )

    return WorkflowExecuteResponse(
        success=True,
        message="Workflow executed successfully.",
        current_step_id=request.next_step_id,
    )