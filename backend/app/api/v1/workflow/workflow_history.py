from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.workflow import (
    WorkflowHistoryCreate,
    WorkflowHistoryUpdate,
    WorkflowHistoryResponse,
)

from app.services.workflow import (
    workflow_history_service,
)

from database.models.workflow.workflow_history import (
    WorkflowHistory,
)


router = APIRouter(
    prefix="/workflow-history",
    tags=["Workflow History"],
)


@router.get(
    "/",
    response_model=List[WorkflowHistoryResponse],
)
def get_history(
    db: Session = Depends(get_db),
):
    return workflow_history_service.get_all(db)


@router.get(
    "/{history_id}",
    response_model=WorkflowHistoryResponse,
)
def get_history_by_id(
    history_id: int,
    db: Session = Depends(get_db),
):
    history = workflow_history_service.get_by_id(
        db,
        history_id,
    )

    if history is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow history not found",
        )

    return history


@router.post(
    "/",
    response_model=WorkflowHistoryResponse,
)
def create_history(
    history: WorkflowHistoryCreate,
    db: Session = Depends(get_db),
):
    obj = WorkflowHistory(
        **history.model_dump()
    )

    return workflow_history_service.create(
        db,
        obj,
    )


@router.put(
    "/{history_id}",
    response_model=WorkflowHistoryResponse,
)
def update_history(
    history_id: int,
    history: WorkflowHistoryUpdate,
    db: Session = Depends(get_db),
):
    obj = workflow_history_service.get_by_id(
        db,
        history_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow history not found",
        )

    update_data = history.model_dump(
        exclude_unset=True,
    )

    for key, value in update_data.items():
        setattr(
            obj,
            key,
            value,
        )

    return workflow_history_service.update(
        db,
        obj,
    )


@router.delete(
    "/{history_id}",
)
def delete_history(
    history_id: int,
    db: Session = Depends(get_db),
):
    obj = workflow_history_service.get_by_id(
        db,
        history_id,
    )

    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow history not found",
        )

    workflow_history_service.delete(
        db,
        obj,
    )

    return {
        "message":
        "Workflow history deleted successfully"
    }