from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintSubCategory(BaseModel):
    __tablename__ = "complaint_subcategories"

    category_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_categories.id"),
        nullable=False,
    )

    subcategory_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    subcategory_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    category = relationship(
        "ComplaintCategory",
        back_populates="subcategories",
    )

    complaints = relationship(
        "Complaint",
        back_populates="subcategory",
    )

    mappings = relationship(
    "ComplaintSubCategoryMapping",
    back_populates="subcategory",
    cascade="all, delete-orphan",
    )