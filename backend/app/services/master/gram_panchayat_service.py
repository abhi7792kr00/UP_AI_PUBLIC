from sqlalchemy.orm import Session

from app.repositories.master.gram_panchayat_repository import (
    gram_panchayat_repository,
)

from app.services.base.base_service import (
    BaseService,
)


class GramPanchayatService(
    BaseService
):
    def __init__(self):
        super().__init__(
            gram_panchayat_repository
        )

    # -----------------------
    # Business Methods
    # -----------------------

    def get_by_block(
        self,
        db: Session,
        block_id: int,
    ):
        return (
            self.repository.get_by_block(
                db,
                block_id,
            )
        )

    def get_by_code(
        self,
        db: Session,
        gram_panchayat_code: str,
    ):
        return (
            self.repository.get_by_code(
                db,
                gram_panchayat_code,
            )
        )


gram_panchayat_service = (
    GramPanchayatService()
)