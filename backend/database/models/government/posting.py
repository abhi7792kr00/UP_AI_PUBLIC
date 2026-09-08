from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Posting(BaseModel):
    __tablename__ = "postings"

    posting_order_no: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    joining_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    relieving_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    officer_id: Mapped[int] = mapped_column(
        ForeignKey("officers.id"),
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False,
    )

    designation_id: Mapped[int] = mapped_column(
        ForeignKey("designations.id"),
        nullable=False,
    )

    office_id: Mapped[int] = mapped_column(
        ForeignKey("offices.id"),
        nullable=False,
    )

    officer = relationship(
        "Officer",
        back_populates="postings",
    )

    department = relationship(
        "Department",
        back_populates="postings",
    )

    designation = relationship(
        "Designation",
        back_populates="postings",
    )

    office = relationship(
        "Office",
        back_populates="postings",
    )
