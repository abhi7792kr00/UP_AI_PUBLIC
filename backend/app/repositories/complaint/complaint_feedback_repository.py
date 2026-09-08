from sqlalchemy.orm import Session

from app.repositories.base.base_repository import (
    BaseRepository,
)

from database.models.complaint.complaint_feedback import (
    ComplaintFeedback,
)


class ComplaintFeedbackRepository(
    BaseRepository[ComplaintFeedback]
):

    def __init__(self):
        super().__init__(
            ComplaintFeedback
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_by_complaint_and_citizen(
        self,
        db: Session,
        complaint_id: int,
        citizen_id: int,
    ) -> ComplaintFeedback | None:

        return (
            db.query(ComplaintFeedback)
            .filter(
                ComplaintFeedback.complaint_id
                == complaint_id,

                ComplaintFeedback.citizen_id
                == citizen_id,
            )
            .first()
        )

    def get_by_complaint(
        self,
        db: Session,
        complaint_id: int,
    ) -> list[ComplaintFeedback]:

        return (
            db.query(ComplaintFeedback)
            .filter(
                ComplaintFeedback.complaint_id
                == complaint_id,
            )
            .order_by(
                ComplaintFeedback.created_at.desc()
            )
            .all()
        )


complaint_feedback_repository = (
    ComplaintFeedbackRepository()
)
