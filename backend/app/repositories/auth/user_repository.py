from sqlalchemy.orm import Session

from app.repositories.base.base_repository import (
    BaseRepository,
)

from database.models.auth.user import User


class UserRepository(
    BaseRepository[User]
):
    """
    Repository for User.
    """

    def __init__(self):
        super().__init__(User)

    # -------------------------
    # Query Methods
    # -------------------------

    def get_by_username(
        self,
        db: Session,
        username: str,
    ):
        return (
            db.query(User)
            .filter(
                User.username == username,
            )
            .first()
        )

    def get_by_email(
        self,
        db: Session,
        email: str,
    ):
        return (
            db.query(User)
            .filter(
                User.email == email,
            )
            .first()
        )

    def get_by_mobile(
        self,
        db: Session,
        mobile: str,
    ):
        return (
            db.query(User)
            .filter(
                User.mobile == mobile,
            )
            .first()
        )


user_repository = UserRepository()