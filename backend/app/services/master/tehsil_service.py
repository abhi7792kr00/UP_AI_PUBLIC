from sqlalchemy.orm import Session

from app.repositories.master.tehsil_repository import (
    tehsil_repository,
)

from app.services.base.base_service import BaseService


class TehsilService(
    BaseService
):
    def __init__(self):
        super().__init__(
            tehsil_repository
        )

    # -----------------------
    # Business Methods
    # -----------------------

    def get_by_district(
        self,
        db: Session,
        district_id: int,
    ):
        return self.repository.get_by_district(
            db,
            district_id,
        )

    def get_by_code(
        self,
        db: Session,
        tehsil_code: str,
    ):
        return self.repository.get_by_code(
            db,
            tehsil_code,
        )


tehsil_service = TehsilService()