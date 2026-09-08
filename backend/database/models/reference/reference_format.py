from sqlalchemy import Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ReferenceFormat(BaseModel):
    __tablename__ = "reference_formats"

    reference_type_id: Mapped[int] = mapped_column(
        ForeignKey("reference_types.id"),
        nullable=False,
    )

    format_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    prefix: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    separator: Mapped[str] = mapped_column(
        String(5),
        default="-",
        nullable=False,
    )

    sequence_length: Mapped[int] = mapped_column(
        Integer,
        default=6,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    reference_type = relationship(
        "ReferenceType",
        back_populates="formats",
    )

    sequences = relationship(
        "ReferenceSequence",
        back_populates="reference_format",
        cascade="all, delete-orphan",
    )