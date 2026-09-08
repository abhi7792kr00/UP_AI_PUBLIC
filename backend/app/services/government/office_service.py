from sqlalchemy.orm import Session

from app.repositories.government import office_repository
from app.schemas.government.office_schema import (
    OfficeCreate,
    OfficeUpdate,
)
from database.models.government.office import Office


def get_offices(db: Session):
    return office_repository.get_all(db)


def get_office(db: Session, office_id: int):
    return office_repository.get_by_id(
        db,
        office_id,
    )


def create_office(
    db: Session,
    office_data: OfficeCreate,
):
    office = Office(
        office_name=office_data.office_name,
        office_code=office_data.office_code,
        address=office_data.address,
        phone=office_data.phone,
        email=office_data.email,
        department_id=office_data.department_id,
    )

    return office_repository.create(
        db,
        office,
    )


def update_office(
    db: Session,
    office_id: int,
    office_data: OfficeUpdate,
):
    office = office_repository.get_by_id(
        db,
        office_id,
    )

    if not office:
        return None

    update_data = office_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(office, key, value)

    db.commit()
    db.refresh(office)

    return office


def delete_office(
    db: Session,
    office_id: int,
):
    office = office_repository.get_by_id(
        db,
        office_id,
    )

    if not office:
        return False

    office_repository.delete(
        db,
        office,
    )

    return True