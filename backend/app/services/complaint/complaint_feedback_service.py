from sqlalchemy.orm import Session

from app.services.base.base_service import (
    BaseService,
)

from app.repositories.complaint.complaint_feedback_repository import (
    complaint_feedback_repository,
)

from database.models.complaint.complaint_feedback import (
    ComplaintFeedback,
)

from database.models.complaint.complaint import (
    Complaint,
)

from database.models.citizen.citizen import (
    Citizen,
)


CLOSED_STATUS_ID = 5


class ComplaintFeedbackService(
    BaseService[ComplaintFeedback]
):

    def __init__(self):
        super().__init__(
            repository=complaint_feedback_repository
        )

    # ---------------------------------
    # Create Feedback
    # ---------------------------------

    def create_feedback(
        self,
        db: Session,
        complaint_number: str,
        citizen_id: int,
        rating: int,
        feedback_text: str | None,
        is_satisfied: bool,
    ) -> ComplaintFeedback:

        # -----------------------------
        # Find complaint
        # -----------------------------

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.complaint_number
                == complaint_number,
            )
            .first()
        )

        if complaint is None:
            raise ValueError(
                "Complaint not found."
            )

        # -----------------------------
        # Verify citizen ownership
        # -----------------------------

        citizen = (
            db.query(Citizen)
            .filter(
                Citizen.id == citizen_id,
                Citizen.is_active == True,
            )
            .first()
        )

        if citizen is None:
            raise ValueError(
                "Citizen profile not found."
            )

        if complaint.citizen_id != citizen.id:
            raise ValueError(
                "You are not allowed to give feedback "
                "for this complaint."
            )

        # -----------------------------
        # Complaint must be closed
        # -----------------------------

        if complaint.status_id != CLOSED_STATUS_ID:
            raise ValueError(
                "Feedback can only be submitted "
                "for a closed complaint."
            )

        # -----------------------------
        # Prevent duplicate feedback
        # -----------------------------

        existing = (
            self.repository
            .get_by_complaint_and_citizen(
                db,
                complaint.id,
                citizen.id,
            )
        )

        if existing is not None:
            raise ValueError(
                "Feedback has already been submitted "
                "for this complaint."
            )

        # -----------------------------
        # Create feedback
        # -----------------------------

        feedback = ComplaintFeedback(
            complaint_id=complaint.id,
            citizen_id=citizen.id,
            rating=rating,
            feedback_text=feedback_text,
            is_satisfied=is_satisfied,
        )

        return self.create(
            db,
            feedback,
        )

    # ---------------------------------
    # Get Citizen Feedback
    # ---------------------------------

    def get_feedback_for_complaint(
        self,
        db: Session,
        complaint_number: str,
        citizen_id: int,
    ):

        complaint = (
            db.query(Complaint)
            .filter(
                Complaint.complaint_number
                == complaint_number,
            )
            .first()
        )

        if complaint is None:
            raise ValueError(
                "Complaint not found."
            )

        if complaint.citizen_id != citizen_id:
            raise ValueError(
                "You are not allowed to access "
                "this complaint."
            )

        feedback = (
            self.repository
            .get_by_complaint_and_citizen(
                db,
                complaint.id,
                citizen_id,
            )
        )

        if feedback is None:
            raise ValueError(
                "Feedback not found."
            )

        return feedback


complaint_feedback_service = (
    ComplaintFeedbackService()
)
