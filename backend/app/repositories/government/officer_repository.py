from sqlalchemy.orm import Session

from database.models.government.officer import Officer


def get_all(db: Session):
    return db.query(Officer).all()


def get_by_id(
    db: Session,
    officer_id: int,
):
    return (
        db.query(Officer)
        .filter(
            Officer.id == officer_id
        )
        .first()
    )


def get_by_employee_code(
    db: Session,
    employee_code: str,
):
    return (
        db.query(Officer)
        .filter(
            Officer.employee_code == employee_code
        )
        .first()
    )


def get_matching_officer(
    db: Session,
    department_id: int,
    designation_id: int,
    office_id: int,
):
    return (
        db.query(Officer)
        .filter(
            Officer.department_id == department_id,
            Officer.designation_id == designation_id,
            Officer.office_id == office_id,
            Officer.is_active == True,
        )
        .order_by(
            Officer.id.asc()
        )
        .first()
    )


def create(
    db: Session,
    officer: Officer,
):
    db.add(officer)
    db.commit()
    db.refresh(officer)

    return officer


def delete(
    db: Session,
    officer: Officer,
):
    db.delete(officer)
    db.commit()