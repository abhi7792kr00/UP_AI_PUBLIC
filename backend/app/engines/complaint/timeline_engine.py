from sqlalchemy.orm import Session

from app.engines.base.base_engine import (
    BaseEngine,
)

from database.models.workflow.workflow_history import (
    WorkflowHistory,
)


class TimelineEngine(BaseEngine):
    """
    Records workflow timeline
    for complaint lifecycle.
    """

    def __init__(
        self,
        workflow_history_service,
    ):
        self.workflow_history_service = (
            workflow_history_service
        )

    def record(
        self,
        db: Session,
        *,
        workflow_definition_id: int,
        workflow_step_id: int,
        reference_number: str,
        action: str,
        remarks: str | None = None,
        performed_by: int | None = None,
    ):
        """
        Record workflow history.
        """

        history = WorkflowHistory(
            workflow_definition_id=workflow_definition_id,
            workflow_step_id=workflow_step_id,
            reference_number=reference_number,
            action=action,
            remarks=remarks,
            performed_by=performed_by,
        )

        return self.workflow_history_service.record_history(
            db,
            history,
        )