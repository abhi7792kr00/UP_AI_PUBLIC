from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.workflow.workflow_definition import (
    WorkflowDefinition,
)


class WorkflowDefinitionRepository(
    BaseRepository[WorkflowDefinition]
):
    def __init__(self):
        super().__init__(
            WorkflowDefinition
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_by_workflow_code(
        self,
        db: Session,
        workflow_code: str,
    ) -> WorkflowDefinition | None:
        return (
            db.query(
                WorkflowDefinition
            )
            .filter(
                WorkflowDefinition.workflow_code
                == workflow_code
            )
            .first()
        )

    def get_active(
        self,
        db: Session,
    ) -> list[WorkflowDefinition]:
        return (
            db.query(
                WorkflowDefinition
            )
            .filter(
                WorkflowDefinition.is_active
                == True
            )
            .all()
        )

    def get_default_workflow(
        self,
        db: Session,
        module_name: str,
    ) -> WorkflowDefinition | None:
        return (
            db.query(
                WorkflowDefinition
            )
            .filter(
                WorkflowDefinition.module_name
                == module_name,
                WorkflowDefinition.is_default
                == True,
                WorkflowDefinition.is_active
                == True,
            )
            .first()
        )

    def exists_by_code(
        self,
        db: Session,
        workflow_code: str,
    ) -> bool:
        return (
            db.query(
                WorkflowDefinition
            )
            .filter(
                WorkflowDefinition.workflow_code
                == workflow_code
            )
            .first()
            is not None
        )


workflow_definition_repository = (
    WorkflowDefinitionRepository()
)