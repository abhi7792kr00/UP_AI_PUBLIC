from app.api.v1.complaint.complaint_request import (
    ComplaintCreateRequest,
)

from app.api.v1.complaint.complaint_response import (
    ComplaintResponse,
)

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from database.models.complaint.complaint import (
    Complaint,
)


class ComplaintMapper:
    """
    Maps API schemas to internal DTOs
    and domain models.
    """

    @staticmethod
    def to_dto(
        request: ComplaintCreateRequest,
    ) -> ComplaintRequest:
        """
        API Request -> Internal DTO
        """

        return ComplaintRequest(
            **request.model_dump(),
        )

    @staticmethod
    def to_response(
        complaint: Complaint,
    ) -> ComplaintResponse:
        """
        Domain Model -> API Response
        """

        return ComplaintResponse(
            id=complaint.id,
            complaint_number=complaint.complaint_number,
            citizen_id=complaint.citizen_id,
            category_id=complaint.category_id,
            priority_id=complaint.priority_id,
            status_id=complaint.status_id,
            department_id=complaint.department_id,
            office_id=complaint.office_id,
            subject=complaint.subject,
            description=complaint.description,
            address=complaint.address,
            latitude=(
                float(complaint.latitude)
                if complaint.latitude is not None
                else None
            ),
            longitude=(
                float(complaint.longitude)
                if complaint.longitude is not None
                else None
            ),
            source=complaint.source,
            language=complaint.language,
            is_public=complaint.is_public,
            created_at=complaint.created_at,
            updated_at=complaint.updated_at,
        )