from sqlalchemy.orm import Session

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from app.engines.base.base_engine import (
    BaseEngine,
)

from database.models.citizen.citizen import (
    Citizen,
)


class CitizenResolver(BaseEngine):
    """
    Resolves the citizen for a complaint.

    Flow:
        1. Search citizen by mobile number.
        2. If citizen exists, return it.
        3. Otherwise create a new citizen.
    """

    def __init__(
        self,
        citizen_service,
    ):
        self.citizen_service = citizen_service

    def resolve(
        self,
        db: Session,
        request: ComplaintRequest,
    ) -> Citizen:
        """
        Resolve or create citizen.
        """

        citizen = self.citizen_service.get_by_mobile(
            db,
            request.mobile_number,
        )

        if citizen is not None:
            return citizen

        citizen = Citizen(
            full_name=request.citizen_name,
            mobile_number=request.mobile_number,
            email=request.email,
        )

        return self.citizen_service.create(
            db,
            citizen,
        )