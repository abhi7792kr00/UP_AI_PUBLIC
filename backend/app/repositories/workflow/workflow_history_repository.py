from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.workflow.workflow_history import (
    WorkflowHistory,
)


class WorkflowHistoryRepository(
    BaseRepository[WorkflowHistory]
):
    def __init__(self):
        super().__init__(
            WorkflowHistory
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_history(
        self,
        db: Session,
        reference_number: str,
    ) -> list[WorkflowHistory]:
        return (
            db.query(
                WorkflowHistory
            )
            .filter(
                WorkflowHistory.reference_number
                == reference_number
            )
            .order_by(
                WorkflowHistory.created_at
            )
            .all()
        )

    def get_latest(
        self,
        db: Session,
        reference_number: str,
    ) -> WorkflowHistory | None:
        return (
            db.query(
                WorkflowHistory
            )
            .filter(
                WorkflowHistory.reference_number
                == reference_number
            )
            .order_by(
                WorkflowHistory.created_at.desc()
            )
            .first()
        )

    def create_history(
        self,
        db: Session,
        history: WorkflowHistory,
    ) -> WorkflowHistory:
        db.add(history)
        db.commit()
        db.refresh(history)

        return history


workflow_history_repository = (
    WorkflowHistoryRepository()
)