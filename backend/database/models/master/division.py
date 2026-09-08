from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel


class Division(BaseModel):
    __tablename__ = "divisions"

    division_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    division_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    state_id: Mapped[int] = mapped_column(
        ForeignKey("states.id")
    )

    state = relationship(
        "State",
        back_populates="divisions"
    )

    districts = relationship(
        "District",
        back_populates="division",
        cascade="all, delete-orphan"
    )