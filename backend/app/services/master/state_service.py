from sqlalchemy.orm import Session

from app.repositories.master.state_repository import (
    state_repository,
)

from app.services.base.base_service import BaseService


class StateService(
    BaseService
):
    def __init__(self):
        super().__init__(
            state_repository
        )

    # -----------------------
    # Business Methods
    # -----------------------

    def get_by_code(
        self,
        db: Session,
        state_code: str,
    ):
        return self.repository.get_by_code(
            db,
            state_code,
        )


state_service = StateService()