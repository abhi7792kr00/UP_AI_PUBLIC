from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.district import District


class DistrictRepository(
    BaseRepository[District]
):
    def __init__(self):
        super().__init__(District)

    def get_by_division(
        self,
        db: Session,
        division_id: int,
    ):
        return (
            db.query(District)
            .filter(
                District.division_id == division_id
            )
            .all()
        )

    def get_by_code(
        self,
        db: Session,
        district_code: str,
    ):
        return (
            db.query(District)
            .filter(
                District.district_code == district_code
            )
            .first()
        )


district_repository = DistrictRepository()