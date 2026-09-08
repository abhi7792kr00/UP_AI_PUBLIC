from sqlalchemy.orm import Session

from app.repositories.master.municipal_body_repository import (
    municipal_body_repository,
)

from app.services.base.base_service import BaseService

from database.models.master.municipal_body import (
    MunicipalBodyType,
)


class MunicipalBodyService(
    BaseService
):
    def __init__(self):
        super().__init__(
            municipal_body_repository
        )

    def get_by_body_code(
        self,
        db: Session,
        body_code: str,
    ):
        return self.repository.get_by_body_code(
            db,
            body_code,
        )

    def get_by_district(
        self,
        db: Session,
        district_id: int,
    ):
        return self.repository.get_by_district(
            db,
            district_id,
        )

    def get_by_type(
        self,
        db: Session,
        body_type: MunicipalBodyType,
    ):
        return self.repository.get_by_type(
            db,
            body_type,
        )


municipal_body_service = MunicipalBodyService()