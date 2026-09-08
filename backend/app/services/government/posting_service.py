from sqlalchemy.orm import Session

from app.repositories.government import posting_repository
from app.schemas.government.posting_schema import (
    PostingCreate,
    PostingUpdate,
)
from database.models.government.posting import Posting


def get_postings(db: Session):
    return posting_repository.get_all(db)


def get_posting(
    db: Session,
    posting_id: int,
):
    return posting_repository.get_by_id(
        db,
        posting_id,
    )


def create_posting(
    db: Session,
    posting_data: PostingCreate,
):
    posting = Posting(
        posting_order_no=posting_data.posting_order_no,
        joining_date=posting_data.joining_date,
        relieving_date=posting_data.relieving_date,
        remarks=posting_data.remarks,
        officer_id=posting_data.officer_id,
        department_id=posting_data.department_id,
        designation_id=posting_data.designation_id,
        office_id=posting_data.office_id,
    )

    return posting_repository.create(
        db,
        posting,
    )


def update_posting(
    db: Session,
    posting_id: int,
    posting_data: PostingUpdate,
):
    posting = posting_repository.get_by_id(
        db,
        posting_id,
    )

    if not posting:
        return None

    update_data = posting_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(posting, key, value)

    db.commit()
    db.refresh(posting)

    return posting


def delete_posting(
    db: Session,
    posting_id: int,
):
    posting = posting_repository.get_by_id(
        db,
        posting_id,
    )

    if not posting:
        return False

    posting_repository.delete(
        db,
        posting,
    )

    return True
