from sqlalchemy.orm import Session

from app.repositories.auth.user_repository import (
    user_repository,
)

from app.services.base.base_service import (
    BaseService,
)

from database.models.auth.user import (
    User,
)

from core.security.password import (
    hash_password,
)


class UserService(BaseService):
    """
    Service for User.
    """

    def __init__(self):
        super().__init__(
            user_repository,
        )

    # ==========================================
    # Query Methods
    # ==========================================

    def get_by_username(
        self,
        db: Session,
        username: str,
    ):
        return self.repository.get_by_username(
            db,
            username,
        )

    def get_by_email(
        self,
        db: Session,
        email: str,
    ):
        return self.repository.get_by_email(
            db,
            email,
        )

    def get_by_mobile(
        self,
        db: Session,
        mobile: str,
    ):
        return self.repository.get_by_mobile(
            db,
            mobile,
        )

    # ==========================================
    # Create User
    # ==========================================

    def create_user(
        self,
        db: Session,
        *,
        full_name: str,
        username: str,
        email: str,
        password: str,
        mobile: str | None,
        role_id: int,
        officer_id: int | None = None,
    ):

        if self.get_by_username(
            db,
            username,
        ):
            raise ValueError(
                "Username already exists."
            )

        if self.get_by_email(
            db,
            email,
        ):
            raise ValueError(
                "Email already exists."
            )

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            password_hash=hash_password(
                password,
            ),
            mobile=mobile,
            role_id=role_id,
            officer_id=officer_id,
        )

        return self.create(
            db,
            user,
        )


# ==========================================
# Service Instance
# ==========================================

user_service = UserService()
