from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Ward(BaseModel):
    __tablename__ = "wards"

    # -------------------------
    # Basic Information
    # -------------------------

    ward_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    ward_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # -------------------------
    # Administrative Hierarchy
    # -------------------------

    municipal_body_id: Mapped[int] = mapped_column(
        ForeignKey("municipal_bodies.id"),
        nullable=False,
    )

    # -------------------------
    # Statistics
    # -------------------------

    population: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    # -------------------------
    # Relationships
    # -------------------------

    municipal_body = relationship(
        "MunicipalBody",
        back_populates="wards",
    )

    localities = relationship(
    "Locality",
    back_populates="ward",
    cascade="all, delete-orphan",
    )