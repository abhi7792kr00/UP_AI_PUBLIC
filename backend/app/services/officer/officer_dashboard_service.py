from sqlalchemy.orm import Session

from app.services.complaint.complaint_service import (
    complaint_service,
)


class OfficerDashboardService:

    def get_dashboard(
        self,
        db: Session,
    ):
        counts = (
            complaint_service.get_dashboard_counts(
                db,
            )
        )

        total = sum(counts.values())

        return {
            "total_complaints": total,

            "pending": counts.get(1, 0),

            "under_investigation": counts.get(3, 0),

            "resolved": counts.get(4, 0),

            "closed": counts.get(5, 0),

            "reopened": counts.get(8, 0),
        }


officer_dashboard_service = OfficerDashboardService()