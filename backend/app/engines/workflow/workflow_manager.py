from app.engines.workflow.workflow_context import (
    WorkflowContext,
)

from app.engines.workflow.workflow_validator import (
    workflow_validator,
)

from app.engines.workflow.workflow_executor import (
    workflow_executor,
)


class WorkflowManager:
    """
    Coordinates workflow execution.

    Responsibilities

    • Validate workflow

    • Execute workflow

    • Return updated context
    """

    def execute(
        self,
        db,
        context: WorkflowContext,
    ) -> WorkflowContext:

        workflow_validator.validate(
            db,
            context,
        )

        workflow_executor.execute(
            db,
            context,
        )

        return context


workflow_manager = (
    WorkflowManager()
)