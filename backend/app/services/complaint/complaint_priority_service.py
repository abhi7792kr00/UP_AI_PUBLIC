from sqlalchemy.orm import Session

from app.repositories.complaint import (
    complaint_priority_repository,
)

from app.services.base.base_service import BaseService


class ComplaintPriorityService(
    BaseService
):
    def __init__(self):
        super().__init__(
            complaint_priority_repository
        )

    def get_by_code(
        self,
        db: Session,
        code: str,
    ):
        return self.repository.get_by_code(
            db,
            code,
        )

    def get_by_name(
        self,
        db: Session,
        name: str,
    ):
        return self.repository.get_by_name(
            db,
            name,
        )

    def get_by_sla(
        self,
        db: Session,
        sla_days: int,
    ):
        return self.repository.get_by_sla(
            db,
            sla_days,
        )

    def get_default_priority(
        self,
        db: Session,
    ):
        return self.repository.get_default_priority(
            db,
        )


complaint_priority_service = (
    ComplaintPriorityService()
)