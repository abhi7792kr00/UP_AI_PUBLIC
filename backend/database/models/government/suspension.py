from datetime import date

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Suspension(BaseModel):
    __tablename__ = "suspensions"

    suspension_order_no: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    suspension_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    officer_id: Mapped[int] = mapped_column(
        ForeignKey("officers.id"),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        String(300),
        nullable=False,
    )

    duration_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Active",
        nullable=False,
    )

    officer = relationship("Officer")