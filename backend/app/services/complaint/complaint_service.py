from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.complaint import (
    complaint_repository,
)

from app.services.base.base_service import BaseService

from app.services.workflow import (
    workflow_definition_service,
)

from app.engines.workflow import (
    WorkflowContext,
    workflow_engine,
)

from database.models.workflow.workflow_step import (
    WorkflowStep,
)

from database.models.complaint.complaint_status import (
    ComplaintStatus,
)


class ComplaintService(
    BaseService
):

    def __init__(self):
        super().__init__(
            complaint_repository
        )

    # =================================
    # Officer Dashboard Counts
    # =================================

    def get_dashboard_counts(
        self,
        db: Session,
    ):

        return self.repository.get_dashboard_counts(
            db,
        )

    # =================================
    # Query Methods
    # =================================

    def get_by_complaint_number(
        self,
        db: Session,
        complaint_number: str,
    ):

        return self.repository.get_by_complaint_number(
            db,
            complaint_number,
        )

    def get_by_citizen(
        self,
        db: Session,
        citizen_id: int,
    ):

        return self.repository.get_by_citizen(
            db,
            citizen_id,
        )

    def get_by_status(
        self,
        db: Session,
        status_id: int,
    ):

        return self.repository.get_by_status(
            db,
            status_id,
        )

    def get_by_officer(
        self,
        db: Session,
        officer_id: int,
    ):

        return self.repository.get_by_officer(
            db,
            officer_id,
        )

    # =================================
    # Officer Assigned Complaints
    # =================================

    def get_assigned_complaints_for_officer(
        self,
        db: Session,
        officer_id: int,
    ):

        return (
            self.repository
            .get_assigned_complaints_for_officer(
                db,
                officer_id,
            )
        )

    # =================================
    # Workflow Transition
    # =================================

    def transition(
        self,
        db: Session,
        complaint_number: str,
        to_status_id: int,
        remarks: str | None = None,
        performed_by: int | None = None,
    ):

        # =================================
        # 1. Get complaint
        # =================================

        complaint = (
            self.repository
            .get_by_complaint_number(
                db,
                complaint_number,
            )
        )

        if complaint is None:
            raise ValueError(
                "Complaint not found."
            )

        # =================================
        # 2. Previous status
        # =================================

        previous_status_id = complaint.status_id

        if previous_status_id == to_status_id:
            raise ValueError(
                "Complaint is already in the requested status."
            )

        # =================================
        # 3. Current ComplaintStatus
        # =================================

        current_status = (
            db.query(ComplaintStatus)
            .filter(
                ComplaintStatus.id
                == previous_status_id
            )
            .first()
        )

        if current_status is None:
            raise ValueError(
                "Current complaint status not found."
            )

        # =================================
        # 4. Target ComplaintStatus
        # =================================

        target_status = (
            db.query(ComplaintStatus)
            .filter(
                ComplaintStatus.id
                == to_status_id
            )
            .first()
        )

        if target_status is None:
            raise ValueError(
                "Target complaint status not found."
            )

        # =================================
        # 5. Get Complaint Workflow
        # =================================

        workflow = (
            workflow_definition_service
            .get_default_workflow(
                db,
                "COMPLAINT",
            )
        )

        if workflow is None:
            raise ValueError(
                "Default complaint workflow not found."
            )

        # =================================
        # 6. Current WorkflowStep
        # =================================

        current_step = (
            db.query(WorkflowStep)
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow.id,

                WorkflowStep.step_code
                == current_status.status_code,
            )
            .first()
        )

        if current_step is None:
            raise ValueError(
                f"Workflow step not found for "
                f"status '{current_status.status_code}'."
            )

        # =================================
        # 7. Target WorkflowStep
        # =================================

        next_step = (
            db.query(WorkflowStep)
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow.id,

                WorkflowStep.step_code
                == target_status.status_code,
            )
            .first()
        )

        if next_step is None:
            raise ValueError(
                f"Workflow step not found for "
                f"status '{target_status.status_code}'."
            )

        # =================================
        # 8. Build Workflow Context
        # =================================

        context = WorkflowContext(
            reference_number=complaint_number,
            workflow=workflow,
            current_step=current_step,
            next_step=next_step,
            performed_by=performed_by,
            assigned_to=complaint.assigned_officer_id,
            remarks=remarks,
        )

        # =================================
        # 9. Execute Workflow
        # =================================

        transitioned_at = datetime.utcnow()

        workflow_engine.move_to_next_step(
            db,
            context,
        )

        # =================================
        # 10. Update Complaint Status
        # =================================

        complaint.status_id = to_status_id

        # Set closed_at when complaint is closed

        if target_status.status_code == "CLOSED":

            complaint.closed_at = datetime.utcnow()

        # Clear closed_at when reopened

        elif target_status.status_code == "REOPENED":

            complaint.closed_at = None

        db.add(complaint)

        # =================================
        # 11. Commit
        # =================================

        db.commit()

        db.refresh(complaint)

        # =================================
        # 12. Return API Response
        # =================================

        return {
            "complaint_number": complaint_number,

            "previous_status_id":
                previous_status_id,

            "new_status_id":
                to_status_id,

            "action": (
                context.transition.transition_code
                if context.transition
                else None
            ),

            "remarks": remarks,

            "performed_by": performed_by,

            "transitioned_at":
                transitioned_at,
        }


# =================================
# Service Instance
# =================================

complaint_service = ComplaintService()