from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Designation(BaseModel):
    __tablename__ = "designations"

    designation_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    designation_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(300),
        nullable=True
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )

    department = relationship(
        "Department",
        back_populates="designations"
    )

    officers = relationship(
        "Officer",
        back_populates="designation"
    )

    postings = relationship(
        "Posting",
        back_populates="designation",
    )