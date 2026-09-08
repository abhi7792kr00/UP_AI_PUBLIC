from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.tehsil import Tehsil


class TehsilRepository(
    BaseRepository[Tehsil]
):
    def __init__(self):
        super().__init__(Tehsil)

    # -----------------------
    # Query Methods
    # -----------------------

    def get_by_district(
        self,
        db: Session,
        district_id: int,
    ):
        return (
            db.query(Tehsil)
            .filter(
                Tehsil.district_id == district_id
            )
            .all()
        )

    def get_by_code(
        self,
        db: Session,
        tehsil_code: str,
    ):
        return (
            db.query(Tehsil)
            .filter(
                Tehsil.tehsil_code == tehsil_code
            )
            .first()
        )


tehsil_repository = TehsilRepository()