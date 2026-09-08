from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ReferenceSequence(BaseModel):
    __tablename__ = "reference_sequences"

    reference_format_id: Mapped[int] = mapped_column(
        ForeignKey("reference_formats.id"),
        nullable=False,
    )

    sequence_period: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    period_value: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    current_sequence: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    last_generated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    reference_format = relationship(
        "ReferenceFormat",
        back_populates="sequences",
    )