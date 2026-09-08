from sqlalchemy.orm import Session

from app.repositories.base.base_repository import BaseRepository

from database.models.workflow.workflow_assignment import (
    WorkflowAssignment,
)


class WorkflowAssignmentRepository(
    BaseRepository[WorkflowAssignment]
):

    def __init__(self):
        super().__init__(
            WorkflowAssignment
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_active_assignment(
        self,
        db: Session,
        reference_number: str,
    ) -> WorkflowAssignment | None:

        return (
            db.query(
                WorkflowAssignment
            )
            .filter(
                WorkflowAssignment.reference_number
                == reference_number,

                WorkflowAssignment.is_completed
                == False,
            )
            .order_by(
                WorkflowAssignment.created_at.desc()
            )
            .first()
        )

    def get_active_assignment_for_officer(
        self,
        db: Session,
        officer_id: int,
        reference_number: str,
    ) -> WorkflowAssignment | None:

        return (
            db.query(
                WorkflowAssignment
            )
            .filter(
                WorkflowAssignment.reference_number
                == reference_number,

                WorkflowAssignment.assigned_to
                == officer_id,

                WorkflowAssignment.is_completed
                == False,
            )
            .order_by(
                WorkflowAssignment.created_at.desc()
            )
            .first()
        )

    def get_by_officer(
        self,
        db: Session,
        officer_id: int,
    ) -> list[WorkflowAssignment]:

        return (
            db.query(
                WorkflowAssignment
            )
            .filter(
                WorkflowAssignment.assigned_to
                == officer_id,
            )
            .order_by(
                WorkflowAssignment.created_at.desc()
            )
            .all()
        )

    def get_active_by_officer(
        self,
        db: Session,
        officer_id: int,
    ) -> list[WorkflowAssignment]:

        return (
            db.query(
                WorkflowAssignment
            )
            .filter(
                WorkflowAssignment.assigned_to
                == officer_id,

                WorkflowAssignment.is_completed
                == False,
            )
            .order_by(
                WorkflowAssignment.created_at.desc()
            )
            .all()
        )

    def get_by_reference(
        self,
        db: Session,
        reference_number: str,
    ) -> list[WorkflowAssignment]:

        return (
            db.query(
                WorkflowAssignment
            )
            .filter(
                WorkflowAssignment.reference_number
                == reference_number
            )
            .order_by(
                WorkflowAssignment.created_at.asc()
            )
            .all()
        )

    # ---------------------------------
    # Business Methods
    # ---------------------------------

    def assign(
        self,
        db: Session,
        assignment: WorkflowAssignment,
    ) -> WorkflowAssignment:

        db.add(assignment)
        db.commit()
        db.refresh(assignment)

        return assignment

    def complete_assignment(
        self,
        db: Session,
        assignment: WorkflowAssignment,
    ) -> WorkflowAssignment:

        assignment.is_completed = True

        db.commit()
        db.refresh(assignment)

        return assignment


workflow_assignment_repository = (
    WorkflowAssignmentRepository()
)