from sqlalchemy.orm import Session

from database.models.government.office import Office


def get_all(db: Session):
    return db.query(Office).all()


def get_by_id(
    db: Session,
    office_id: int,
):
    return (
        db.query(Office)
        .filter(
            Office.id == office_id
        )
        .first()
    )


def get_by_code(
    db: Session,
    office_code: str,
):
    return (
        db.query(Office)
        .filter(
            Office.office_code == office_code
        )
        .first()
    )


def create(
    db: Session,
    office: Office,
):
    db.add(office)
    db.commit()
    db.refresh(office)
    return office


def delete(
    db: Session,
    office: Office,
):
    db.delete(office)
    db.commit()