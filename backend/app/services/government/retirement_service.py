from sqlalchemy.orm import Session

from app.repositories.government.retirement_repository import (
    create_retirement,
    get_retirements,
)

from app.schemas.government.retirement_schema import (
    RetirementCreate,
)


def create_retirement_service(
    db: Session,
    retirement: RetirementCreate,
):
    return create_retirement(
        db,
        retirement,
    )


def get_retirements_service(
    db: Session,
):
    return get_retirements(db)