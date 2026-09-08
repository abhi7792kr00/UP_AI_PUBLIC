from sqlalchemy.orm import Session

from app.repositories.base.base_repository import (
    BaseRepository,
)

from database.models.citizen.citizen import (
    Citizen,
)


class CitizenRepository(
    BaseRepository[Citizen]
):
    """
    Repository for Citizen.
    """

    def __init__(self):
        super().__init__(Citizen)

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(Citizen)
            .filter(
                Citizen.user_id == user_id,
            )
            .first()
        )


citizen_repository = CitizenRepository()