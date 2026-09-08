from app.services.base.base_service import BaseService

from app.repositories.workflow.workflow_assignment_repository import (
    workflow_assignment_repository,
)

from database.models.workflow.workflow_assignment import (
    WorkflowAssignment,
)


class WorkflowAssignmentService(
    BaseService[WorkflowAssignment]
):

    def __init__(self):
        super().__init__(
            repository=workflow_assignment_repository
        )

    # ---------------------------------
    # Business Methods
    # ---------------------------------

    def get_active_assignment(
        self,
        db,
        reference_number: str,
    ):
        return self.repository.get_active_assignment(
            db,
            reference_number,
        )

    def get_active_assignment_for_officer(
        self,
        db,
        officer_id: int,
        reference_number: str,
    ):
        return self.repository.get_active_assignment_for_officer(
            db,
            officer_id,
            reference_number,
        )

    def get_by_officer(
        self,
        db,
        officer_id: int,
    ):
        return self.repository.get_by_officer(
            db,
            officer_id,
        )

    def get_active_by_officer(
        self,
        db,
        officer_id: int,
    ):
        return self.repository.get_active_by_officer(
            db,
            officer_id,
        )

    def get_by_reference(
        self,
        db,
        reference_number: str,
    ):
        return self.repository.get_by_reference(
            db,
            reference_number,
        )

    def assign(
        self,
        db,
        assignment: WorkflowAssignment,
    ):
        return self.repository.assign(
            db,
            assignment,
        )

    def complete(
        self,
        db,
        assignment: WorkflowAssignment,
    ):
        return self.repository.complete_assignment(
            db,
            assignment,
        )


workflow_assignment_service = (
    WorkflowAssignmentService()
)