from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel


class GramPanchayat(BaseModel):
    __tablename__ = "gram_panchayats"

    gram_panchayat_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    gram_panchayat_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    block_id: Mapped[int | None] = mapped_column(
        ForeignKey("blocks.id"),
        nullable=True,
    )

    block = relationship(
        "Block",
        back_populates="gram_panchayats"
    )

    villages = relationship(
        "Village",
        back_populates="gram_panchayat",
        cascade="all, delete-orphan"
    )