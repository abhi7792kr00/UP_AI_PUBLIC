from typing import Generic
from typing import Type
from typing import TypeVar

from sqlalchemy.orm import Session

from core.database.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)


class BaseRepository(
    Generic[ModelType]
):
    def __init__(
        self,
        model: Type[ModelType],
    ):
        self.model = model

    def get_all(
        self,
        db: Session,
    ):
        return (
            db.query(self.model)
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        obj_id: int,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.id == obj_id
            )
            .first()
        )

    def create(
        self,
        db: Session,
        obj: ModelType,
    ):
        db.add(obj)
        return obj

    def update(
        self,
        db: Session,
        obj: ModelType,
    ):
        db.add(obj)
        return obj

    def delete(
        self,
        db: Session,
        obj: ModelType,
    ):
        db.delete(obj)

    def exists(
        self,
        db: Session,
        obj_id: int,
    ):
        return (
            db.query(self.model)
            .filter(
                self.model.id == obj_id
            )
            .first()
            is not None
        )

    def count(
        self,
        db: Session,
    ):
        return (
            db.query(self.model)
            .count()
        )