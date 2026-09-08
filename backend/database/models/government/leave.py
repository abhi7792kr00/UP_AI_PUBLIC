from datetime import date
from typing import Optional

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Leave(BaseModel):
    __tablename__ = "leaves"

    leave_order_no: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    leave_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    total_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    reason: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
    )

    approved_by: Mapped[Optional[int]] = mapped_column(
        ForeignKey("officers.id"),
        nullable=True,
    )

    officer_id: Mapped[int] = mapped_column(
        ForeignKey("officers.id"),
        nullable=False,
    )

    remarks: Mapped[Optional[str]] = mapped_column(
        String(300),
        nullable=True,
    )

    officer = relationship(
        "Officer",
        foreign_keys=[officer_id],
    )

    approver = relationship(
        "Officer",
        foreign_keys=[approved_by],
    )