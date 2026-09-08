from app.engines.workflow.workflow_context import (
    WorkflowContext,
)

from app.engines.workflow.workflow_manager import (
    workflow_manager,
)


class WorkflowEngine:
    """
    Public entry point for the
    Workflow Engine.

    Other modules should interact
    only with this class.
    """

    def move_to_next_step(
        self,
        db,
        context: WorkflowContext,
    ) -> WorkflowContext:

        return workflow_manager.execute(
            db,
            context,
        )


workflow_engine = WorkflowEngine()