from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.gram_panchayat import (
    GramPanchayat,
)


class GramPanchayatRepository(
    BaseRepository[GramPanchayat]
):
    def __init__(self):
        super().__init__(
            GramPanchayat
        )

    # -----------------------
    # Query Methods
    # -----------------------

    def get_by_block(
        self,
        db: Session,
        block_id: int,
    ):
        return (
            db.query(
                GramPanchayat
            )
            .filter(
                GramPanchayat.block_id == block_id
            )
            .all()
        )

    def get_by_code(
        self,
        db: Session,
        gram_panchayat_code: str,
    ):
        return (
            db.query(
                GramPanchayat
            )
            .filter(
                GramPanchayat.gram_panchayat_code
                == gram_panchayat_code
            )
            .first()
        )


gram_panchayat_repository = (
    GramPanchayatRepository()
)