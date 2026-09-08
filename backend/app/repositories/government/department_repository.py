from sqlalchemy.orm import Session

from database.models.government.department import Department


def get_all(db: Session):
    return db.query(Department).all()


def get_by_id(db: Session, department_id: int):
    return (
        db.query(Department)
        .filter(Department.id == department_id)
        .first()
    )


def get_by_name(db: Session, department_name: str):
    return (
        db.query(Department)
        .filter(
            Department.department_name == department_name
        )
        .first()
    )


def create(db: Session, department: Department):
    db.add(department)
    db.commit()
    db.refresh(department)
    return department


def delete(db: Session, department: Department):
    db.delete(department)
    db.commit()