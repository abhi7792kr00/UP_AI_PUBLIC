from sqlalchemy.orm import Session

from app.repositories.citizen.citizen_repository import (
    citizen_repository,
)

from app.services.base.base_service import (
    BaseService,
)

from database.models.citizen.citizen import (
    Citizen,
)


class CitizenService(BaseService):
    """
    Service for Citizen.
    """

    def __init__(self):
        super().__init__(
            citizen_repository,
        )

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ):
        return self.repository.get_by_user_id(
            db,
            user_id,
        )

    def create_citizen(
        self,
        db: Session,
        citizen: Citizen,
    ):
        existing = self.get_by_user_id(
            db,
            citizen.user_id,
        )

        if existing:
            raise ValueError(
                "Citizen profile already exists."
            )

        return self.create(
            db,
            citizen,
        )


citizen_service = CitizenService()