from sqlalchemy.orm import Session

from app.dto.complaint.complaint_registration_request import (
    ComplaintRegistrationRequest,
)

from app.engines.complaint.address_resolver import (
    address_resolver,
)

from app.workflows.base.base_workflow import (
    BaseWorkflow,
)


class ComplaintWorkflow(BaseWorkflow):
    """
    Enterprise Complaint Registration Workflow

    This workflow orchestrates the complete
    complaint registration lifecycle.
    """

    def __init__(self):
        super().__init__()

    def register_complaint(
        self,
        db: Session,
        request: ComplaintRegistrationRequest,
    ):
        """
        Complaint Registration Flow

        Steps

        1. Validate Request

        2. Resolve Address

        3. Resolve Jurisdiction

        4. Resolve Department

        5. Resolve Office

        6. Resolve Priority

        7. Generate Tracking Number

        8. Assign Officer

        9. Create Timeline

        10. Save Complaint

        11. Send Notification
        """

        # ---------------------------------
        # Step 1
        # Address Resolution
        # ---------------------------------

        resolved_address = (
            address_resolver.resolve(
                db=db,
                request=request,
            )
        )

        # ---------------------------------
        # Future Workflow
        # ---------------------------------

        # resolved_jurisdiction =
        # jurisdiction_engine.resolve(
        #     db=db,
        #     request=request,
        #     address=resolved_address,
        # )

        # resolved_routing =
        # routing_engine.resolve(
        #     db=db,
        #     request=request,
        #     jurisdiction=resolved_jurisdiction,
        # )

        # resolved_priority =
        # priority_engine.resolve(
        #     db=db,
        #     request=request,
        # )

        # tracking =
        # tracking_engine.generate(
        #     db=db,
        #     request=request,
        # )

        # assignment =
        # assignment_engine.assign(
        #     db=db,
        #     request=request,
        # )

        # timeline_engine.create(
        #     db=db,
        #     request=request,
        # )

        # complaint = complaint_service.create(...)

        # notification_engine.send(...)

        # ---------------------------------
        # Temporary Return
        # ---------------------------------

        return {
            "status": "success",
            "message": "Address resolved successfully.",
            "resolved_address": resolved_address,
        }


complaint_workflow = ComplaintWorkflow()