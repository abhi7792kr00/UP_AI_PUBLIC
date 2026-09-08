from sqlalchemy.orm import Session

from app.repositories.master.division_repository import (
    division_repository,
)

from app.services.base.base_service import BaseService


class DivisionService(
    BaseService
):
    def __init__(self):
        super().__init__(
            division_repository
        )

    def get_by_state(
        self,
        db: Session,
        state_id: int,
    ):
        return self.repository.get_by_state(
            db,
            state_id,
        )


division_service = DivisionService()