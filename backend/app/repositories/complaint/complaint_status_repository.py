from sqlalchemy.orm import Session

from app.repositories.base.base_repository import (
    BaseRepository,
)

from database.models.complaint.complaint_status import (
    ComplaintStatus,
)


class ComplaintStatusRepository(
    BaseRepository[ComplaintStatus]
):
    def __init__(self):
        super().__init__(
            ComplaintStatus
        )

    def get_by_code(
        self,
        db: Session,
        code: str,
    ):
        return (
            db.query(
                ComplaintStatus
            )
            .filter(
                ComplaintStatus.status_code == code
            )
            .first()
        )

    def get_by_name(
        self,
        db: Session,
        name: str,
    ):
        return (
            db.query(
                ComplaintStatus
            )
            .filter(
                ComplaintStatus.status_name == name
            )
            .first()
        )

    def get_initial_status(
        self,
        db: Session,
    ):
        return (
            db.query(
                ComplaintStatus
            )
            .order_by(
                ComplaintStatus.display_order.asc()
            )
            .first()
        )

    def get_final_status(
        self,
        db: Session,
    ):
        return (
            db.query(
                ComplaintStatus
            )
            .filter(
                ComplaintStatus.is_final.is_(True)
            )
            .all()
        )

    def get_reopen_status(
        self,
        db: Session,
    ):
        return (
            db.query(
                ComplaintStatus
            )
            .filter(
                ComplaintStatus.allow_reopen.is_(True)
            )
            .all()
        )


complaint_status_repository = (
    ComplaintStatusRepository()
)