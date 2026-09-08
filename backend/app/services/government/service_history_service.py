from sqlalchemy.orm import Session

from database.models.government.posting import Posting
from database.models.government.transfer import Transfer
from database.models.government.promotion import Promotion
from database.models.government.leave import Leave
from database.models.government.suspension import Suspension
from database.models.government.retirement import Retirement
from database.models.government.training import Training

from app.schemas.government.service_history_schema import (
    ServiceHistoryResponse,
)


def build_posting_events(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    events = []

    postings = (
        db.query(Posting)
        .filter(
            Posting.officer_id == officer_id,
        )
        .all()
    )

    for posting in postings:

        events.append(
            ServiceHistoryResponse(
                event_type="Posting",
                event_date=posting.joining_date,
                title=(
                    f"Posted as "
                    f"{posting.designation.designation_name} "
                    f"at "
                    f"{posting.office.office_name}"
                ),
                reference_no=posting.posting_order_no,
                remarks=posting.remarks,
            )
        )

    return events


def build_transfer_events(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    events = []

    transfers = (
        db.query(Transfer)
        .filter(
            Transfer.officer_id == officer_id,
            Transfer.status == "Approved",
        )
        .all()
    )

    for transfer in transfers:

        events.append(
            ServiceHistoryResponse(
                event_type="Transfer",
                event_date=transfer.transfer_date,
                title=(
                    f"Transferred from "
                    f"{transfer.from_office.office_name} "
                    f"to "
                    f"{transfer.to_office.office_name}"
                ),
                reference_no=transfer.transfer_order_no,
                remarks=transfer.reason,
            )
        )

    return events


def build_promotion_events(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    events = []

    promotions = (
        db.query(Promotion)
        .filter(
            Promotion.officer_id == officer_id,
            Promotion.status == "Approved",
        )
        .all()
    )

    for promotion in promotions:

        events.append(
            ServiceHistoryResponse(
                event_type="Promotion",
                event_date=promotion.promotion_date,
                title=(
                    f"Promoted from "
                    f"{promotion.old_designation.designation_name} "
                    f"to "
                    f"{promotion.new_designation.designation_name}"
                ),
                reference_no=promotion.promotion_order_no,
                remarks=promotion.remarks,
            )
        )

    return events


def build_leave_events(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    events = []

    leaves = (
        db.query(Leave)
        .filter(
            Leave.officer_id == officer_id,
            Leave.status == "Approved",
        )
        .all()
    )

    for leave in leaves:

        events.append(
            ServiceHistoryResponse(
                event_type="Leave",
                event_date=leave.start_date,
                title=leave.leave_type,
                reference_no=leave.leave_order_no,
                remarks=leave.reason or leave.remarks,
            )
        )

    return events

def build_suspension_events(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    events = []

    suspensions = (
        db.query(Suspension)
        .filter(
            Suspension.officer_id == officer_id,
            Suspension.status.in_(
                [
                    "Active",
                    "Completed",
                ]
            ),
        )
        .all()
    )

    for suspension in suspensions:

        events.append(
            ServiceHistoryResponse(
                event_type="Suspension",
                event_date=suspension.suspension_date,
                title="Officer Suspended",
                reference_no=suspension.suspension_order_no,
                remarks=suspension.reason,
            )
        )

    return events


def build_retirement_events(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    events = []

    retirements = (
        db.query(Retirement)
        .filter(
            Retirement.officer_id == officer_id,
            Retirement.status == "Completed",
        )
        .all()
    )

    for retirement in retirements:

        events.append(
            ServiceHistoryResponse(
                event_type="Retirement",
                event_date=retirement.retirement_date,
                title=retirement.retirement_type,
                reference_no=retirement.retirement_order_no,
                remarks=retirement.remarks,
            )
        )

    return events


def build_training_events(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    events = []

    trainings = (
        db.query(Training)
        .filter(
            Training.officer_id == officer_id,
            Training.status == "Completed",
        )
        .all()
    )

    for training in trainings:

        events.append(
            ServiceHistoryResponse(
                event_type="Training",
                event_date=training.start_date,
                title=training.training_name,
                reference_no=training.training_order_no,
                remarks=training.remarks,
            )
        )

    return events


def get_service_history(
    db: Session,
    officer_id: int,
) -> list[ServiceHistoryResponse]:

    history = []

    history.extend(
        build_posting_events(
            db,
            officer_id,
        )
    )

    history.extend(
        build_transfer_events(
            db,
            officer_id,
        )
    )

    history.extend(
        build_promotion_events(
            db,
            officer_id,
        )
    )

    history.extend(
        build_leave_events(
            db,
            officer_id,
        )
    )

    history.extend(
        build_suspension_events(
            db,
            officer_id,
        )
    )

    history.extend(
        build_retirement_events(
            db,
            officer_id,
        )
    )

    history.extend(
        build_training_events(
            db,
            officer_id,
        )
    )

    history.sort(
        key=lambda event: event.event_date,
    )

    return history  