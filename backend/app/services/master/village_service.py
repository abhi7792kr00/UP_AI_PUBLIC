from sqlalchemy.orm import Session

from app.repositories.master.village_repository import (
    village_repository,
)

from app.services.base.base_service import BaseService


class VillageService(
    BaseService
):
    def __init__(self):
        super().__init__(
            village_repository
        )

    # -----------------------
    # Business Methods
    # -----------------------

    def get_by_gram_panchayat(
        self,
        db: Session,
        gram_panchayat_id: int,
    ):
        return self.repository.get_by_gram_panchayat(
            db,
            gram_panchayat_id,
        )

    def get_by_code(
        self,
        db: Session,
        village_code: str,
    ):
        return self.repository.get_by_code(
            db,
            village_code,
        )


village_service = VillageService()