from sqlalchemy import Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from core.database.base_model import BaseModel


class ComplaintStatus(BaseModel):
    __tablename__ = "complaint_statuses"

    status_name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    status_code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    display_order: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    is_final: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    allow_reopen: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    color: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )

    complaints = relationship(
        "Complaint",
        back_populates="status",
    )