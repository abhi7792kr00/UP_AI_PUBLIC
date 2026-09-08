from sqlalchemy.orm import Session

from app.repositories.government import designation_repository
from database.models.government.designation import Designation
from app.schemas.government.designation_schema import (
    DesignationCreate,
    DesignationUpdate,
)


def get_designations(db: Session):
    return designation_repository.get_all(db)


def get_designation(db: Session, designation_id: int):
    return designation_repository.get_by_id(
        db,
        designation_id,
    )


def create_designation(
    db: Session,
    designation_data: DesignationCreate,
):
    designation = Designation(
        designation_name=designation_data.designation_name,
        designation_code=designation_data.designation_code,
        description=designation_data.description,
        department_id=designation_data.department_id,
    )

    return designation_repository.create(
        db,
        designation,
    )


def update_designation(
    db: Session,
    designation_id: int,
    designation_data: DesignationUpdate,
):
    designation = designation_repository.get_by_id(
        db,
        designation_id,
    )

    if not designation:
        return None

    update_data = designation_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(designation, key, value)

    db.commit()
    db.refresh(designation)

    return designation


def delete_designation(
    db: Session,
    designation_id: int,
):
    designation = designation_repository.get_by_id(
        db,
        designation_id,
    )

    if not designation:
        return False

    designation_repository.delete(
        db,
        designation,
    )

    return True