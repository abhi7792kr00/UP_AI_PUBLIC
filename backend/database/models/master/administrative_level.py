from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class AdministrativeLevel(BaseModel):
    __tablename__ = "administrative_levels"

    level_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    level_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    complaint_category_mappings = relationship(
        "ComplaintCategoryMapping",
        back_populates="administrative_level",
    )