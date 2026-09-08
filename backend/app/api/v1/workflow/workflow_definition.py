from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.workflow import (
    WorkflowDefinitionCreate,
    WorkflowDefinitionUpdate,
    WorkflowDefinitionResponse,
)

from app.services.workflow import (
    workflow_definition_service,
)

from database.models.workflow.workflow_definition import (
    WorkflowDefinition,
)


router = APIRouter(
    prefix="/workflow-definitions",
    tags=["Workflow Definition"],
)


@router.get(
    "/",
    response_model=List[
        WorkflowDefinitionResponse
    ],
)
def get_workflows(
    db: Session = Depends(get_db),
):
    return workflow_definition_service.get_all(
        db,
    )


@router.get(
    "/{workflow_id}",
    response_model=WorkflowDefinitionResponse,
)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    workflow = (
        workflow_definition_service.get_by_id(
            db,
            workflow_id,
        )
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    return workflow


@router.post(
    "/",
    response_model=WorkflowDefinitionResponse,
)
def create_workflow(
    workflow: WorkflowDefinitionCreate,
    db: Session = Depends(get_db),
):
    obj = WorkflowDefinition(
        **workflow.model_dump()
    )

    return workflow_definition_service.create(
        db,
        obj,
    )


@router.put(
    "/{workflow_id}",
    response_model=WorkflowDefinitionResponse,
)
def update_workflow(
    workflow_id: int,
    workflow: WorkflowDefinitionUpdate,
    db: Session = Depends(get_db),
):
    obj = workflow_definition_service.get_by_id(
        db,
        workflow_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    update_data = workflow.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return workflow_definition_service.update(
        db,
        obj,
    )


@router.delete(
    "/{workflow_id}",
)
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
):
    obj = workflow_definition_service.get_by_id(
        db,
        workflow_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found",
        )

    workflow_definition_service.delete(
        db,
        obj,
    )

    return {
        "message":
        "Workflow deleted successfully"
    }