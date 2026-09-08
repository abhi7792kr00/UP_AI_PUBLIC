from app.services.base.base_service import BaseService

from app.repositories.workflow.workflow_definition_repository import (
    workflow_definition_repository,
)

from database.models.workflow.workflow_definition import (
    WorkflowDefinition,
)


class WorkflowDefinitionService(
    BaseService[WorkflowDefinition]
):
    def __init__(self):
        super().__init__(
            repository=workflow_definition_repository
        )

    # ---------------------------------
    # Business Methods
    # ---------------------------------

    def get_by_workflow_code(
        self,
        db,
        workflow_code: str,
    ):
        return self.repository.get_by_workflow_code(
            db,
            workflow_code,
        )

    def get_default_workflow(
        self,
        db,
        module_name: str,
    ):
        return self.repository.get_default_workflow(
            db,
            module_name,
        )

    def get_active(
        self,
        db,
    ):
        return self.repository.get_active(db)

    def exists_by_code(
        self,
        db,
        workflow_code: str,
    ) -> bool:
        return self.repository.exists_by_code(
            db,
            workflow_code,
        )


workflow_definition_service = (
    WorkflowDefinitionService()
)