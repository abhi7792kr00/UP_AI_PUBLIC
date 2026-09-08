from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models.government.officer import Officer
from database.models.complaint.complaint import Complaint
from database.models.complaint.complaint_status import ComplaintStatus
from database.models.workflow.workflow_assignment import (
    WorkflowAssignment,
)

from app.schemas.officer.dashboard_schema import (
    OfficerDashboardResponse,
    OfficerComplaintItem,
)


def get_officer_dashboard(
    db: Session,
    officer_id: int,
) -> OfficerDashboardResponse:

    # ==========================================
    # 1. Get Officer
    # ==========================================

    officer = (
        db.query(Officer)
        .filter(
            Officer.id == officer_id,
        )
        .first()
    )

    if officer is None:
        raise ValueError(
            "Officer not found."
        )

    # ==========================================
    # 2. Latest assignment for each complaint
    # ==========================================

    latest_assignment = (
        db.query(
            WorkflowAssignment.reference_number,
            func.max(
                WorkflowAssignment.created_at
            ).label("latest_created_at"),
        )
        .filter(
            WorkflowAssignment.assigned_to
            == officer_id,
        )
        .group_by(
            WorkflowAssignment.reference_number,
        )
        .subquery()
    )

    # ==========================================
    # 3. Current assigned complaints
    # ==========================================

    complaint_rows = (
        db.query(
            Complaint,
            ComplaintStatus.status_code,
            WorkflowAssignment.created_at,
            WorkflowAssignment.remarks,
        )
        .join(
            ComplaintStatus,
            Complaint.status_id
            == ComplaintStatus.id,
        )
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

            WorkflowAssignment.created_at
            == latest_assignment.c.latest_created_at,

            WorkflowAssignment.is_completed
            == False,
        )
        .order_by(
            Complaint.created_at.desc(),
        )
        .all()
    )

    # ==========================================
    # 4. Status counts
    # ==========================================

    status_counts = {}

    for (
        complaint,
        status_code,
        assigned_at,
        remarks,
    ) in complaint_rows:

        status_counts[status_code] = (
            status_counts.get(
                status_code,
                0,
            )
            + 1
        )

    # ==========================================
    # 5. Complaint list
    # ==========================================

    complaints = []

    for (
        complaint,
        status_code,
        assigned_at,
        remarks,
    ) in complaint_rows:

        complaints.append(
            OfficerComplaintItem(
                complaint_number=(
                    complaint.complaint_number
                ),

                subject=complaint.subject,

                description=(
                    complaint.description
                ),

                category_id=(
                    complaint.category_id
                ),

                priority_id=(
                    complaint.priority_id
                ),

                status_id=(
                    complaint.status_id
                ),

                address=complaint.address,

                assigned_at=assigned_at,

                remarks=remarks,
            )
        )

    # ==========================================
    # 6. Return dashboard
    # ==========================================

    return OfficerDashboardResponse(
        officer_id=officer.id,

        officer_name=(
            officer.officer_name
        ),

        employee_code=(
            officer.employee_code
        ),

        total_assigned=len(
            complaints
        ),

        pending=status_counts.get(
            "PENDING",
            0,
        ),

        assigned=status_counts.get(
            "ASSIGNED",
            0,
        ),

        in_progress=status_counts.get(
            "IN_PROGRESS",
            0,
        ),

        resolved=status_counts.get(
            "RESOLVED",
            0,
        ),

        escalated=status_counts.get(
            "ESCALATED",
            0,
        ),

        reopened=status_counts.get(
            "REOPENED",
            0,
        ),

        closed=status_counts.get(
            "CLOSED",
            0,
        ),

        rejected=status_counts.get(
            "REJECTED",
            0,
        ),

        complaints=complaints,
    )