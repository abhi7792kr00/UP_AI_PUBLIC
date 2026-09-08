from sqlalchemy.orm import Session

from app.engines.base.base_engine import (
    BaseEngine,
)

from database.models.workflow.workflow_assignment import (
    WorkflowAssignment,
)


class AssignmentEngine(BaseEngine):
    """
    Creates the initial workflow assignment.
    """

    def __init__(
        self,
        workflow_assignment_service,
    ):
        self.workflow_assignment_service = (
            workflow_assignment_service
        )

    def assign(
        self,
        db: Session,
        *,
        workflow_definition_id: int,
        workflow_step_id: int,
        reference_number: str,
        assigned_to: int,
        assigned_by: int | None = None,
        assignment_type: str = "SYSTEM",
        remarks: str | None = None,
    ):
        assignment = WorkflowAssignment(
            workflow_definition_id=workflow_definition_id,
            workflow_step_id=workflow_step_id,
            reference_number=reference_number,
            assigned_to=assigned_to,
            assigned_by=assigned_by,
            assignment_type=assignment_type,
            remarks=remarks,
        )

        return self.workflow_assignment_service.assign(
            db,
            assignment,
        )