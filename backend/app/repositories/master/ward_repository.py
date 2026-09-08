from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.ward import Ward


class WardRepository(
    BaseRepository[Ward]
):
    def __init__(self):
        super().__init__(Ward)

    def get_by_municipal_body(
        self,
        db: Session,
        municipal_body_id: int,
    ):
        return (
            db.query(Ward)
            .filter(
                Ward.municipal_body_id == municipal_body_id
            )
            .all()
        )

    def get_by_ward_number(
        self,
        db: Session,
        municipal_body_id: int,
        ward_number: int,
    ):
        return (
            db.query(Ward)
            .filter(
                Ward.municipal_body_id == municipal_body_id,
                Ward.ward_number == ward_number,
            )
            .first()
        )


ward_repository = WardRepository()