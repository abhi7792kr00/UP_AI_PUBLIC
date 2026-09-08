from app.services.base.base_service import BaseService

from app.repositories.workflow.workflow_history_repository import (
    workflow_history_repository,
)

from database.models.workflow.workflow_history import (
    WorkflowHistory,
)


class WorkflowHistoryService(
    BaseService[WorkflowHistory]
):
    def __init__(self):
        super().__init__(
            repository=workflow_history_repository
        )

    # ---------------------------------
    # Business Methods
    # ---------------------------------

    def get_history(
        self,
        db,
        reference_number: str,
    ):
        return self.repository.get_history(
            db,
            reference_number,
        )

    def get_latest(
        self,
        db,
        reference_number: str,
    ):
        return self.repository.get_latest(
            db,
            reference_number,
        )

    def record_history(
        self,
        db,
        history: WorkflowHistory,
    ):
        return self.repository.create_history(
            db,
            history,
        )


workflow_history_service = (
    WorkflowHistoryService()
)