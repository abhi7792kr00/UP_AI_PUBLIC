from sqlalchemy.orm import Session

from app.repositories.master.district_repository import (
    district_repository,
)

from app.services.base.base_service import BaseService


class DistrictService(
    BaseService
):
    def __init__(self):
        super().__init__(
            district_repository
        )

    # -----------------------
    # Business Methods
    # -----------------------

    def get_by_division(
        self,
        db: Session,
        division_id: int,
    ):
        return self.repository.get_by_division(
            db,
            division_id,
        )

    def get_by_code(
        self,
        db: Session,
        district_code: str,
    ):
        return self.repository.get_by_code(
            db,
            district_code,
        )


district_service = DistrictService()