from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Officer(BaseModel):
    __tablename__ = "officers"

    officer_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    employee_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    mobile: Mapped[str] = mapped_column(
        String(15),
        unique=True,
        nullable=False,
    )

    photo_url: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    office_address: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    joining_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    retirement_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_public: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    # -------------------------
    # Foreign Keys
    # -------------------------

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

    # -------------------------
    # Relationships
    # -------------------------

    department = relationship(
        "Department",
        back_populates="officers",
    )

    designation = relationship(
        "Designation",
        back_populates="officers",
    )

    office = relationship(
        "Office",
        back_populates="officers",
    )

    postings = relationship(
        "Posting",
        back_populates="officer",
    )