from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    mobile: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
    )

    officer_id: Mapped[int | None] = mapped_column(
        ForeignKey("officers.id"),
        nullable=True,
    )

    role = relationship(
        "Role",
        back_populates="users",
    )

    officer = relationship(
        "Officer",
    )