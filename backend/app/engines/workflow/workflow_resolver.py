from sqlalchemy.orm import Session

from app.engines.base.base_engine import BaseEngine


class WorkflowResolver(BaseEngine):
    """
    Resolves the workflow and its initial step
    for a module.
    """

    def __init__(
        self,
        workflow_definition_service,
        workflow_step_service,
    ):
        self.workflow_definition_service = (
            workflow_definition_service
        )

        self.workflow_step_service = (
            workflow_step_service
        )

    def resolve(
        self,
        db: Session,
        module_name: str,
    ):
        """
        Resolve default workflow
        and its initial step.
        """

        workflow = (
            self.workflow_definition_service.get_default_workflow(
                db,
                module_name,
            )
        )

        if workflow is None:
            raise ValueError(
                f"No default workflow configured for '{module_name}'."
            )

        step = (
            self.workflow_step_service.get_initial_step(
                db,
                workflow.id,
            )
        )

        if step is None:
            raise ValueError(
                f"No initial step configured for workflow '{workflow.workflow_code}'."
            )

        return workflow, step