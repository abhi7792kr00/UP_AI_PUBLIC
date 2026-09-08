from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.workflow.workflow_step import (
    WorkflowStep,
)


class WorkflowStepRepository(
    BaseRepository[WorkflowStep]
):
    def __init__(self):
        super().__init__(
            WorkflowStep
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_by_workflow(
        self,
        db: Session,
        workflow_definition_id: int,
    ) -> list[WorkflowStep]:
        return (
            db.query(
                WorkflowStep
            )
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow_definition_id
            )
            .order_by(
                WorkflowStep.step_order
            )
            .all()
        )

    def get_initial_step(
        self,
        db: Session,
        workflow_definition_id: int,
    ) -> WorkflowStep | None:
        return (
            db.query(
                WorkflowStep
            )
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow_definition_id,
                WorkflowStep.is_initial
                == True,
            )
            .first()
        )

    def get_final_step(
        self,
        db: Session,
        workflow_definition_id: int,
    ) -> WorkflowStep | None:
        return (
            db.query(
                WorkflowStep
            )
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow_definition_id,
                WorkflowStep.is_final
                == True,
            )
            .first()
        )

    def get_by_step_code(
        self,
        db: Session,
        workflow_definition_id: int,
        step_code: str,
    ) -> WorkflowStep | None:
        return (
            db.query(
                WorkflowStep
            )
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow_definition_id,
                WorkflowStep.step_code
                == step_code,
            )
            .first()
        )

    def get_by_order(
        self,
        db: Session,
        workflow_definition_id: int,
        step_order: int,
    ) -> WorkflowStep | None:
        return (
            db.query(
                WorkflowStep
            )
            .filter(
                WorkflowStep.workflow_definition_id
                == workflow_definition_id,
                WorkflowStep.step_order
                == step_order,
            )
            .first()
        )


workflow_step_repository = (
    WorkflowStepRepository()
)