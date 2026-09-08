from dataclasses import dataclass

from database.models.workflow.workflow_definition import (
    WorkflowDefinition,
)

from database.models.workflow.workflow_step import (
    WorkflowStep,
)

from database.models.workflow.workflow_transition import (
    WorkflowTransition,
)


@dataclass(slots=True)
class WorkflowContext:
    """
    Runtime context used during workflow execution.

    A WorkflowContext must always represent a valid
    workflow execution state.

    This object should be created only after:

    - WorkflowDefinition is loaded
    - Current WorkflowStep is loaded
    - Next WorkflowStep is resolved (if applicable)
    - WorkflowTransition is resolved (if applicable)

    Business APIs should NOT construct this object
    directly with incomplete data. That responsibility
    belongs to WorkflowRuntimeService.
    """

    # Business Reference
    reference_number: str

    # Workflow Configuration
    workflow: WorkflowDefinition

    current_step: WorkflowStep

    # Runtime State
    next_step: WorkflowStep | None = None

    transition: WorkflowTransition | None = None

    # Execution Metadata
    performed_by: int | None = None

    assigned_to: int | None = None

    remarks: str | None = None

    attachment: str | None = None