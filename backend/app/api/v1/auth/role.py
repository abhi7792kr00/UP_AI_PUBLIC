from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.schemas.auth.role_schema import (
    RoleCreate,
    RoleResponse,
)
from app.services.auth import role_service

router = APIRouter(
    prefix="/roles",
    tags=["Authentication - Roles"]
)


@router.get(
    "/",
    response_model=List[RoleResponse]
)
def get_roles(db: Session = Depends(get_db)):
    return role_service.get_all_roles(db)


@router.post(
    "/",
    response_model=RoleResponse
)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db)
):
    result = role_service.create_role(db, role)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Role already exists."
        )

    return result


@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db)
):
    success = role_service.delete_role(
        db,
        role_id
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Role not found."
        )

    return {"message": "Role deleted successfully."}