from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel


class Village(BaseModel):
    __tablename__ = "villages"

    village_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    village_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    gram_panchayat_id: Mapped[int | None] = mapped_column(
        ForeignKey("gram_panchayats.id"),
        nullable=True,
    )

    gram_panchayat = relationship(
        "GramPanchayat",
        back_populates="villages"
    )
    