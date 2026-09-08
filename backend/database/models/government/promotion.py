from datetime import date
from typing import Optional

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Promotion(BaseModel):
    __tablename__ = "promotions"

    promotion_order_no: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    promotion_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    officer_id: Mapped[int] = mapped_column(
        ForeignKey("officers.id"),
        nullable=False,
    )

    old_designation_id: Mapped[int] = mapped_column(
        ForeignKey("designations.id"),
        nullable=False,
    )

    new_designation_id: Mapped[int] = mapped_column(
        ForeignKey("designations.id"),
        nullable=False,
    )

    remarks: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
    )

    officer = relationship("Officer")

    old_designation = relationship(
        "Designation",
        foreign_keys=[old_designation_id],
    )

    new_designation = relationship(
        "Designation",
        foreign_keys=[new_designation_id],
    )