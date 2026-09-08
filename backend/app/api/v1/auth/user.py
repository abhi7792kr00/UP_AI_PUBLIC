from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.dependencies import get_db

from app.schemas.auth.user_schema import (
    UserCreate,
    UserResponse,
)

from app.services.auth.user_service import user_service


router = APIRouter(
    prefix="/users",
    tags=["Authentication - Users"],
)


@router.get(
    "/",
    response_model=List[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    return user_service.get_all_users(
        db,
    )


@router.post(
    "/",
    response_model=UserResponse,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:

        result = user_service.create_user(
            db=db,
            full_name=user.full_name,
            username=user.username,
            email=user.email,
            password=user.password,
            mobile=user.mobile,
            role_id=user.role_id,
            officer_id=user.officer_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    return result


@router.delete(
    "/{user_id}",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):

    success = user_service.delete_user(
        db,
        user_id,
    )

    if not success:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return {
        "message": "User deleted successfully.",
    }