from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel


class District(BaseModel):
    __tablename__ = "districts"

    district_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    district_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    division_id: Mapped[int] = mapped_column(
        ForeignKey("divisions.id")
    )

    division = relationship(
        "Division",
        back_populates="districts"
    )

    tehsils = relationship(
    "Tehsil",
    back_populates="district",
    cascade="all, delete-orphan"
    )

    blocks = relationship(
    "Block",
    back_populates="district",
    cascade="all, delete-orphan",
    )

    municipal_bodies = relationship(
    "MunicipalBody",
    back_populates="district",
    cascade="all, delete-orphan",
    )