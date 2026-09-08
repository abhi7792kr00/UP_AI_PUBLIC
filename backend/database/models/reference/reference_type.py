from sqlalchemy import Boolean
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ReferenceType(BaseModel):
    __tablename__ = "reference_types"

    module_name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    module_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    formats = relationship(
        "ReferenceFormat",
        back_populates="reference_type",
        cascade="all, delete-orphan",
    )