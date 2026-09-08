from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.reference.reference_format import (
    ReferenceFormat,
)


class ReferenceFormatRepository(
    BaseRepository[ReferenceFormat]
):
    def __init__(self):
        super().__init__(
            ReferenceFormat
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_by_prefix(
        self,
        db: Session,
        prefix: str,
    ) -> ReferenceFormat | None:
        return (
            db.query(
                ReferenceFormat
            )
            .filter(
                ReferenceFormat.prefix
                == prefix
            )
            .first()
        )

    def get_active_by_type(
        self,
        db: Session,
        reference_type_id: int,
    ) -> list[ReferenceFormat]:
        return (
            db.query(
                ReferenceFormat
            )
            .filter(
                ReferenceFormat.reference_type_id
                == reference_type_id,
                ReferenceFormat.is_active.is_(True),
            )
            .all()
        )

    def get_by_type_and_name(
        self,
        db: Session,
        reference_type_id: int,
        format_name: str,
    ) -> ReferenceFormat | None:
        return (
            db.query(
                ReferenceFormat
            )
            .filter(
                ReferenceFormat.reference_type_id
                == reference_type_id,
                ReferenceFormat.format_name
                == format_name,
            )
            .first()
        )

    # ---------------------------------
    # Validation Methods
    # ---------------------------------

    def exists_by_prefix(
        self,
        db: Session,
        prefix: str,
    ) -> bool:
        return (
            db.query(
                ReferenceFormat
            )
            .filter(
                ReferenceFormat.prefix
                == prefix
            )
            .first()
            is not None
        )


reference_format_repository = (
    ReferenceFormatRepository()
)