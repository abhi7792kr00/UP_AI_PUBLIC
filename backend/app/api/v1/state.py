from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.state_schema import (
    StateCreate,
    StateUpdate,
    StateResponse,
)

from app.services.master.state_service import (
    state_service,
)

router = APIRouter(
    prefix="/states",
    tags=["States"],
)


@router.get(
    "/",
    response_model=List[StateResponse],
)
def read_states(
    db: Session = Depends(get_db),
):
    return state_service.get_all(db)


@router.get(
    "/{state_id}",
    response_model=StateResponse,
)
def read_state(
    state_id: int,
    db: Session = Depends(get_db),
):
    obj = state_service.get_by_id(
        db,
        state_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="State not found",
        )

    return obj


@router.post(
    "/",
    response_model=StateResponse,
)
def create_state(
    state: StateCreate,
    db: Session = Depends(get_db),
):
    return state_service.create(
        db,
        state,
    )


@router.put(
    "/{state_id}",
    response_model=StateResponse,
)
def update_state(
    state_id: int,
    state: StateUpdate,
    db: Session = Depends(get_db),
):
    obj = state_service.update(
        db,
        state_id,
        state,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="State not found",
        )

    return obj


@router.delete(
    "/{state_id}",
)
def delete_state(
    state_id: int,
    db: Session = Depends(get_db),
):
    obj = state_service.delete(
        db,
        state_id,
    )

    if not obj:
        raise HTTPException(
            status_code=404,
            detail="State not found",
        )

    return {
        "message": "State deleted successfully"
    }