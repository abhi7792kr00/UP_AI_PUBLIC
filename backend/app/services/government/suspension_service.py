from sqlalchemy.orm import Session

from app.repositories.government.suspension_repository import (
    SuspensionRepository,
)

from app.schemas.government.suspension_schema import (
    SuspensionCreate,
    SuspensionUpdate,
)

repository = SuspensionRepository()


def create_suspension(
    db: Session,
    suspension: SuspensionCreate,
):
    return repository.create(
        db,
        suspension,
    )


def get_suspensions(
    db: Session,
):
    return repository.get_all(
        db,
    )


def get_suspension(
    db: Session,
    suspension_id: int,
):
    return repository.get_by_id(
        db,
        suspension_id,
    )


def update_suspension(
    db: Session,
    suspension_id: int,
    suspension: SuspensionUpdate,
):
    return repository.update(
        db,
        suspension_id,
        suspension,
    )


def delete_suspension(
    db: Session,
    suspension_id: int,
):
    return repository.delete(
        db,
        suspension_id,
    )