from sqlalchemy.orm import Session

from database.models.government.training import Training

from app.schemas.government.training_schema import (
    TrainingCreate,
    TrainingUpdate,
)


def create_training(
    db: Session,
    training: TrainingCreate,
):
    db_training = Training(**training.model_dump())

    db.add(db_training)
    db.commit()
    db.refresh(db_training)

    return db_training


def get_trainings(
    db: Session,
):
    return db.query(Training).all()


def get_training(
    db: Session,
    training_id: int,
):
    return (
        db.query(Training)
        .filter(Training.id == training_id)
        .first()
    )


def update_training(
    db: Session,
    training_id: int,
    training: TrainingUpdate,
):
    db_training = get_training(
        db,
        training_id,
    )

    if db_training is None:
        return None

    update_data = training.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            db_training,
            key,
            value,
        )

    db.commit()
    db.refresh(db_training)

    return db_training


def delete_training(
    db: Session,
    training_id: int,
):
    db_training = get_training(
        db,
        training_id,
    )

    if db_training is None:
        return None

    db.delete(db_training)
    db.commit()

    return db_training