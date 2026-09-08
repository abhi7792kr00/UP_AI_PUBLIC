from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.municipal_body import MunicipalBody
from database.models.master.municipal_body import MunicipalBodyType


class MunicipalBodyRepository(
    BaseRepository[MunicipalBody]
):
    def __init__(self):
        super().__init__(MunicipalBody)

    def get_by_body_code(
        self,
        db: Session,
        body_code: str,
    ):
        return (
            db.query(MunicipalBody)
            .filter(
                MunicipalBody.body_code == body_code
            )
            .first()
        )

    def get_by_district(
        self,
        db: Session,
        district_id: int,
    ):
        return (
            db.query(MunicipalBody)
            .filter(
                MunicipalBody.district_id == district_id
            )
            .all()
        )

    def get_by_type(
        self,
        db: Session,
        body_type: MunicipalBodyType,
    ):
        return (
            db.query(MunicipalBody)
            .filter(
                MunicipalBody.body_type == body_type
            )
            .all()
        )


municipal_body_repository = MunicipalBodyRepository()