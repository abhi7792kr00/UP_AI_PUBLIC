from sqlalchemy.orm import Session

from database.models.complaint.complaint import Complaint

from app.dto.complaint.complaint_request import (
    ComplaintRequest,
)

from app.engines.reference.reference_engine import (
    reference_engine,
)


class ComplaintRegistrationEngine:
    """
    Main complaint registration orchestrator.
    """

    def __init__(
        self,
        complaint_validator,
        routing_engine,
        assignment_engine,
        timeline_engine,
        notification_engine,
        complaint_service,
    ):
        self.complaint_validator = (
            complaint_validator
        )

        self.routing_engine = (
            routing_engine
        )

        self.assignment_engine = (
            assignment_engine
        )

        self.timeline_engine = (
            timeline_engine
        )

        self.notification_engine = (
            notification_engine
        )

        self.complaint_service = (
            complaint_service
        )

        self.reference_engine = (
            reference_engine
        )

    def register_complaint(
        self,
        db: Session,
        request: ComplaintRequest,
    ):
        """
        Complete complaint registration.
        """

        validation = (
        self.complaint_validator.validate(
        db,
        request,
        )
    )

        if not validation.is_valid:
            raise ValueError(
                validation.errors,
            )

        routing = (
            self.routing_engine.resolve(
                db,
                request,
            )
        )

        complaint_number = (
            self.reference_engine.generate(
                db=db,
                module_code="COMPLAINT",
            )
        )

        complaint = Complaint(
            complaint_number=complaint_number,

            citizen_id=request.citizen_id,

            category_id=request.category_id,

	        subcategory_id=request.subcategory_id,
           
	        priority_id=routing.priority_id,

            status_id=routing.status_id,

            department_id=routing.department_id,

            office_id=routing.office_id,

            assigned_officer_id=routing.officer_id,

            subject=request.subject,

            description=request.description,

            address=request.address,

            latitude=request.latitude,

            longitude=request.longitude,

            source=request.source,

            language=request.language,

            is_public=(
                request.visibility == "PUBLIC"
            ),
        )

        complaint = (
            self.complaint_service.create(
                db,
                complaint,
            )
        )

        self.assignment_engine.assign(
            db=db,
            workflow_definition_id=(
                routing.workflow_definition_id
            ),
            workflow_step_id=(
                routing.workflow_step_id
            ),
            reference_number=complaint_number,
            assigned_to=routing.officer_id,
            assignment_type="SYSTEM",
        )

        self.timeline_engine.record(
            db=db,
            workflow_definition_id=(
                routing.workflow_definition_id
            ),
            workflow_step_id=(
                routing.workflow_step_id
            ),
            reference_number=complaint_number,
            action="REGISTERED",
            remarks="Complaint registered.",
        )

        self.notification_engine.notify(
            complaint,
        )

        return complaint


complaint_registration_engine = (
    ComplaintRegistrationEngine
)
