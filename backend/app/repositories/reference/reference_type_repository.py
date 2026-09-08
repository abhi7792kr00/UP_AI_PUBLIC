from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.reference.reference_type import (
    ReferenceType,
)


class ReferenceTypeRepository(
    BaseRepository[ReferenceType]
):
    def __init__(self):
        super().__init__(
            ReferenceType
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_by_module_code(
        self,
        db: Session,
        module_code: str,
    ) -> ReferenceType | None:
        return (
            db.query(
                ReferenceType
            )
            .filter(
                ReferenceType.module_code
                == module_code
            )
            .first()
        )

    def get_active(
        self,
        db: Session,
    ) -> list[ReferenceType]:
        return (
            db.query(
                ReferenceType
            )
            .filter(
                ReferenceType.is_active.is_(True)
            )
            .all()
        )

    # ---------------------------------
    # Validation Methods
    # ---------------------------------

    def exists_by_module_code(
        self,
        db: Session,
        module_code: str,
    ) -> bool:
        return (
            db.query(
                ReferenceType
            )
            .filter(
                ReferenceType.module_code
                == module_code
            )
            .first()
            is not None
        )


reference_type_repository = (
    ReferenceTypeRepository()
)