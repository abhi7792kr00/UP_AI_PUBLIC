from sqlalchemy.orm import Session

from app.repositories.government import officer_repository
from app.schemas.government.officer_schema import (
    OfficerCreate,
    OfficerUpdate,
)
from database.models.government.officer import Officer


def get_officers(db: Session):
    return officer_repository.get_all(db)


def get_officer(db: Session, officer_id: int):
    return officer_repository.get_by_id(
        db,
        officer_id,
    )


def create_officer(
    db: Session,
    officer_data: OfficerCreate,
):
    officer = Officer(
    officer_name=officer_data.officer_name,
    employee_code=officer_data.employee_code,
    mobile=officer_data.mobile,
    email=officer_data.email,
    department_id=officer_data.department_id,
    designation_id=officer_data.designation_id,
    office_id=officer_data.office_id,
)

    return officer_repository.create(
        db,
        officer,
    )


def update_officer(
    db: Session,
    officer_id: int,
    officer_data: OfficerUpdate,
):
    officer = officer_repository.get_by_id(
        db,
        officer_id,
    )

    if not officer:
        return None

    update_data = officer_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(officer, key, value)

    db.commit()
    db.refresh(officer)

    return officer


def delete_officer(
    db: Session,
    officer_id: int,
):
    officer = officer_repository.get_by_id(
        db,
        officer_id,
    )

    if not officer:
        return False

    officer_repository.delete(
        db,
        officer,
    )

    return True