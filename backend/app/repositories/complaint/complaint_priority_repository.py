from sqlalchemy.orm import Session

from app.repositories.base.base_repository import (
    BaseRepository,
)

from database.models.complaint.complaint_priority import (
    ComplaintPriority,
)


class ComplaintPriorityRepository(
    BaseRepository[ComplaintPriority]
):
    def __init__(self):
        super().__init__(
            ComplaintPriority
        )

    def get_by_code(
        self,
        db: Session,
        code: str,
    ):
        return (
            db.query(
                ComplaintPriority
            )
            .filter(
                ComplaintPriority.priority_code == code
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
                ComplaintPriority
            )
            .filter(
                ComplaintPriority.priority_name == name
            )
            .first()
        )

    def get_by_sla(
        self,
        db: Session,
        sla_days: int,
    ):
        return (
            db.query(
                ComplaintPriority
            )
            .filter(
                ComplaintPriority.sla_days == sla_days
            )
            .all()
        )

    def get_default_priority(
        self,
        db: Session,
    ):
        return (
            db.query(
                ComplaintPriority
            )
            .order_by(
                ComplaintPriority.sla_days.asc()
            )
            .first()
        )


complaint_priority_repository = (
    ComplaintPriorityRepository()
)