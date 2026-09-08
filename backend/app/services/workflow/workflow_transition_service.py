from app.services.base.base_service import BaseService

from app.repositories.workflow.workflow_transition_repository import (
    workflow_transition_repository,
)

from database.models.workflow.workflow_transition import (
    WorkflowTransition,
)


class WorkflowTransitionService(
    BaseService[WorkflowTransition]
):
    def __init__(self):
        super().__init__(
            repository=workflow_transition_repository
        )

    # ---------------------------------
    # Business Methods
    # ---------------------------------

    def get_allowed_transition(
        self,
        db,
        from_step_id: int,
        to_step_id: int,
    ):
        return self.repository.get_allowed_transition(
            db,
            from_step_id,
            to_step_id,
        )

    def get_available_transitions(
        self,
        db,
        from_step_id: int,
    ):
        return self.repository.get_available_transitions(
            db,
            from_step_id,
        )

    def get_by_transition_code(
        self,
        db,
        transition_code: str,
    ):
        return self.repository.get_by_transition_code(
            db,
            transition_code,
        )

    def is_transition_allowed(
        self,
        db,
        from_step_id: int,
        to_step_id: int,
    ) -> bool:
        return self.repository.exists_transition(
            db,
            from_step_id,
            to_step_id,
        )


workflow_transition_service = (
    WorkflowTransitionService()
)