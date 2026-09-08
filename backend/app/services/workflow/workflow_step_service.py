from app.services.base.base_service import BaseService

from app.repositories.workflow.workflow_step_repository import (
    workflow_step_repository,
)

from database.models.workflow.workflow_step import (
    WorkflowStep,
)


class WorkflowStepService(
    BaseService[WorkflowStep]
):
    def __init__(self):
        super().__init__(
            repository=workflow_step_repository
        )

    # ---------------------------------
    # Business Methods
    # ---------------------------------

    def get_steps(
        self,
        db,
        workflow_definition_id: int,
    ):
        return self.repository.get_by_workflow(
            db,
            workflow_definition_id,
        )

    def get_initial_step(
        self,
        db,
        workflow_definition_id: int,
    ):
        return self.repository.get_initial_step(
            db,
            workflow_definition_id,
        )

    def get_final_step(
        self,
        db,
        workflow_definition_id: int,
    ):
        return self.repository.get_final_step(
            db,
            workflow_definition_id,
        )

    def get_by_step_code(
        self,
        db,
        workflow_definition_id: int,
        step_code: str,
    ):
        return self.repository.get_by_step_code(
            db,
            workflow_definition_id,
            step_code,
        )

    def get_by_order(
        self,
        db,
        workflow_definition_id: int,
        step_order: int,
    ):
        return self.repository.get_by_order(
            db,
            workflow_definition_id,
            step_order,
        )


workflow_step_service = (
    WorkflowStepService()
)