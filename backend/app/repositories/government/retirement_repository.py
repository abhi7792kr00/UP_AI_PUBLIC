from sqlalchemy.orm import Session

from database.models.government.retirement import Retirement

from app.schemas.government.retirement_schema import RetirementCreate


def create_retirement(
    db: Session,
    retirement: RetirementCreate,
):
    db_retirement = Retirement(**retirement.model_dump())

    db.add(db_retirement)
    db.commit()
    db.refresh(db_retirement)

    return db_retirement


def get_retirements(
    db: Session,
):
    return db.query(Retirement).all()