from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.workflow import (
    WorkflowStepCreate,
    WorkflowStepUpdate,
    WorkflowStepResponse,
)

from app.services.workflow import (
    workflow_step_service,
)

from database.models.workflow.workflow_step import (
    WorkflowStep,
)


router = APIRouter(
    prefix="/workflow-steps",
    tags=["Workflow Step"],
)


@router.get(
    "/",
    response_model=List[
        WorkflowStepResponse
    ],
)
def get_steps(
    db: Session = Depends(get_db),
):
    return workflow_step_service.get_all(
        db,
    )


@router.get(
    "/{step_id}",
    response_model=WorkflowStepResponse,
)
def get_step(
    step_id: int,
    db: Session = Depends(get_db),
):
    step = workflow_step_service.get_by_id(
        db,
        step_id,
    )

    if step is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow step not found",
        )

    return step


@router.post(
    "/",
    response_model=WorkflowStepResponse,
)
def create_step(
    step: WorkflowStepCreate,
    db: Session = Depends(get_db),
):
    obj = WorkflowStep(
        **step.model_dump()
    )

    return workflow_step_service.create(
        db,
        obj,
    )


@router.put(
    "/{step_id}",
    response_model=WorkflowStepResponse,
)
def update_step(
    step_id: int,
    step: WorkflowStepUpdate,
    db: Session = Depends(get_db),
):
    obj = workflow_step_service.get_by_id(
        db,
        step_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow step not found",
        )

    update_data = step.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return workflow_step_service.update(
        db,
        obj,
    )


@router.delete(
    "/{step_id}",
)
def delete_step(
    step_id: int,
    db: Session = Depends(get_db),
):
    obj = workflow_step_service.get_by_id(
        db,
        step_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow step not found",
        )

    workflow_step_service.delete(
        db,
        obj,
    )

    return {
        "message":
        "Workflow step deleted successfully"
    }