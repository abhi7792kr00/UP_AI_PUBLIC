from sqlalchemy.orm import Session

from database.models.auth.role import Role


def get_all(db: Session):
    return db.query(Role).all()


def get_by_id(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def get_by_name(db: Session, role_name: str):
    return db.query(Role).filter(Role.role_name == role_name).first()


def create(db: Session, role: Role):
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def delete(db: Session, role: Role):
    db.delete(role)
    db.commit()