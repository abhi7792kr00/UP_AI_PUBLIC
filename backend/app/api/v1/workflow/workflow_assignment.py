from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.workflow import (
    WorkflowAssignmentCreate,
    WorkflowAssignmentUpdate,
    WorkflowAssignmentResponse,
)

from app.services.workflow import (
    workflow_assignment_service,
)

from database.models.workflow.workflow_assignment import (
    WorkflowAssignment,
)


router = APIRouter(
    prefix="/workflow-assignments",
    tags=["Workflow Assignment"],
)


@router.get(
    "/",
    response_model=List[
        WorkflowAssignmentResponse
    ],
)
def get_assignments(
    db: Session = Depends(get_db),
):
    return workflow_assignment_service.get_all(
        db,
    )


@router.get(
    "/{assignment_id}",
    response_model=WorkflowAssignmentResponse,
)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    assignment = (
        workflow_assignment_service.get_by_id(
            db,
            assignment_id,
        )
    )

    if assignment is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow assignment not found",
        )

    return assignment


@router.post(
    "/",
    response_model=WorkflowAssignmentResponse,
)
def create_assignment(
    assignment: WorkflowAssignmentCreate,
    db: Session = Depends(get_db),
):
    obj = WorkflowAssignment(
        **assignment.model_dump()
    )

    return workflow_assignment_service.create(
        db,
        obj,
    )


@router.put(
    "/{assignment_id}",
    response_model=WorkflowAssignmentResponse,
)
def update_assignment(
    assignment_id: int,
    assignment: WorkflowAssignmentUpdate,
    db: Session = Depends(get_db),
):
    obj = (
        workflow_assignment_service.get_by_id(
            db,
            assignment_id,
        )
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow assignment not found",
        )

    update_data = assignment.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return workflow_assignment_service.update(
        db,
        obj,
    )


@router.delete(
    "/{assignment_id}",
)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    obj = (
        workflow_assignment_service.get_by_id(
            db,
            assignment_id,
        )
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow assignment not found",
        )

    workflow_assignment_service.delete(
        db,
        obj,
    )

    return {
        "message":
        "Workflow assignment deleted successfully"
    }