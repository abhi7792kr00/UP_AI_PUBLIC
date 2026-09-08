from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel


class State(BaseModel):
    __tablename__ = "states"

    state_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    state_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    divisions = relationship(
        "Division",
        back_populates="state",
        cascade="all, delete-orphan"
    )