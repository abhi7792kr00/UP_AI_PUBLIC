from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel


class Role(BaseModel):
    __tablename__ = "roles"

    role_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    users = relationship(
        "User",
        back_populates="role"
    )