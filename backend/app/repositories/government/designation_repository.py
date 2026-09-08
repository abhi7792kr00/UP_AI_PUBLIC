from sqlalchemy.orm import Session

from database.models.government.designation import Designation


def get_all(db: Session):
    return db.query(Designation).all()


def get_by_id(db: Session, designation_id: int):
    return (
        db.query(Designation)
        .filter(
            Designation.id == designation_id
        )
        .first()
    )


def get_by_name(db: Session, designation_name: str):
    return (
        db.query(Designation)
        .filter(
            Designation.designation_name == designation_name
        )
        .first()
    )


def create(db: Session, designation: Designation):
    db.add(designation)
    db.commit()
    db.refresh(designation)
    return designation


def delete(db: Session, designation: Designation):
    db.delete(designation)
    db.commit()