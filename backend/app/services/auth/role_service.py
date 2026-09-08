from sqlalchemy.orm import Session

from app.repositories.auth import role_repository
from database.models.auth.role import Role
from app.schemas.auth.role_schema import RoleCreate


def get_all_roles(db: Session):
    return role_repository.get_all(db)


def get_role_by_id(db: Session, role_id: int):
    return role_repository.get_by_id(db, role_id)


def create_role(db: Session, role_data: RoleCreate):
    existing = role_repository.get_by_name(
        db,
        role_data.role_name
    )

    if existing:
        return None

    role = Role(
        role_name=role_data.role_name,
        description=role_data.description
    )

    return role_repository.create(db, role)


def delete_role(db: Session, role_id: int):
    role = role_repository.get_by_id(db, role_id)

    if not role:
        return False

    role_repository.delete(db, role)

    return True