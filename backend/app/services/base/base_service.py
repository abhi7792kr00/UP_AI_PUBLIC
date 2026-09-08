from typing import Generic
from typing import TypeVar

from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository


RepositoryType = TypeVar(
    "RepositoryType",
    bound=BaseRepository,
)


class BaseService(
    Generic[RepositoryType]
):
    def __init__(
        self,
        repository: RepositoryType,
    ):
        self.repository = repository

    def get_all(
        self,
        db: Session,
    ):
        return self.repository.get_all(db)

    def get_by_id(
        self,
        db: Session,
        obj_id: int,
    ):
        return self.repository.get_by_id(
            db,
            obj_id,
        )

    def exists(
        self,
        db: Session,
        obj_id: int,
    ):
        return self.repository.exists(
            db,
            obj_id,
        )

    def count(
        self,
        db: Session,
    ):
        return self.repository.count(db)

    def create(
        self,
        db: Session,
        obj,
    ):
        self.repository.create(
            db,
            obj,
        )

        db.commit()
        db.refresh(obj)

        return obj

    def update(
        self,
        db: Session,
        obj,
    ):
        self.repository.update(
            db,
            obj,
        )

        db.commit()
        db.refresh(obj)

        return obj

    def delete(
        self,
        db: Session,
        obj,
    ):
        self.repository.delete(
            db,
            obj,
        )

        db.commit()

    def rollback(
        self,
        db: Session,
    ):
        db.rollback()