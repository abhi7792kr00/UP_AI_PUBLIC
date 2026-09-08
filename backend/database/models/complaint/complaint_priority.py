from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintPriority(BaseModel):
    __tablename__ = "complaint_priorities"

    priority_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    priority_code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
    )

    sla_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    color: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    mappings = relationship(
        "ComplaintCategoryMapping",
        back_populates="priority",
    )

    complaints = relationship(
        "Complaint",
        back_populates="priority",
    )