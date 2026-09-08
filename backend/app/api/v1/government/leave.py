from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.leave_schema import (
    LeaveCreate,
    LeaveUpdate,
    LeaveResponse,
)

from app.services.government.leave_service import (
    get_leaves,
    get_leave,
    create_leave,
    update_leave,
    delete_leave,
)

router = APIRouter(
    prefix="/leaves",
    tags=["Leave"],
)


@router.get(
    "/",
    response_model=list[LeaveResponse],
)
def read_leaves(
    db: Session = Depends(get_db),
):
    return get_leaves(db)


@router.get(
    "/{leave_id}",
    response_model=LeaveResponse,
)
def read_leave(
    leave_id: int,
    db: Session = Depends(get_db),
):
    leave = get_leave(
        db,
        leave_id,
    )

    if not leave:
        raise HTTPException(
            status_code=404,
            detail="Leave not found",
        )

    return leave


@router.post(
    "/",
    response_model=LeaveResponse,
)
def create_new_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db),
):
    return create_leave(
        db,
        leave,
    )


@router.put(
    "/{leave_id}",
    response_model=LeaveResponse,
)
def update_existing_leave(
    leave_id: int,
    leave: LeaveUpdate,
    db: Session = Depends(get_db),
):
    updated = update_leave(
        db,
        leave_id,
        leave,
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Leave not found",
        )

    return updated


@router.delete(
    "/{leave_id}",
)
def delete_existing_leave(
    leave_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_leave(
        db,
        leave_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Leave not found",
        )

    return {
        "message": "Leave deleted successfully"
    }