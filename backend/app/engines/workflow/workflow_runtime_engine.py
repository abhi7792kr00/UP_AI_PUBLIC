from sqlalchemy.orm import Session

from app.engines.base.base_engine import (
    BaseEngine,
)


class WorkflowRuntimeEngine(BaseEngine):
    """
    Executes workflow runtime.

    Responsible for starting
    workflow execution.
    """

    def __init__(
        self,
        workflow_resolver,
        assignment_engine,
        timeline_engine,
    ):
        self.workflow_resolver = (
            workflow_resolver
        )

        self.assignment_engine = (
            assignment_engine
        )

        self.timeline_engine = (
            timeline_engine
        )

    def start(
        self,
        db: Session,
        *,
        module_name: str,
        reference_number: str,
        assigned_to: int,
    ):
        workflow, step = (
            self.workflow_resolver.resolve(
                db,
                module_name,
            )
        )

        self.assignment_engine.assign(
            db=db,
            workflow_definition_id=workflow.id,
            workflow_step_id=step.id,
            reference_number=reference_number,
            assigned_to=assigned_to,
            assignment_type="SYSTEM",
        )

        self.timeline_engine.record(
            db=db,
            workflow_definition_id=workflow.id,
            workflow_step_id=step.id,
            reference_number=reference_number,
            action="STARTED",
            remarks="Workflow started.",
        )

        return workflow, step