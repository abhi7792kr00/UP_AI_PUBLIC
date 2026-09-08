from sqlalchemy.orm import Session

from database.models.complaint.complaint_priority import ComplaintPriority


DATA = [
    {
        "priority_name": "Low",
        "priority_code": "LOW",
        "sla_days": 15,
        "color": "#4CAF50",
        "description": "Low Priority",
    },
    {
        "priority_name": "Medium",
        "priority_code": "MEDIUM",
        "sla_days": 7,
        "color": "#FFC107",
        "description": "Medium Priority",
    },
    {
        "priority_name": "High",
        "priority_code": "HIGH",
        "sla_days": 3,
        "color": "#FF9800",
        "description": "High Priority",
    },
    {
        "priority_name": "Critical",
        "priority_code": "CRITICAL",
        "sla_days": 1,
        "color": "#F44336",
        "description": "Critical Priority",
    },
    {
        "priority_name": "Emergency",
        "priority_code": "EMERGENCY",
        "sla_days": 0,
        "color": "#B71C1C",
        "description": "Emergency Complaint",
    },
]


def seed_complaint_priorities(db: Session):
    for item in DATA:

        exists = (
            db.query(ComplaintPriority)
            .filter(
                ComplaintPriority.priority_code == item["priority_code"]
            )
            .first()
        )

        if exists:
            continue

        db.add(ComplaintPriority(**item))

    db.commit()

    print("✓ Complaint Priorities Seeded")