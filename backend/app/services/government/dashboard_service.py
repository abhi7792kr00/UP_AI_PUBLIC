from sqlalchemy import func
from sqlalchemy.orm import Session

from database.models.government.officer import Officer
from database.models.government.posting import Posting
from database.models.government.transfer import Transfer
from database.models.government.promotion import Promotion
from database.models.government.leave import Leave
from database.models.government.suspension import Suspension
from database.models.government.retirement import Retirement
from database.models.government.training import Training

from app.schemas.government.dashboard_schema import (
    DashboardResponse,
)


def get_dashboard(
    db: Session,
) -> DashboardResponse:

    total_officers = (
        db.query(
            func.count(Officer.id)
        )
        .scalar()
    )

    active_postings = (
        db.query(
            func.count(Posting.id)
        )
        .filter(
            Posting.is_current == True,
        )
        .scalar()
    )

    total_transfers = (
        db.query(
            func.count(Transfer.id)
        )
        .scalar()
    )

    total_promotions = (
        db.query(
            func.count(Promotion.id)
        )
        .scalar()
    )

    total_leaves = (
        db.query(
            func.count(Leave.id)
        )
        .scalar()
    )

    active_suspensions = (
        db.query(
            func.count(Suspension.id)
        )
        .filter(
            Suspension.status == "Active",
        )
        .scalar()
    )

    total_retirements = (
        db.query(
            func.count(Retirement.id)
        )
        .scalar()
    )

    completed_trainings = (
        db.query(
            func.count(Training.id)
        )
        .filter(
            Training.status == "Completed",
        )
        .scalar()
    )

    return DashboardResponse(
        total_officers=total_officers,
        active_postings=active_postings,
        total_transfers=total_transfers,
        total_promotions=total_promotions,
        total_leaves=total_leaves,
        active_suspensions=active_suspensions,
        total_retirements=total_retirements,
        completed_trainings=completed_trainings,
    )