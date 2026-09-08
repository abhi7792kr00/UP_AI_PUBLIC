from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base_model import BaseModel


class Locality(BaseModel):
    __tablename__ = "localities"

    # -------------------------
    # Basic Information
    # -------------------------

    locality_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    locality_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    # -------------------------
    # Hierarchy
    # -------------------------

    ward_id: Mapped[int] = mapped_column(
        ForeignKey("wards.id"),
        nullable=False,
    )

    # -------------------------
    # Optional Details
    # -------------------------

    pincode: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # -------------------------
    # Relationships
    # -------------------------

    ward = relationship(
        "Ward",
        back_populates="localities",
    )