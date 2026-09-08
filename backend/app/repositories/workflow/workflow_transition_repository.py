from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.workflow.workflow_transition import (
    WorkflowTransition,
)


class WorkflowTransitionRepository(
    BaseRepository[WorkflowTransition]
):
    def __init__(self):
        super().__init__(
            WorkflowTransition
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_allowed_transition(
        self,
        db: Session,
        from_step_id: int,
        to_step_id: int,
    ) -> WorkflowTransition | None:
        return (
            db.query(
                WorkflowTransition
            )
            .filter(
                WorkflowTransition.from_step_id
                == from_step_id,
                WorkflowTransition.to_step_id
                == to_step_id,
                WorkflowTransition.is_active
                == True,
            )
            .first()
        )

    def get_available_transitions(
        self,
        db: Session,
        from_step_id: int,
    ) -> list[WorkflowTransition]:
        return (
            db.query(
                WorkflowTransition
            )
            .filter(
                WorkflowTransition.from_step_id
                == from_step_id,
                WorkflowTransition.is_active
                == True,
            )
            .all()
        )

    def get_by_transition_code(
        self,
        db: Session,
        transition_code: str,
    ) -> WorkflowTransition | None:
        return (
            db.query(
                WorkflowTransition
            )
            .filter(
                WorkflowTransition.transition_code
                == transition_code
            )
            .first()
        )

    def exists_transition(
        self,
        db: Session,
        from_step_id: int,
        to_step_id: int,
    ) -> bool:
        return (
            self.get_allowed_transition(
                db,
                from_step_id,
                to_step_id,
            )
            is not None
        )


workflow_transition_repository = (
    WorkflowTransitionRepository()
)