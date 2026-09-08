from sqlalchemy.orm import Session

from app.engines.base.base_engine import (
    BaseEngine,
)

from database.models.complaint.complaint_status import (
    ComplaintStatus,
)


class StatusResolver(BaseEngine):
    """
    Resolves the initial status
    of a complaint.
    """

    def __init__(
        self,
        complaint_status_service,
    ):
        self.complaint_status_service = (
            complaint_status_service
        )

    def resolve(
        self,
        db: Session,
    ) -> ComplaintStatus:
        """
        Return the initial complaint status.
        """

        status = (
            self.complaint_status_service.get_initial_status(
                db,
            )
        )

        if status is None:
            raise ValueError(
                "Initial complaint status is not configured."
            )

        return status