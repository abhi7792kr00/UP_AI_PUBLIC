from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintCategory(BaseModel):
    __tablename__ = "complaint_categories"

    category_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    category_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    icon: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    color: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    mappings = relationship(
        "ComplaintCategoryMapping",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    complaints = relationship(
        "Complaint",
        back_populates="category",
    )

    subcategories = relationship(
    "ComplaintSubCategory",
    back_populates="category",
    cascade="all, delete-orphan",
    )