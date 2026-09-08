from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Block(BaseModel):
    __tablename__ = "blocks"

    block_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    block_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    district_id: Mapped[int] = mapped_column(
        ForeignKey("districts.id"),
        nullable=False,
    )

    district = relationship(
        "District",
        back_populates="blocks",
    )

    tehsils = relationship(
        "Tehsil",
        secondary="block_tehsils",
        back_populates="blocks",
    )

    gram_panchayats = relationship(
        "GramPanchayat",
        back_populates="block",
        cascade="all, delete-orphan",
    )
