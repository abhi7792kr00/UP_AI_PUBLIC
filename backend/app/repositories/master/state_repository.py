from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.state import State


class StateRepository(
    BaseRepository[State]
):
    def __init__(self):
        super().__init__(State)

    # -----------------------
    # Query Methods
    # -----------------------

    def get_by_code(
        self,
        db: Session,
        state_code: str,
    ):
        return (
            db.query(State)
            .filter(
                State.state_code == state_code
            )
            .first()
        )


state_repository = StateRepository()