from datetime import date

from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Transfer(BaseModel):
    __tablename__ = "transfers"

    transfer_order_no: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    transfer_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    relieving_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    joining_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    officer_id: Mapped[int] = mapped_column(
        ForeignKey("officers.id"),
        nullable=False,
    )

    from_office_id: Mapped[int] = mapped_column(
        ForeignKey("offices.id"),
        nullable=False,
    )

    to_office_id: Mapped[int] = mapped_column(
        ForeignKey("offices.id"),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
    )

    officer = relationship(
        "Officer",
    )

    from_office = relationship(
        "Office",
        foreign_keys=[from_office_id],
    )

    to_office = relationship(
        "Office",
        foreign_keys=[to_office_id],
    )