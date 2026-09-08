from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.village import Village


class VillageRepository(
    BaseRepository[Village]
):
    def __init__(self):
        super().__init__(Village)

    # -----------------------
    # Query Methods
    # -----------------------

    def get_by_gram_panchayat(
        self,
        db: Session,
        gram_panchayat_id: int,
    ):
        return (
            db.query(Village)
            .filter(
                Village.gram_panchayat_id == gram_panchayat_id
            )
            .all()
        )

    def get_by_code(
        self,
        db: Session,
        village_code: str,
    ):
        return (
            db.query(Village)
            .filter(
                Village.village_code == village_code
            )
            .first()
        )


village_repository = VillageRepository()