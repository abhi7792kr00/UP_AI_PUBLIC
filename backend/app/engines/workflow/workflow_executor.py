from app.engines.workflow.workflow_context import (
    WorkflowContext,
)

from database.models.workflow.workflow_assignment import (
    WorkflowAssignment,
)

from database.models.workflow.workflow_history import (
    WorkflowHistory,
)

from app.services.workflow import (
    workflow_assignment_service,
    workflow_history_service,
)


class WorkflowExecutor:
    """
    Executes a validated workflow transition.

    Responsibilities

    • Complete current active assignment
    • Record workflow history
    • Create next assignment
    • Update runtime context
    """

    def record_history(
        self,
        db,
        context: WorkflowContext,
    ) -> WorkflowHistory:

        history = WorkflowHistory(
            workflow_definition_id=context.workflow.id,
            workflow_step_id=context.next_step.id,
            reference_number=context.reference_number,
            action=context.transition.transition_code,
            remarks=context.remarks,
            performed_by=context.performed_by,
        )

        return workflow_history_service.record_history(
            db,
            history,
        )

    def complete_current_assignment(
        self,
        db,
        context: WorkflowContext,
    ) -> WorkflowAssignment | None:

        assignment = (
            workflow_assignment_service
            .get_active_assignment(
                db,
                context.reference_number,
            )
        )

        if assignment is None:
            return None

        return (
            workflow_assignment_service
            .complete(
                db,
                assignment,
            )
        )

    def create_assignment(
        self,
        db,
        context: WorkflowContext,
    ) -> WorkflowAssignment | None:

        if context.assigned_to is None:
            raise ValueError(
                "No officer is assigned to this complaint."
            )

        assignment = WorkflowAssignment(
            workflow_definition_id=context.workflow.id,
            workflow_step_id=context.next_step.id,
            reference_number=context.reference_number,
            assigned_to=context.assigned_to,
            assigned_by=context.performed_by,
            assignment_type="MANUAL",
            remarks=context.remarks,
        )

        return workflow_assignment_service.assign(
            db,
            assignment,
        )

    def execute(
        self,
        db,
        context: WorkflowContext,
    ) -> WorkflowContext:

        # 1. Complete current active assignment
        self.complete_current_assignment(
            db,
            context,
        )

        # 2. Record workflow history
        self.record_history(
            db,
            context,
        )

        # 3. Create next assignment if required
        self.create_assignment(
            db,
            context,
        )

        # 4. Update runtime context
        context.current_step = context.next_step

        return context


workflow_executor = (
    WorkflowExecutor()
)