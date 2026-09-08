from sqlalchemy.orm import Session

from app.repositories.government.training_repository import (
    create_training as repo_create_training,
    get_trainings as repo_get_trainings,
    get_training as repo_get_training,
    update_training as repo_update_training,
    delete_training as repo_delete_training,
)

from app.schemas.government.training_schema import (
    TrainingCreate,
    TrainingUpdate,
)


def create_training_service(
    db: Session,
    training: TrainingCreate,
):
    return repo_create_training(
        db,
        training,
    )


def get_trainings_service(
    db: Session,
):
    return repo_get_trainings(
        db,
    )


def read_training_service(
    db: Session,
    training_id: int,
):
    return repo_get_training(
        db,
        training_id,
    )


def update_training_service(
    db: Session,
    training_id: int,
    training: TrainingUpdate,
):
    return repo_update_training(
        db,
        training_id,
        training,
    )


def delete_training_service(
    db: Session,
    training_id: int,
):
    return repo_delete_training(
        db,
        training_id,
    )