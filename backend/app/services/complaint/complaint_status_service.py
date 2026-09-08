from sqlalchemy.orm import Session

from app.repositories.complaint import (
    complaint_status_repository,
)

from app.services.base.base_service import (
    BaseService,
)


class ComplaintStatusService(
    BaseService
):
    def __init__(self):
        super().__init__(
            complaint_status_repository
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

    def get_initial_status(
        self,
        db: Session,
    ):
        return self.repository.get_initial_status(
            db,
        )

    def get_final_status(
        self,
        db: Session,
    ):
        return self.repository.get_final_status(
            db,
        )

    def get_reopen_status(
        self,
        db: Session,
    ):
        return self.repository.get_reopen_status(
            db,
        )


complaint_status_service = (
    ComplaintStatusService()
)