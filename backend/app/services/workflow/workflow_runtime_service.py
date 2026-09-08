from sqlalchemy.orm import Session

from app.engines.workflow import (
    WorkflowContext,
    workflow_engine,
)


class WorkflowRuntimeService:
    """
    Runtime service for executing workflows.

    This service acts as the bridge between
    API layer and Workflow Engine.
    """

    def execute(
        self,
        db: Session,
        context: WorkflowContext,
    ) -> WorkflowContext:

        return workflow_engine.move_to_next_step(
            db,
            context,
        )


workflow_runtime_service = (
    WorkflowRuntimeService()
)