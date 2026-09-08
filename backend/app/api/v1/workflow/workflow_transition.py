from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.workflow import (
    WorkflowTransitionCreate,
    WorkflowTransitionUpdate,
    WorkflowTransitionResponse,
)

from app.services.workflow import (
    workflow_transition_service,
)

from database.models.workflow.workflow_transition import (
    WorkflowTransition,
)


router = APIRouter(
    prefix="/workflow-transitions",
    tags=["Workflow Transition"],
)


@router.get(
    "/",
    response_model=List[
        WorkflowTransitionResponse
    ],
)
def get_transitions(
    db: Session = Depends(get_db),
):
    return workflow_transition_service.get_all(
        db,
    )


@router.get(
    "/{transition_id}",
    response_model=WorkflowTransitionResponse,
)
def get_transition(
    transition_id: int,
    db: Session = Depends(get_db),
):
    transition = (
        workflow_transition_service.get_by_id(
            db,
            transition_id,
        )
    )

    if transition is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow transition not found",
        )

    return transition


@router.post(
    "/",
    response_model=WorkflowTransitionResponse,
)
def create_transition(
    transition: WorkflowTransitionCreate,
    db: Session = Depends(get_db),
):
    obj = WorkflowTransition(
        **transition.model_dump()
    )

    return workflow_transition_service.create(
        db,
        obj,
    )


@router.put(
    "/{transition_id}",
    response_model=WorkflowTransitionResponse,
)
def update_transition(
    transition_id: int,
    transition: WorkflowTransitionUpdate,
    db: Session = Depends(get_db),
):
    obj = (
        workflow_transition_service.get_by_id(
            db,
            transition_id,
        )
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow transition not found",
        )

    update_data = transition.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return workflow_transition_service.update(
        db,
        obj,
    )


@router.delete(
    "/{transition_id}",
)
def delete_transition(
    transition_id: int,
    db: Session = Depends(get_db),
):
    obj = (
        workflow_transition_service.get_by_id(
            db,
            transition_id,
        )
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow transition not found",
        )

    workflow_transition_service.delete(
        db,
        obj,
    )

    return {
        "message":
        "Workflow transition deleted successfully"
    }