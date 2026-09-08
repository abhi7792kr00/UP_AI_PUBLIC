from sqlalchemy.orm import Session

from database.models.government.suspension import Suspension

from app.schemas.government.suspension_schema import (
    SuspensionCreate,
    SuspensionUpdate,
)


class SuspensionRepository:

    @staticmethod
    def create(
        db: Session,
        suspension: SuspensionCreate,
    ):
        db_suspension = Suspension(
            **suspension.model_dump()
        )

        db.add(db_suspension)
        db.commit()
        db.refresh(db_suspension)

        return db_suspension

    @staticmethod
    def get_all(
        db: Session,
    ):
        return (
            db.query(Suspension)
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        suspension_id: int,
    ):
        return (
            db.query(Suspension)
            .filter(
                Suspension.id == suspension_id
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        suspension_id: int,
        suspension: SuspensionUpdate,
    ):
        db_suspension = (
            db.query(Suspension)
            .filter(
                Suspension.id == suspension_id
            )
            .first()
        )

        if not db_suspension:
            return None

        update_data = suspension.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                db_suspension,
                key,
                value,
            )

        db.commit()
        db.refresh(db_suspension)

        return db_suspension

    @staticmethod
    def delete(
        db: Session,
        suspension_id: int,
    ):
        db_suspension = (
            db.query(Suspension)
            .filter(
                Suspension.id == suspension_id
            )
            .first()
        )

        if not db_suspension:
            return None

        db.delete(db_suspension)
        db.commit()

        return db_suspension