from sqlalchemy.orm import Session

from database.models.government.department import Department

from app.repositories.government import department_repository

from app.schemas.government.department_schema import (
    DepartmentCreate,
    DepartmentUpdate,
)


def get_all_departments(db: Session):
    return department_repository.get_all(db)


def get_department_by_id(
    db: Session,
    department_id: int,
):
    return department_repository.get_by_id(
        db,
        department_id
    )


def create_department(
    db: Session,
    department_data: DepartmentCreate,
):
    existing = department_repository.get_by_name(
        db,
        department_data.department_name,
    )

    if existing:
        return None

    department = Department(
        department_name=department_data.department_name,
        department_code=department_data.department_code,
        description=department_data.description,
    )

    return department_repository.create(
        db,
        department,
    )


def update_department(
    db: Session,
    department_id: int,
    department_data: DepartmentUpdate,
):
    department = department_repository.get_by_id(
        db,
        department_id,
    )

    if department is None:
        return None

    if department_data.department_name is not None:
        department.department_name = (
            department_data.department_name
        )

    if department_data.department_code is not None:
        department.department_code = (
            department_data.department_code
        )

    if department_data.description is not None:
        department.description = (
            department_data.description
        )

    db.commit()
    db.refresh(department)

    return department


def delete_department(
    db: Session,
    department_id: int,
):
    department = department_repository.get_by_id(
        db,
        department_id,
    )

    if department is None:
        return False

    department_repository.delete(
        db,
        department,
    )

    return True