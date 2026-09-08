from app.engines.workflow.workflow_context import (
    WorkflowContext,
)

from app.services.workflow import (
    workflow_transition_service,
)


class WorkflowValidator:
    """
    Validates workflow execution.

    Responsibilities

    • Validate workflow transition

    • Validate required remark

    • Validate required attachment
    """

    def validate_transition(
        self,
        db,
        context: WorkflowContext,
    ) -> bool:

        transition = (
            workflow_transition_service
            .get_allowed_transition(
                db,
                context.current_step.id,
                context.next_step.id,
            )
        )

        if transition is None:
            raise ValueError(
                "Invalid workflow transition."
            )

        context.transition = transition

        return True

    def validate_remark(
        self,
        context: WorkflowContext,
    ) -> bool:

        if (
            context.transition
            and context.transition.requires_remark
        ):
            if (
                context.remarks is None
                or context.remarks.strip() == ""
            ):
                raise ValueError(
                    "Remark is required."
                )

        return True

    def validate_attachment(
        self,
        context: WorkflowContext,
    ) -> bool:

        if (
            context.transition
            and context.transition.requires_attachment
        ):
            if (
                context.attachment is None
                or context.attachment.strip() == ""
            ):
                raise ValueError(
                    "Attachment is required."
                )

        return True

    def validate(
        self,
        db,
        context: WorkflowContext,
    ) -> bool:

        self.validate_transition(
            db,
            context,
        )

        self.validate_remark(
            context,
        )

        self.validate_attachment(
            context,
        )

        return True


workflow_validator = (
    WorkflowValidator()
)