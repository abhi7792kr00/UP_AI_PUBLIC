from sqlalchemy.orm import Session

from database.models.complaint.complaint_status import ComplaintStatus


DATA = [
    {
        "status_name": "Pending",
        "status_code": "PENDING",
        "display_order": 1,
        "is_final": False,
        "allow_reopen": False,
        "color": "#9E9E9E",
        "description": "Complaint Registered",
    },
    {
        "status_name": "Assigned",
        "status_code": "ASSIGNED",
        "display_order": 2,
        "is_final": False,
        "allow_reopen": False,
        "color": "#2196F3",
        "description": "Assigned to Officer",
    },
    {
        "status_name": "In Progress",
        "status_code": "IN_PROGRESS",
        "display_order": 3,
        "is_final": False,
        "allow_reopen": False,
        "color": "#FF9800",
        "description": "Work in Progress",
    },
    {
        "status_name": "Resolved",
        "status_code": "RESOLVED",
        "display_order": 4,
        "is_final": False,
        "allow_reopen": True,
        "color": "#4CAF50",
        "description": "Resolved Awaiting Citizen Confirmation",
    },
    {
        "status_name": "Closed",
        "status_code": "CLOSED",
        "display_order": 5,
        "is_final": True,
        "allow_reopen": True,
        "color": "#2E7D32",
        "description": "Complaint Closed",
    },
    {
        "status_name": "Rejected",
        "status_code": "REJECTED",
        "display_order": 6,
        "is_final": True,
        "allow_reopen": True,
        "color": "#F44336",
        "description": "Complaint Rejected",
    },
    {
        "status_name": "Escalated",
        "status_code": "ESCALATED",
        "display_order": 7,
        "is_final": False,
        "allow_reopen": False,
        "color": "#9C27B0",
        "description": "Escalated to Higher Authority",
    },
    {
        "status_name": "Reopened",
        "status_code": "REOPENED",
        "display_order": 8,
        "is_final": False,
        "allow_reopen": False,
        "color": "#795548",
        "description": "Complaint Reopened",
    },
]


def seed_complaint_statuses(db: Session):
    for item in DATA:

        exists = (
            db.query(ComplaintStatus)
            .filter(
                ComplaintStatus.status_code == item["status_code"]
            )
            .first()
        )

        if exists:
            continue

        db.add(ComplaintStatus(**item))

    db.commit()

    print("✓ Complaint Statuses Seeded")