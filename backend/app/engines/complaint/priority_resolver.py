from sqlalchemy.orm import Session

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from app.engines.base.base_engine import (
    BaseEngine,
)

from database.models.complaint.complaint_priority import (
    ComplaintPriority,
)


class PriorityResolver(BaseEngine):
    """
    Resolves complaint priority.
    """

    def __init__(
        self,
        complaint_priority_service,
    ):
        self.complaint_priority_service = (
            complaint_priority_service
        )

    def resolve(
        self,
        db: Session,
        request: ComplaintRequest,
    ) -> ComplaintPriority:
        """
        Resolve complaint priority.
        """

        if request.priority_id is not None:

            priority = (
                self.complaint_priority_service.get_by_id(
                    db,
                    request.priority_id,
                )
            )

            if priority is None:
                raise ValueError(
                    "Invalid complaint priority."
                )

            return priority

        priority = (
            self.complaint_priority_service.get_default_priority(
                db,
            )
        )

        if priority is None:
            raise ValueError(
                "Default complaint priority is not configured."
            )

        return priority