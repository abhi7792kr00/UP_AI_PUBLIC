from sqlalchemy.orm import Session

from app.repositories.government import leave_repository
from app.schemas.government.leave_schema import (
    LeaveCreate,
    LeaveUpdate,
)
from database.models.government.leave import Leave


def get_leaves(db: Session):
    return leave_repository.get_all(db)


def get_leave(
    db: Session,
    leave_id: int,
):
    return leave_repository.get_by_id(
        db,
        leave_id,
    )


def create_leave(
    db: Session,
    leave_data: LeaveCreate,
):
    leave = Leave(
        leave_order_no=leave_data.leave_order_no,
        leave_type=leave_data.leave_type,
        start_date=leave_data.start_date,
        end_date=leave_data.end_date,
        total_days=leave_data.total_days,
        reason=leave_data.reason,
        status=leave_data.status,
        approved_by=leave_data.approved_by,
        officer_id=leave_data.officer_id,
        remarks=leave_data.remarks,
    )

    return leave_repository.create(
        db,
        leave,
    )


def update_leave(
    db: Session,
    leave_id: int,
    leave_data: LeaveUpdate,
):
    leave = leave_repository.get_by_id(
        db,
        leave_id,
    )

    if not leave:
        return None

    update_data = leave_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            leave,
            key,
            value,
        )

    db.commit()
    db.refresh(leave)

    return leave


def delete_leave(
    db: Session,
    leave_id: int,
):
    leave = leave_repository.get_by_id(
        db,
        leave_id,
    )

    if not leave:
        return False

    leave_repository.delete(
        db,
        leave,
    )

    return True