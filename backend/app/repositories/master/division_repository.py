from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.master.division import Division


class DivisionRepository(
    BaseRepository[Division]
):
    def __init__(self):
        super().__init__(Division)

    def get_by_state(
        self,
        db: Session,
        state_id: int,
    ):
        return (
            db.query(Division)
            .filter(
                Division.state_id == state_id
            )
            .all()
        )


division_repository = DivisionRepository()