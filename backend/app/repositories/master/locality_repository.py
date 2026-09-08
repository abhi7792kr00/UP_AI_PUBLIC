from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository
from database.models.master.locality import Locality


class LocalityRepository(BaseRepository[Locality]):
    def __init__(self):
        super().__init__(Locality)

    def get_by_code(
        self,
        db: Session,
        locality_code: str,
    ):
        return (
            db.query(Locality)
            .filter(
                Locality.locality_code == locality_code
            )
            .first()
        )


locality_repository = LocalityRepository()