from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class Department(BaseModel):
    __tablename__ = "departments"

    department_name: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    department_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(300),
        nullable=True
    )

    designations = relationship(
        "Designation",
        back_populates="department"
    )

    officers = relationship(
        "Officer",
        back_populates="department"
    )
    offices = relationship(
    "Office",
    back_populates="department"
    )

    postings = relationship(
        "Posting",
        back_populates="department",
    )    

        