from sqlalchemy.orm import Session

from app.repositories.master.ward_repository import (
    ward_repository,
)

from app.services.base.base_service import BaseService


class WardService(
    BaseService
):
    def __init__(self):
        super().__init__(
            ward_repository
        )

    def get_by_municipal_body(
        self,
        db: Session,
        municipal_body_id: int,
    ):
        return self.repository.get_by_municipal_body(
            db,
            municipal_body_id,
        )

    def get_by_ward_number(
        self,
        db: Session,
        municipal_body_id: int,
        ward_number: int,
    ):
        return self.repository.get_by_ward_number(
            db,
            municipal_body_id,
            ward_number,
        )


ward_service = WardService()