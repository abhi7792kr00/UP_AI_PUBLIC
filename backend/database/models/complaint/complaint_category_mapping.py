from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintCategoryMapping(BaseModel):
    __tablename__ = "complaint_category_mappings"

    category_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_categories.id"),
        nullable=False,
    )

    administrative_level_id: Mapped[int] = mapped_column(
        ForeignKey("administrative_levels.id"),
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False,
    )

    office_id: Mapped[int] = mapped_column(
        ForeignKey("offices.id"),
        nullable=False,
    )

    designation_id: Mapped[int] = mapped_column(
        ForeignKey("designations.id"),
        nullable=False,
    )

    priority_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_priorities.id"),
        nullable=False,
    )

    sla_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    category = relationship(
        "ComplaintCategory",
        back_populates="mappings",
    )

    administrative_level = relationship(
        "AdministrativeLevel",
        back_populates="complaint_category_mappings",
    )

    department = relationship(
        "Department",
    )

    office = relationship(
        "Office",
    )

    designation = relationship(
        "Designation",
    )

    priority = relationship(
        "ComplaintPriority",
        back_populates="mappings",
    )