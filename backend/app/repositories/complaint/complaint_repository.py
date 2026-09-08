from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.repositories.base.base_repository import BaseRepository

from database.models.complaint.complaint import Complaint
from database.models.government.officer import Officer

from database.models.workflow.workflow_assignment import (
    WorkflowAssignment,
)


class ComplaintRepository(
    BaseRepository[Complaint]
):

    def __init__(self):
        super().__init__(
            Complaint
        )

    # ---------------------------------
    # Query Methods
    # ---------------------------------

    def get_by_complaint_number(
        self,
        db: Session,
        complaint_number: str,
    ) -> Complaint | None:

        return (
            db.query(Complaint)
            .options(
                joinedload(
                    Complaint.assigned_officer
                ).joinedload(
                    Officer.designation
                ),
                joinedload(
                    Complaint.assigned_officer
                ).joinedload(
                    Officer.department
                ),
                joinedload(
                    Complaint.assigned_officer
                ).joinedload(
                    Officer.office
                ),
            )
            .filter(
                Complaint.complaint_number
                == complaint_number
            )
            .first()
        )

    def get_by_citizen(
        self,
        db: Session,
        citizen_id: int,
    ) -> list[Complaint]:

        return (
            db.query(Complaint)
            .options(
                joinedload(
                    Complaint.assigned_officer
                ).joinedload(
                    Officer.designation
                ),
                joinedload(
                    Complaint.assigned_officer
                ).joinedload(
                    Officer.department
                ),
                joinedload(
                    Complaint.assigned_officer
                ).joinedload(
                    Officer.office
                ),
            )
            .filter(
                Complaint.citizen_id
                == citizen_id
            )
            .order_by(
                Complaint.created_at.desc()
            )
            .all()
        )

    def get_by_status(
        self,
        db: Session,
        status_id: int,
    ) -> list[Complaint]:

        return (
            db.query(Complaint)
            .filter(
                Complaint.status_id
                == status_id
            )
            .all()
        )

    def get_by_officer(
        self,
        db: Session,
        officer_id: int,
    ) -> list[Complaint]:

        return (
            db.query(Complaint)
            .filter(
                Complaint.assigned_officer_id
                == officer_id
            )
            .all()
        )

    # ---------------------------------
    # Officer Assigned Complaints
    # ---------------------------------

    def get_assigned_complaints_for_officer(
        self,
        db: Session,
        officer_id: int,
    ) -> list[Complaint]:

        # Find latest active workflow assignment
        # for every complaint assigned to this officer.

        latest_assignment = (
            db.query(
                WorkflowAssignment.reference_number,
                func.max(
                    WorkflowAssignment.created_at
                ).label(
                    "latest_created_at"
                ),
            )
            .filter(
                WorkflowAssignment.assigned_to
                == officer_id,

                WorkflowAssignment.is_completed
                == False,
            )
            .group_by(
                WorkflowAssignment.reference_number,
            )
            .subquery()
        )

        return (
            db.query(Complaint)
            .join(
                latest_assignment,
                latest_assignment.c.reference_number
                == Complaint.complaint_number,
            )
            .join(
                WorkflowAssignment,
                WorkflowAssignment.reference_number
                == latest_assignment.c.reference_number,
            )
            .filter(
                WorkflowAssignment.assigned_to
                == officer_id,

                WorkflowAssignment.is_completed
                == False,

                WorkflowAssignment.created_at
                == latest_assignment.c.latest_created_at,

                Complaint.is_active
                == True,
            )
            .order_by(
                Complaint.created_at.desc()
            )
            .all()
        )

    # ---------------------------------
    # Workflow Methods
    # ---------------------------------

    def update_status(
        self,
        db: Session,
        complaint: Complaint,
        status_id: int,
    ) -> Complaint:

        complaint.status_id = status_id

        db.add(complaint)
        db.flush()

        return complaint

    def get_dashboard_counts(
        self,
        db: Session,
    ):

        rows = (
            db.query(
                Complaint.status_id,
                func.count(Complaint.id),
            )
            .group_by(
                Complaint.status_id,
            )
            .all()
        )

        return {
            status_id: count
            for status_id, count in rows
        }


# ---------------------------------
# Repository Instance
# ---------------------------------

complaint_repository = ComplaintRepository()