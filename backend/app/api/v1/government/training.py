from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.database import get_db

from app.schemas.government.training_schema import (
    TrainingCreate,
    TrainingResponse,
    TrainingUpdate,
)

from app.services.government.training_service import (
    create_training_service,
    get_trainings_service,
    read_training_service,
    update_training_service,
    delete_training_service,
)

router = APIRouter(
    prefix="/trainings",
    tags=["Training"],
)


@router.post(
    "/",
    response_model=TrainingResponse,
)
def create_new_training(
    training: TrainingCreate,
    db: Session = Depends(get_db),
):
    return create_training_service(
        db,
        training,
    )


@router.get(
    "/",
    response_model=list[TrainingResponse],
)
def read_trainings(
    db: Session = Depends(get_db),
):
    return get_trainings_service(
        db,
    )


@router.get(
    "/{training_id}",
    response_model=TrainingResponse,
)
def read_training_by_id(
    training_id: int,
    db: Session = Depends(get_db),
):
    return read_training_service(
        db,
        training_id,
    )


@router.put(
    "/{training_id}",
    response_model=TrainingResponse,
)
def update_existing_training(
    training_id: int,
    training: TrainingUpdate,
    db: Session = Depends(get_db),
):
    return update_training_service(
        db,
        training_id,
        training,
    )


@router.delete(
    "/{training_id}",
    response_model=TrainingResponse,
)
def delete_existing_training(
    training_id: int,
    db: Session = Depends(get_db),
):
    return delete_training_service(
        db,
        training_id,
    )