from sqlalchemy.orm import Session

from app.repositories.auth.user_repository import (
    user_repository,
)

from core.security.password import (
    verify_password,
)

from core.security.jwt_handler import (
    create_access_token,
)


def login(
    db: Session,
    username: str,
    password: str,
):
    user = user_repository.get_by_username(
        db,
        username,
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user.password_hash,
    ):
        return None

    if not user.is_active:
        return None

    token = create_access_token(
        data={
            "sub": user.username,
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }