from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Tehsil(BaseModel):
    __tablename__ = "tehsils"

    tehsil_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    tehsil_code: Mapped[str] = mapped_column(
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
        back_populates="tehsils",
    )

    blocks = relationship(
        "Block",
        secondary="block_tehsils",
        back_populates="tehsils",
    )
